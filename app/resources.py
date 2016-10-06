from app import app, db, api, user_datastore, security
from flask import request
from flask.ext.restful import abort, marshal, marshal_with, fields, Resource
from models import *
from flask.ext.security.utils import encrypt_password, verify_password, login_user
from flask.ext.security.confirmable import send_confirmation_instructions
from flask.ext.security.recoverable import generate_reset_password_token, send_reset_password_instructions, reset_password_token_status, update_password
from flask.ext.login import current_user
import json, datetime, re

class Donate(Resource):
    def get(self, part):
        p = Participant.query.get(part)
        p.current_progress = p.current_progress + 5
        p.donation_count = p.donation_count + 1
        db.session.add(p)
        db.session.commit()

class NewUser(Resource):
    def post(self):
        from models import User, Section
        usr = request.json
        email = usr.get('email')
        if email is None:
            return abort(500)
        user = user_datastore.create_user(first_name=usr.get('first_name'),
                                          last_name=usr.get('last_name'),
                                          email=email)
        if current_user.is_authenticated():
            if ("admin" in [r for r in current_user.roles]):
                for r in usr.get('roles', []):
                    user_datastore.add_role_to_user(user, r)
                user.permissions = [Section.query.get(int(p)) for p in usr.get('permissions', [])]
        user.experiences = ",".join(usr.get('experiences', []))
        user.most_interested = usr.get('most_interested')
        user.preferred_resource = usr.get('preferred_resource')
        user.company = usr.get('company')
        db.session.add(user)
        db.session.commit()
        return True
        
class Login(Resource):
    #a stub for login restful. Might work.
    def post(self):
        data = request.json
        usr = User.query.filter_by(email=data['email']).first()
        if not usr is None:
            if verify_password(data['password'], usr.password):
                login_user(usr)
            else: 
                return False
        else:
            abort(400)
        return True

class AddTag(Resource):
    def post(self):
        if current_user.is_authenticated():
            if ("contributer" in [r for r in current_user.roles]) or ("admin" in [r for r in current_user.roles]):
                t = Tag()
                t.title = request.json.get('title')
                t.slug = slugify(request.json.get('title'))
                db.session.add(t)
                db.session.commit()
                return {'slug': t.slug, 'title': t.title}
                
class NewGallery(Resource):
    def post(self):
        g = Gallery()
        g.title = request.json.get("gallery_title")
        g.slug = slugify(g.title)
        g.creator = current_user.id
        db.session.add(g)
        db.session.commit()
        return g.slug

def slugify(s):
    return re.sub('[^0-9a-zA-Z]+', '_', s)
