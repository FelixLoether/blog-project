from blog import app, db, create_token, validate_token
from blog.posts import Post, paginate, get_post
from blog.tags import Tag, prepare_tag_name
from flask import Blueprint, abort, render_template, request, redirect, \
    url_for, g, flash, session

blueprint = Blueprint('posts', __name__)


@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/page-<int:page>')
def list(page):
    res = paginate(db.session.query(Post).order_by(Post.id.desc()), page)

    if len(res['posts']) == 0:
        flash("We don't have that many posts.", 'error')
        abort(404)

    return render_template('posts/list.html', page=page, **res)


def get_tags(tag_names):
    tags = []
    for name in tag_names:
        try:
            tags.append(db.session.query(Tag).filter_by(name=name).one())
        except db.NoResultFound:
            app.logger.warning('Trying to get invalid tag: "%s".', name)
            flash('Tag "{0}" does not exist.'.format(name), 'error')
            return None

    return tags


@blueprint.route('/<int:id>')
def show(id):
    post = get_post(id)
    session['token'] = create_token()
    return render_template('posts/show.html', post=post)


def preprocess(post, edit):
    if request.method == 'GET':
        session['token'] = create_token()
        return render_template('posts/edit.html', post=post, edit=edit), None

    req_tags = request.form['tags']
    req_tags = map(prepare_tag_name, req_tags.split())
    tags = get_tags(req_tags)
    req_tags = ' '.join(req_tags)

    if request.form['action'] == 'preview':
        p = Post(request.form['title'], request.form['content'], g.user)
        p.id = post.id if post else -1
        return render_template('posts/edit.html', post=p, preview=True,
                edit=edit, tags=req_tags), None

    if tags is None:
        return render_template('posts/edit.html', post=post, edit=edit,
                tags=req_tags), None

    if not validate_token():
        flash('Tokens did not match. Try again.', 'error')

        if edit:
            return redirect(url_for('posts.edit', id=post.id)), None
        else:
            return redirect(url_for('posts.create')), None

    return None, tags


@blueprint.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not g.user:
        abort(403)

    post = get_post(id)

    res, tags = preprocess(post, True)
    if res:
        return res

    post.title = request.form['title']
    post.content = request.form['content']
    post.tags = tags
    db.session.commit()
    app.logger.info('Edited post %d', post.id)
    flash('Post edited successfully.', 'success')
    return redirect(url_for('posts.show', id=post.id))


@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if not g.user:
        abort(403)

    res, tags = preprocess(None, False)
    if res:
        return res

    post = Post(request.form['title'], request.form['content'], g.user)
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    app.logger.info('Created post %d', post.id)
    flash('Post created.', 'success')
    return redirect(url_for('posts.show', id=post.id))


@blueprint.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    if not g.user:
        abort(403)

    post = get_post(id)

    if request.method == 'GET':
        session['token'] = create_token()
        return render_template('posts/delete.html', post=post)

    if not validate_token():
        return redirect(url_for('posts.delete', id=post.id))

    if request.form['action'] != 'delete':
        return redirect(url_for('posts.show', id=post.id))

    app.logger.info('Deleting post %d', post.id)

    for comment in post.comments:
        db.session.delete(comment)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'success')
    return redirect(url_for('index'))

app.register_blueprint(blueprint)
