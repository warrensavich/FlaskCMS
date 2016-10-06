import config
import json
import datetime
from flask import Flask, render_template, request, redirect, Markup, send_from_directory, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, RoleMixin, UserMixin
from flask.ext.login import LoginManager
from flask.ext.restful import abort, marshal, marshal_with, fields, Resource
from flask_mail import Mail
from flask.ext.restful import Api
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy import func
from flask.ext.principal import Principal
from flask.ext.security.signals import user_registered
from flask.ext.security.recoverable import generate_reset_password_token, send_reset_password_instructions, reset_password_token_status, update_password
from jinja_filters import register_filters, has_admin, can_edit, can_publish
from flask.ext.login import current_user
from werkzeug import secure_filename
from werkzeug.routing import BaseConverter, ValidationError
import re, os, base64, hashlib, mammoth, mimetypes, random, string

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters = register_filters(app.jinja_env.filters)
db = SQLAlchemy(app)
mail = Mail(app)
api = Api(app)
admin = Admin(app)
principals = Principal(app)
login_manager = LoginManager(app)

class UnstaticConverter(BaseConverter):
    def to_python(self, v):
        if v == "static":
            raise ValidationError()
        else:
            return v

    def to_url(self, v):
        return v

app.url_map.converters['unstatic'] = UnstaticConverter

from flask_security.forms import RegisterForm, TextField, Required

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])

import models
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

@app.context_processor
def nav_context():
    from models import Section, Page
    sections = Section.query.filter_by(deleted=False).all()
    navs = []
    for s in sections:
        pages = Page.query.filter_by(section=s.id).filter_by(deleted=False).all()
        part = {'title': s.title,
                'url': "/" + s.slug,
                'slug': s.slug,
                'preview': s.preview,
                'type': s.section_type,
                'children': [{'title': p.title,
                              'slug': p.slug,
                              'preview': p.preview,
                              'url': "/" + s.slug + "/" + p.slug} for p in pages if str(p.slug) != "_main"]
            }
        navs.append(part)
    return dict(navs=navs, main=Section.query.filter_by(slug=app.config['MAIN_SECTION']).first())

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    send_reset_password_instructions(user)
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/welcome?next=' + request.path)

# Views

@app.route('/image/<image_id>', methods=['GET', 'PUT', 'DELETE'])
def image(image_id):
    if current_user.is_authenticated():
        if has_admin(current_user):
            from models import Image
            i = Image.query.get(int(image_id))
            if request.method == 'PUT':
                i.title = request.json.get('title')
                i.link = request.json.get('link')
                i.alt_text = request.json.get('alt_text')
                db.session.add(i)
                db.session.commit()
                return "ok"
            if request.method == 'DELETE':
                Image.query.filter_by(id=image_id).delete()
                db.session.commit()
                return "ok"
            else:
                return "coming soon"
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/gallery/', methods=['GET'])
@app.route('/gallery/<gallery_slug>', methods=['GET', 'POST'])
def gallery(gallery_slug=None):
    if request.method == 'GET':
        from models import Gallery, Section
        if gallery_slug:
            g = Gallery.query.filter_by(slug=gallery_slug).first()
        else:
            galleries = Gallery.query.all()
        if request.headers['Content-Type'] == "application/json":
            return jsonify(**{'images': [{'url': i.url} for i in g.images],
                              'title': g.title,
                              'slug': g.slug})
        else:
            if gallery_slug:
                return render_template("gallery_view.html", g=g, sections=Section.query.all())
            else:
                return render_template("galleries_view.html", galleries = galleries)
    else:
        if current_user.is_authenticated():
            if has_admin(current_user):
                if request.method == 'POST':
                    from models import Gallery, Image
                    f = request.files['file']
                    path = save_file(f)
                    g = Gallery.query.filter_by(slug=gallery_slug).first()
                    i = Image()
                    i.creator = current_user.id
                    i.created = datetime.datetime.now()
                    i.preview = True
                    i.gallery = g.id
                    i.url = "/uploads/" + path
                    db.session.add(i)
                    db.session.commit()
                    return jsonify(**{'url': i.url,
                                      'id': i.id})
                else:
                    return abort(401)
            else:
                return abort(401)

@app.route('/new_gallery', methods=['GET', 'POST'])
def new_gallery():
    if current_user.is_authenticated():
        if has_admin(current_user):
            if request.method == 'POST':
                from models import Gallery, Image
                g = Gallery()
                g.title = request.form.get("gallery_title")
                g.slug = slugify(g.title)
                g.creator = current_user.id
                db.session.add(g)
                db.session.commit()
                if request.files:
                    f = request.files['file']
                    if f and allowed_file(f.filename):
                        path = save_file(f)
                        i = Image()
                        i.title = request.form.get("file_title")
                        i.url = "/uploads/" + path
                        i.creator = current_user.id
                        i.gallery = g.id
                        db.session.add(i)
                        db.session.commit()
                return g.slug
            else:
                return render_template("new_gallery.html")
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/uploads/<wrapper>/<filename>')
def uploaded_file(wrapper, filename):
    if wrapper == "fonts":
        #hack to stop uploaded bootstrap themes from failing to get fonts.
        return send_from_directory(os.path.realpath('.') + "/app/static/fonts/", filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "/" + wrapper + '/',
                               filename)

@app.route('/user_signup')
def user_signup():
    from models import Role, Section
    if current_user.is_authenticated():
        if has_admin(current_user):
            return render_template('user_signup.html', 
                                   roles=Role.query.all(), 
                                   sections=Section.query.all())
        else:
            abort(401)
    else:
        abort(401)

@app.route('/publish/<section_id>/<page_id>')
def publish_page(section_id, page_id):
    from models import Section, Page, EditRecord
    if current_user.is_authenticated():
        if can_publish(section_id):
            s = Section.query.filter_by(slug=section_id).first()
            p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
            if request.method == "GET":
                if (page_id == "_main"):
                    s.preview = False
                    db.session.add(s)
                p.preview = False
                db.session.add(p)
                db.session.commit()
                return redirect('/' + s.slug + "/" + p.slug)
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/unpublish/<section_id>/<page_id>')
def unpublish_page(section_id, page_id):
    from models import Section, Page, EditRecord
    if current_user.is_authenticated():
        if can_publish(section_id):
            s = Section.query.filter_by(slug=section_id).first()
            p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
            if request.method == "GET":
                if (page_id == "_main"):
                    s.preview = True
                    db.session.add(s)
                p.preview = True
                db.session.add(p)
                db.session.commit()
                return redirect('/' + s.slug + "/" + p.slug)
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/delete/<section_id>')
def delete_section(section_id):
    from models import Section, Page, User, permissions_users
    if current_user.is_authenticated():
        if has_admin(current_user):
            s = Section.query.filter_by(slug=section_id).first()
            for p in db.session.query(permissions_users).filter_by(permission_id=s.id):
                u = User.query.get(p.user_id)
                u.permissions.remove(s)
            db.session.commit()
            p = Page.query.filter_by(section=s.id).filter_by(slug="_main").first()
            p.deleted = True
            db.session.add(p)
            s.deleted = True
            db.session.add(s)
            db.session.commit()
            return redirect('/')
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/delete/<section_id>/<page_id>')
def delete_page(section_id, page_id):
    from models import Section, Page
    if current_user.is_authenticated():
        if has_admin(current_user):
            s = Section.query.filter_by(slug=section_id).first()
            p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
            p.deleted = True
            db.session.commit()
            return redirect('/')
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/edit/<section_id>/<page_id>', methods=['GET', 'POST'])
def edit_page(section_id, page_id):
    from models import Section, Page, EditRecord
    if current_user.is_authenticated():
        if can_edit(section_id):
            s = Section.query.filter_by(slug=section_id).first()
            p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
            if request.method == "GET":
                return render_template("edit_page.html", c=p, s=s)
            elif request.method == "POST":
                e = EditRecord ()
                e.previous_content = p.content
                e.new_content = request.form['content']
                e.editor = current_user.id
                e.time = datetime.datetime.now()
                e.page = p.id
                db.session.add(e)
                p.title = request.form['title']
                p.excerpt = request.form['excerpt']
                p.content = request.form['content']
                db.session.add(p)
                db.session.commit()
                return redirect('/' + s.slug + "/" + p.slug)
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/add_dynamic_page', methods=["GET", "POST"])
def add_dynamic_page():
    from models import Section, Gallery, Page, DynamicPage, PageComponent, Gallery
    if current_user.is_authenticated():
        if can_edit(request.args.get('section')):
            s = Section.query.filter_by(slug=request.args.get('section')).first()
            g = Gallery.query.all()
            if request.method == "GET":
                return render_template('add_dynamic_page.html', s=s, sections=Section.query.all(),galleries=g)
            elif request.method == "POST":
                dp = DynamicPage()
                db.session.add(dp)
                db.session.commit()
                p = Page()
                p.title = request.json.get("page_title")
                p.slug = slugify(request.json.get("page_title"))
                p.layout = "dynamic"
                p.author = current_user.id
                p.section = s.id
                p.dynamic_page_data = dp.id
                db.session.add(p)
                db.session.commit()
                order = 0
                for x in request.json.get('components'):
                    pc = PageComponent()
                    pc.page_container_id = dp.id
                    pc.order = order
                    order = order + 1
                    pc.component_type = x.get("type")
                    slgs = x.get('linked_slugs')
                    if slgs:
                        slgs = slgs.split("/")
                        slg_len = len(slgs)
                        if slg_len == 1:
                            sect = Section.query.filter_by(slug=slgs[0]).first()
                            pc.link_to_section_id = sect.id
                        if slg_len == 2:
                            sect = Section.query.filter_by(slug=slgs[0]).first()
                            pge = Page.query.filter_by(section=sect.id).filter_by(slug=slgs[1]).first()
                            pc.link_to_page_id = pge.id
                        if slg_len == 3:
                            pgph = Paragraph.query.get(int(slgs[2]))
                            pc.link_to_paragraph_id = pgph.id
                    gall = x.get("gallery")
                    if gall:
                        gal = Gallery.query.filter_by(slug=gall).first()
                        pc.gallery = gal
                    pc.href = x.get("link")
                    print pc.href
                    pc.text = x.get("text")
                    pc.title = x.get("title")
                    pc.second_text = x.get("second_text")
                    pc.second_title = x.get("second_title")
                    pc.third_text = x.get("third_text")
                    pc.third_title = x.get("third_title")
                    pc.fourth_text = x.get("fourth_text")
                    pc.fourth_title = x.get("fourth_title")
                    pc.second_href = x.get("second_href")
                    pc.third_href = x.get("third_href")
                    pc.fourth_href = x.get("fourth_href")
                    db.session.add(pc)
                    db.session.commit()
                return "/" + s.slug + "/" + p.slug

@app.route('/favicon.ico')
def return_404():
    return abort(404)

@app.route('/add_page', methods=['GET', 'POST'])
def add_page():
    from models import Section, Page, Gallery
    if current_user.is_authenticated():
        if can_edit(request.args.get('section')):
            s = Section.query.filter_by(slug=request.args.get('section')).first()
            if request.method == "GET":
                return render_template("add_page.html", s=s, galleries=Gallery.query.all())
            elif request.method == "POST":
                p = Page()
                p.slug = slugify(request.form.get('title'))
                p.title = request.form.get('title')
                p.excerpt = request.form.get('excerpt')
                p.layout = request.form.get('layout')
                p.author = current_user.id
                p.published = datetime.datetime.now()
                if request.files.get('source_document'):
                    if request.files.get('source_document').filename != '':
                        p.content = mammoth.convert_to_markdown(request.files['source_document'], 
                                                                convert_image=mammoth.images.inline(convert_image)).value
                else:
                    p.content = request.form.get('content')
                gallery_slug = request.form.get('gallery')
                if gallery_slug:
                    gal = Gallery.query.filter_by(slug=gallery_slug).first()
                    p.gallery = gal
                p.deleted = False
                s.pages.append(p)
                db.session.add(s)
                db.session.commit()
                return redirect("/" + s.slug + "/" + p.slug)
        else:
            return abort(401)
    else:
        return abort(401)

@app.route('/add_paragraph/<section_id>/<page_id>', methods=["GET", "POST"])
def add_paragraph(section_id, page_id):
    from models import Section, Page, Gallery, Participant, Tag, Paragraph
    if current_user.is_authenticated():
        if can_publish(current_user):
            s = Section.query.filter_by(slug=section_id).first()
            p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
            g = Gallery.query.all()
            t = Tag.query.all()
            if (request.method == "POST"):
                if s.section_type == "fundraiser":
                    par = Participant()
                    par.name = request.form.get("name")
                    relevant_gallery = Gallery.query.filter_by(slug=request.form.get("gallery")).first()
                    par.photos = relevant_gallery.id
                    par.bio = request.form.get("content")
                    par.goal = request.form.get("goal")
                    par.event = p.id
                    db.session.add(par)
                    db.session.commit()
                if s.section_type == "blog":
                    para = Paragraph()
                    para.title = request.form.get('title')
                    para.content = request.form.get('content')
                    para.author = current_user.id
                    para.slug = slugify(request.form.get('title'))
                    para.time = datetime.datetime.now()
                    if (request.form.get("gallery")):
                        galla = Gallery.query.filter_by(slug=request.form.get("gallery")).first()
                        para.photos = galla
                    for t in request.form.getlist('tag'):
                        ta = Tag.query.filter_by(slug=t).first()
                        para.tags.append(ta)
                    para.pages.append(p)
                    db.session.add(para)
                    db.session.commit()
                print s.section_type
                if s.section_type == "magazine":
                    pa = Paragraph()
                    pa.title = request.form.get('title')
                    pa.abstract = request.form.get('abstract')
                    pa.author = current_user.id
                    pa.slug = slugify(request.form.get('title'))
                    pa.time = datetime.datetime.now()
                    if request.files.get('source_document'):
                        if request.files.get('source_document').filename != '':
                            pa.content = mammoth.convert_to_markdown(request.files['source_document'], 
                                                                       convert_image=mammoth.images.inline(convert_image)).value
                    else:
                        pa.content = request.form.get('content')
                    print request.form.get('gallery')
                    if (request.form.get("gallery")):
                        galla = Gallery.query.filter_by(slug=request.form.get("gallery")).first()
                        pa.photos = galla.id
                    for t in request.form.getlist('tag'):
                        ta = Tag.query.filter_by(slug=t).first()
                        pa.tags.append(ta)
                    pa.pages.append(p)
                    db.session.add(pa)
                    db.session.commit()
                return redirect("/" + section_id + "/" + page_id)
            else:
                if (s.section_type == "fundraiser"):
                    return render_template("add_participant.html", galleries=g, s=s, p=p)
                elif (s.section_type == "blog"):
                    return render_template("add_blog_post.html", galleries=g, tags=t, s=s, p=p)
                elif (s.section_type == "magazine"):
                    return render_template("add_article.html", galleries=g, tags=t, s=s, p=p)
                else:
                    return "Section type does not support paragraphs"

@app.route('/add_section', methods=["GET", "POST"])
def add_section():
    from models import Role, User, Section, Page, EditRecord
    if current_user.is_authenticated():
        if has_admin(current_user):
            if (request.method == "POST"):
                permish = []
                for d in request.form:
                    if str(d).startswith("user_permissions"):
                        permish.append(int(request.form.get(d)))
                s = Section()
                s.slug = slugify(request.form['title'])
                s.title = request.form['title']
                s.description = request.form['description']
                s.creator = current_user.id
                s.section_type = request.form.get('section_type')
                if request.files:
                    if request.files['css'].filename != '':
                        css = request.files['css']
                        s.css = '/uploads/' + save_file(css)
                    if request.files['logo'].filename != '':
                        logo = request.files['logo']
                        s.logo = '/uploads/' + save_file(logo)
                db.session.add(s)
                db.session.commit()
                for u in permish:
                    user = User.query.get(u)
                    user.permissions.append(s)
                p = Page()
                p.slug = "_main"
                p.title = request.form['title']
                p.excerpt = request.form['description']
                p.author = current_user.id
                p.published = datetime.datetime.now()
                p.section = s.id
                p.content = request.form['content']
                p.deleted = False
                db.session.add(p)
                db.session.commit()
                return redirect("/" + s.slug)
            elif (request.method == "GET"):
                return render_template('add_section.html', users=User.query.all())
        else:
            abort(401)
    else:
        abort(401)

@app.route('/')
def index():
    from models import Section, Page
    s = Section.query.filter_by(slug=app.config['MAIN_SECTION']).first()
    p = Page.query.filter_by(section=s.id).filter_by(slug="_main").first()
    return render_template(p.layout + '.html', c=p, s=s, content=Markup(p.content))

@app.route('/add_comment/<section_id>/<page_id>/<paragraph_id>', methods=["POST"])
def add_comment(section_id, page_id, paragraph_id):
    from models import Comment, Paragraph
    if current_user.is_authenticated():
        para = Paragraph.query.get(int(paragraph_id))
        c = Comment()
        c.title = request.form.get('title')
        c.comment = request.form.get('comment')
        c.time = datetime.datetime.now()
        c.author = current_user.id
        c.paragraph = para.id
        db.session.add(c)
        db.session.commit()
        return redirect("/" + section_id + "/" + page_id + "/" + paragraph_id)

@app.route('/<unstatic:section_id>')
@app.route('/<unstatic:section_id>/<page_id>')
@app.route('/<unstatic:section_id>/<page_id>/<paragraph_id>')
def section_page(section_id, page_id="_main", paragraph_id=None):
    from models import Role, User, Section, Page, EditRecord, Participant, Paragraph
    s = Section.query.filter_by(slug=section_id).first()
    p = Page.query.filter_by(section=s.id).filter_by(slug=page_id).first()
    layout = "content"
    if p.layout != None:
        layout = p.layout
    elif s.section_type != None:
        layout = s.section_type
    if s.section_type == "blog":
        if page_id == "_main":
            layout = "blog_group"
    if paragraph_id:
        # Paragraphs are a third tier for blog posts, magazine articles, 
        # and fundraising participants. Here we have to deal with it.
        if s.section_type == 'fundraiser':
            part = Participant.query.get(int(paragraph_id))
            return render_template("participant.html", c=p, s=s, p=part)
        elif s.section_type == 'blog':
            post = Paragraph.query.get(int(paragraph_id))
            return render_template("blog_post.html", c=p, s=s, post=post)
        elif s.section_type == "magazine":
            post = Paragraph.query.get(int(paragraph_id))
            return render_template("article.html", c=p, s=s, a=post)
    else:
        return render_template(layout + '.html', c=p, s=s, content=Markup(p.content))

# Restful Resources

import resources
api.add_resource(resources.NewUser, '/api/new_user')
api.add_resource(resources.Login, '/api/login')
api.add_resource(resources.NewGallery, '/api/gallery')
api.add_resource(resources.Donate, '/api/donate/<int:part>')
api.add_resource(resources.AddTag, '/api/tag')

class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated():
            if "admin" in [ x.name for x in current_user.roles]:
                return True
            else:
                return False
        else:
            return False

# Admin Views

admin.add_view(AdminView(models.User, db.session))
admin.add_view(AdminView(models.Role, db.session))
admin.add_view(AdminView(models.Section, db.session))
admin.add_view(AdminView(models.Page, db.session))
admin.add_view(AdminView(models.EditRecord, db.session))
admin.add_view(AdminView(models.Gallery, db.session))
admin.add_view(AdminView(models.Image, db.session))
admin.add_view(AdminView(models.Participant, db.session))
admin.add_view(AdminView(models.Paragraph, db.session))
admin.add_view(AdminView(models.DynamicPage, db.session))
admin.add_view(AdminView(models.PageComponent, db.session))
admin.add_view(AdminView(models.Tag, db.session))

def slugify(s):
    return re.sub('[^0-9a-zA-Z]+', '_', s)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def save_file(f):
    if f:
        filename = "".join(i for i in f.filename if i not in "\/:*?<>|")
        h = base64.urlsafe_b64encode(hashlib.sha1(datetime.datetime.now().ctime()).digest() + ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)]))
        os.makedirs(app.config['UPLOAD_FOLDER'] + h + "/")
        f.save(os.path.join(app.config['UPLOAD_FOLDER'] + h + "/", filename))
        return h + "/" + filename
    else:
        return "NONONONONNONN"

def convert_image(image):
    # an image conversion function for use with Mammoth in markdown conversion
    with image.open() as image_bytes:
        h = base64.urlsafe_b64encode(hashlib.sha1(datetime.datetime.now().ctime()).digest() + ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)]))
        os.makedirs(app.config['UPLOAD_FOLDER'] + h + "/")
        f = open(os.path.join(app.config['UPLOAD_FOLDER'] + h + "/", "image" + mimetypes.guess_extension(image.content_type)), "wb")
        f.write(image_bytes.read())
        f.close()
        return {
            "src": "/uploads/" + h + "/image" + mimetypes.guess_extension(image.content_type)
        }
