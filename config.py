import os

DEBUG = True
TESTING = True
PROPOGATE_EXCEPTIONS = True

VERSION = 1.0
NAME= "Skotia CMS"

MAIN_SECTION = "main"

SQLALCHEMY_DATABASE_URI="mysql://root@localhost/dtf"
#SQLALCHEMY_DATABASE_URI="mysql://b8b5c9dd408c57:13a951af@us-cdbr-iron-east-01.cleardb.net/heroku_faa3b643a2d26ee"

UPLOAD_FOLDER=os.path.realpath('..') + "/uploads/"
ALLOWED_EXTENSIONS=set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'css'])

SECRET_KEY="warrenisthebest"
SECURITY_PASSWORD_HASH="bcrypt"
SECURITY_PASSWORD_SALT="warrenisreallythebest"
SECURITY_UNAUTHORIZED_VIEW="/forbidden"
SECURITY_REGISTER_USER_TEMPLATE="user_signup.html"
SECURITY_SEND_REGISTER_EMAIL=True
SECURITY_REGISTERABLE=True
SECURITY_CONFIRMABLE=True
SECURITY_POST_CONFIRM_VIEW="/confirmed"

MAIL_SERVER="smtp.sendgrid.net"
MAIL_PORT=587
MAIL_DEBUG=True
MAIL_USERNAME="wsavich"
MAIL_PASSWORD="treetrunks1"
MAIL_SUPPRESS_SEND=False
MAIL_DEFAULT_SENDER="wsavich@outlook.com"
