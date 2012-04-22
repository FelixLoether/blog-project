import os
from flask import Flask, g, render_template, flash
from flask.ext.markdown import Markdown

app = Flask(__name__)
Markdown(app, safe_mode=True)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

import timesince
import logger
import db
from users import User
import login
import posts

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

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
