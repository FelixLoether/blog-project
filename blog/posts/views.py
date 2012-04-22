from blog import app, db
from blog.posts import Post
from flask import Blueprint, abort, render_template, request, redirect, \
    url_for, g, flash
import math

blueprint = Blueprint('posts', __name__)

@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/page-<int:page>')
def list(page):
    if page <= 0:
        abort(404)

    start = (page - 1) * app.config['POSTS_PER_PAGE']
    end = page * app.config['POSTS_PER_PAGE']

    posts = db.session.query(Post).order_by(Post.id.desc())[start:end]

    if len(posts) == 0:
        flash("We don't have that many posts here.", 'error')
        abort(404, 'woot')

    max_page = int(math.ceil(
        db.session.query(Post).count() / float(app.config['POSTS_PER_PAGE'])))

    num = app.config['NAVIGATION_PAGE_COUNT'] / 2
    pages = [p for p in xrange(page - num, page + num + 1) if 1 < p < max_page]

    return render_template('posts/list.html', posts=posts, page=page,
            pages=pages, max_page=max_page)

def get_post(post_id):
    try:
        return db.session.query(Post).filter_by(id=post_id).one()
    except db.NoResultFound:
        app.logger.warning('Requested invalid post: "%s".', post_id)
        flash('That post does not exist.', 'error')
        abort(404)

@blueprint.route('/<int:id>')
def show(id):
    post = get_post(id)
    return render_template('posts/show.html', post=post)

@blueprint.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not g.user:
        abort(403)

    post = get_post(id)

    if request.method == 'GET':
        return render_template('posts/edit.html', post=post)

    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    flash('Post edited successfully.', 'success')
    return redirect(url_for('posts.show', id=post.id))

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if not g.user:
        abort(403)

    if request.method == 'GET':
        return render_template('posts/edit.html', post=None)

    post = Post(request.form['title'], request.form['content'], g.user)
    db.session.add(post)
    db.session.commit()
    flash('Post created.', 'success')
    return redirect(url_for('posts.show', id=post.id))

app.register_blueprint(blueprint)
