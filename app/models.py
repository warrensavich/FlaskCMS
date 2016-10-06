from app import db
from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy import func
import pdb

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

permissions_users = db.Table('permissions_users',
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('permission_id', db.Integer(), db.ForeignKey('section.id')))

tags_pages = db.Table('tags_pages',
                      db.Column('page_id', db.Integer(), db.ForeignKey('page.id')),
                      db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')))

tags_paragraphs = db.Table('tags_paragraphs',
                           db.Column('paragraph_id', db.Integer(), db.ForeignKey('paragraph.id')),
                           db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')))

pages_paragraphs = db.Table('pages_paragraphs',
                            db.Column('page_id', db.Integer(), db.ForeignKey('page.id')),
                            db.Column('paragraph_id', db.Integer(), db.ForeignKey('paragraph.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    permissions = db.relationship('Section', secondary=permissions_users, 
                                  backref=db.backref('usrs', lazy='dynamic'))
    experiences = db.Column(db.Text())
    most_interested = db.Column(db.Text())
    preferred_resource = db.Column(db.Text())
    company = db.Column(db.String(255))
    def __str__(self):
        return self.first_name + " " + self.last_name

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship('Image', backref=db.backref('galleries'))
    preview = db.Column(db.Boolean(), default=True)
    def __str__(self):
        return self.title

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    alt_text = db.Column(db.Text())
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    preview = db.Column(db.Boolean(), default=True)
    gallery = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    order = db.Column(db.Integer)
    url = db.Column(db.String(255), unique=True)
    link = db.Column(db.String(512))
    created = db.Column(db.DateTime())
    deleted = db.Column(db.Boolean(), default= False)
    def __str__(self):
        if self.title:
            return self.title
        else:
            return "no title"

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    preview = db.Column(db.Boolean(), default=True)
    section_type = db.Column(db.Enum('content', 'blog', 'magazine', 'fundraiser'), default="content")
    title = db.Column(db.String(511))
    description = db.Column(db.Text())
    order = db.Column(db.Integer)
    theme = db.Column(db.String(255))
    css = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    deleted = db.Column(db.Boolean(), default=False)
    pages = db.relationship('Page', backref=db.backref('sections'))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __str__(self):
        return self.title

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255))
    preview = db.Column(db.Boolean(), default=True)
    title = db.Column(db.String(511))
    excerpt = db.Column(db.Text())
    content = db.Column(db.Text())
    published = db.Column(db.DateTime())
    fundraiser_end_time = db.Column(db.DateTime())
    participants = db.relationship('Participant', backref=db.backref('page'))
    deleted = db.Column(db.Boolean(), default=False)
    updated = db.Column(db.DateTime())
    layout = db.Column(db.String(255))
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    gallery = db.relationship('Gallery', uselist=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    section = db.Column(db.Integer, db.ForeignKey('section.id'))
    section_obj = db.relationship('Section', uselist=False)
    dynamic_page_data = db.Column(db.Integer, db.ForeignKey('dynamic_page.id'))
    dynamic_page = db.relationship('DynamicPage', uselist=False)
    tags = db.relationship('Tag',
                           secondary=tags_pages,
                           back_populates='pages')
    paragraphs = db.relationship('Paragraph', secondary=pages_paragraphs,
                                 back_populates="pages")
    __table_args__ = (db.UniqueConstraint('section', 'slug', name='_section_slug_uc'),
                     )
    def __str__(self):
        return self.title

class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    title = db.Column(db.String(255))
    abstract = db.Column(db.Text())
    slug = db.Column(db.String(255), unique=True)
    time = db.Column(db.DateTime())
    photos = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    gallery = db.relationship('Gallery', uselist=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    writer = db.relationship('User', uselist=False)
    layout = db.Column(db.Enum('content'))
    comments = db.relationship('Comment')
    pages = db.relationship('Page', 
                            secondary=pages_paragraphs, 
                            back_populates="paragraphs")
    tags = db.relationship('Tag',
                           secondary=tags_paragraphs,
                           back_populates='paragraphs')
    def __str__(self):
        return self.title

class DynamicPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    components = db.relationship('PageComponent')

class PageComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_container_id = db.Column(db.Integer, db.ForeignKey('dynamic_page.id'))
    order = db.Column(db.Integer)
    component_type = db.Column(db.String(255))
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    gallery = db.relationship('Gallery', uselist=False)
    title = db.Column(db.Text)
    text = db.Column(db.Text)
    second_text = db.Column(db.Text)
    second_title = db.Column(db.Text)
    third_text = db.Column(db.Text)
    third_title = db.Column(db.Text)
    fourth_text = db.Column(db.Text)
    fourth_title = db.Column(db.Text)
    href = db.Column(db.String(512))
    second_href = db.Column(db.String(512))
    third_href = db.Column(db.String(512))
    fourth_href = db.Column(db.String(512))
    link_to_section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    linked_section = db.relationship('Section')
    link_to_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    linked_page = db.relationship('Page')
    link_to_paragraph_id = db.Column(db.Integer, db.ForeignKey('paragraph.id'))
    linked_paragraph = db.relationship('Paragraph')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    title = db.Column(db.String(512))
    time = db.Column(db.DateTime())
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    paragraph = db.Column(db.Integer, db.ForeignKey('paragraph.id'))

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(511))
    photos = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    gallery = db.relationship('Gallery', uselist=False)
    bio = db.Column(db.Text())
    goal = db.Column(db.Integer())
    donation_count = db.Column(db.Integer(), default=0)
    current_progress = db.Column(db.Integer(), default=0)
    event = db.Column(db.Integer, db.ForeignKey('page.id'))
    def __str__(self):
        return self.name

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255))
    pages = db.relationship('Page',
                            secondary=tags_pages,
                            back_populates="tags")
    paragraphs = db.relationship('Paragraph',
                                 secondary=tags_paragraphs,
                                 back_populates='tags')

class EditRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime())
    editor = db.Column(db.Integer, db.ForeignKey('user.id'))
    previous_content = db.Column(db.Text())
    new_content = db.Column(db.Text())
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    page = db.Column(db.Integer, db.ForeignKey('page.id'))
    def __str__(self):
        return self.page
    
    
