import os
from flask import Flask, flash, request, session
from flask.ext.markdown import Markdown

app = Flask(__name__)
Markdown(app, safe_mode=True)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

def create_token(length=32):
    # Take random bytes from os.urandom, turn them into hexadecimals, and join
    # the result to one string.
    return ''.join(map(lambda x: '{0:02x}'.format(ord(x)), os.urandom(length)))

def validate_token():
    if request.form['token'] != session.pop('token', None):
        app.logger.info('Token does not exist: %s', request.form['token'])
        flash('Tokens did not match. Try again.', 'error')
        return False
    return True

import timesince
import logger
import db
import users
import login
import posts
import tags

app.add_url_rule('/', 'index', 'posts.list', defaults={'page': 1})

@app.template_filter()
def plural(num, a, b=None):
    if b is None:
        singular = ''
        plural = a
    else:
        singular = a
        plural = b

    return singular if num == 1 else plural

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def install(username, password):
    if app.config['DATABASE_PATH'] is not None:
        if os.path.exists(app.config['DATABASE_PATH']):
            confirm = raw_input(
                'A database already exists. Remove it? [y/N] ').lower()

            if confirm != 'y':
                print 'Aborting install.'
                return

            app.logger.warning('Removing database.')

    db.init_db()
    admin = users.User(username, password)
    db.session.add(admin)
    db.session.commit()

def run():
    app.run(host=app.config['HOST'], port=app.config['PORT'])
