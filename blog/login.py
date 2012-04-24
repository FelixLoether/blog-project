from flask import session, request, redirect, url_for, g, render_template, \
        flash
from blog import app, db
from users import User


@app.errorhandler(403)
def require_login(error):
    session['redirect-to'] = request.url
    flash('You need to be logged in to view that content.', 'error')
    return redirect(url_for('login')), 403


@app.before_request
def load_user():
    g.user = None

    if 'user-id' in session:
        try:
            g.user = db.session.query(User).\
                    filter_by(id=session['user-id']).one()
        except db.NoResultFound:
            app.logger.error("Session's user id \"%s\" does not exist",
                    session['user-id'])


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    try:
        user = db.session.query(User).filter_by(name=username).one()
    except db.NoResultFound:
        flash('Invalid username or password.', 'error')
        app.logger.info('Trying to log in with nonexisting user: %s',
                username)
        return redirect(url_for('login'))

    if not user.verify(password):
        flash('Invalid username or password.', 'error')
        app.logger.info('Login for %s (%d) failed.', user.name, user.id)
        return redirect(url_for('login'))

    url = session.pop('redirect-to', url_for('index'))
    session['user-id'] = user.id
    app.logger.info('User %s (%d) logged in successfully.',
            user.name, user.id)
    flash('You have logged in.', 'success')
    return redirect(url)


@app.route('/logout')
def logout():
    session.pop('user-id', None)
    flash('You have logged out.', 'success')
    return redirect(url_for('index'))
