from app import app, db, api, user_datastore, security
from flask import request
from flask.ext.restful import abort, marshal, marshal_with, fields, Resource
from models import *
from flask.ext.security.utils import encrypt_password, login_user
from flask.ext.security.confirmable import send_confirmation_instructions
import json, datetime

class NewUser(Resource):
    def post(self):
        usr = json.loads(request.data)
        user = user_datastore.create_user(first_name=usr['first_name'],
                                          last_name=usr['last_name'],
                                          email=usr['email'],
                                          password=encrypt_password(usr['password']))
        for r in usr['roles']:
            user_datastore.add_role_to_user(user, str(r))
        db.session.add(user)
        db.session.commit()
        token = send_confirmation_instructions(user) 
        return True
        
class Login(Resource):
    #a stub for login restful. Might work.
    def post(self):
        data = json.loads(request.data)
        usr = User.query.filter_by(email=data['email'])
        if not usr is None:
            if usr.password == encrypt_password(data['password']):
                login_user(user)
        return True
                
