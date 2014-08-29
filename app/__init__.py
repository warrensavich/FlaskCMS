import config
import json
import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, RoleMixin, UserMixin
from flask.ext.restful import abort, marshal, marshal_with, fields, Resource
from flask_mail import Mail
from flask.ext.restful import Api
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from sqlalchemy import func
from flask.ext.principal import Principal
from flask.ext.security.signals import user_registered

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
api = Api(app)
admin = Admin(app)
principals = Principal(app)

from flask_security.forms import RegisterForm, TextField, Required

class ExtendedRegisterForm(RegisterForm):
    first_name = TextField('First Name', [Required()])
    last_name = TextField('Last Name', [Required()])

import models
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("user")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

# Views

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/user_signup')
def user_signup():
    return render_template('user_signup.html')

@app.route('/confirmed')
@login_required
def confirmed():
    return render_template('confirmed.html')

@app.route('/application')
@login_required
def application():
    return render_template('application.html')

# Restful Resources

import resources
api.add_resource(resources.NewUser, '/api/new_user')

# Admin Views

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Role, db.session))
