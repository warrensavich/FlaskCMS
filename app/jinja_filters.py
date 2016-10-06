import markdown
from flask import Markup
from flask.ext.login import current_user

def has_admin(usr):
    if "admin" in [r for r in usr.roles]:
        return True
    else: 
        return False

def can_edit(slug):
    from models import Section, Page
    s = Section.query.filter_by(slug=slug).first()
    if has_admin(current_user):
        return True
    if "contributer" in [r for r in current_user.roles]:
        if s.id in [s for s in current_user.permissions]:
            return True
        else:
            return False
    else:
        return False

def can_publish(slug):
    from models import Section, Page
    s = Section.query.filter_by(slug=slug).first()
    if has_admin(current_user):
        return True
    if "editor" in [r for r in current_user.roles]:
        if s.id in [s for s in current_user.permissions]:
            return True
        else:
            return False
    else:
          return False  

def wiki_markup(s):
    return Markup(markdown.markdown(s))

def defined(var):
    if var:
        if var != None:
            return True
        else:
            return False
    else:
        return False

def currency(value, decimal_offset=1.0):
    return "{:,.2f}".format(int(value)/decimal_offset)

def truncate_number(value):
    return "{:.1f}".format(value)

def date_format(date, fmt="%b. %d, %Y"):
    return date.strftime(fmt)

def register_filters(env):
    env['date'] = date_format
    env['currency'] = currency
    env['truncate_number'] = truncate_number
    env['has_admin'] = has_admin
    env['markdown'] = wiki_markup
    env['can_edit'] = can_edit
    env['can_publish'] = can_publish
    env['defined'] = defined
    return env
