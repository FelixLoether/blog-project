import os
import math
from flask import Flask, g, render_template, flash, redirect, url_for, \
        request, session, abort
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

def paginate(query, page):
    result = {}

    if page <= 0:
        abort(404)

    num = app.config['NAVIGATION_PAGE_COUNT'] / 2
    ppp = app.config['POSTS_PER_PAGE']
    start = (page - 1) * ppp
    end = start + ppp

    result['posts'] = posts = query[start:end]
    result['max_page'] = max_page = int(math.ceil(query.count() / float(ppp)))
    result['pages'] = [p for p in xrange(page - num, page + num + 1)
            if 1 < p < max_page]

    if len(posts) == 0:
        flash("We don't have that many posts.", 'error')
        abort(404)

    return result

import timesince
import logger
import db
from users import User
import login
import posts
import tags

app.add_url_rule('/', 'index', 'posts.list', defaults={'page': 1})

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
