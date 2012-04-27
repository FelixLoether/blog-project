from blog import app, db, create_token, validate_token
from blog.comments import Comment
from blog.posts import get_post
from flask import Blueprint, abort, flash, render_template, request, \
        session, url_for, redirect, g, jsonify

blueprint = Blueprint('comments', __name__)


def get_comment(id):
    try:
        return db.session.query(Comment).filter_by(id=id).one()
    except db.NoResultFound:
        app.logger.warning('Requested invalid comment: "%s".', id)
        flash('That comment does not exist.', 'error')
        abort(404)


def preprocess(comment, post, edit=False, delete=False):
    if request.method == 'GET':
        session['token'] = create_token()

        if delete:
            return render_template('comments/delete.html', comment=comment)

        return render_template('comments/edit.html', comment=comment,
                post=post, edit=edit)

    if not delete:
        if not request.form['content']:
            if g.json:
                return jsonify(status='error',
                        message='You need to add some content.')
            flash('You need to add some content.', 'error')
            return render_template('comments/edit.html', comment=comment,
                    post=post, edit=edit)

    if not validate_token():
        if g.json:
            return jsonify(status='error', try_without_js=True)

        if delete:
            return redirect(url_for('comments.delete', id=comment.id))

        session['token'] = create_token()
        return render_template('comments/edit.html', comment=comment,
                post=post, edit=edit)

    return None


@blueprint.route('/<int:id>')
def show(id):
    comment = get_comment(id)
    return render_template('comments/show.html', comment=comment)


@blueprint.route('/create', methods=['POST'])
def create():
    try:
        post_id = int(request.form['post_id'])
    except ValueError:
        abort(400)

    post = get_post(post_id)

    if g.user:
        comment = Comment(request.form['content'], post, user=g.user)
    else:
        comment = Comment(request.form['content'], post,
                username=request.form['username'])
        if not request.form['username']:
            if g.json:
                return jsonify(status='error',
                        message='You have to add a name.')
            flash('You have to add a name.', 'error')
            session['token'] = create_token()
            return render_template('comments/edit.html', comment=comment,
                    post=post, edit=False)

    res = preprocess(comment, post=post)
    if res:
        return res

    db.session.add(comment)
    db.session.commit()
    app.logger.info('Created comment %d', comment.id)

    if g.json:
        return jsonify(status='success', message='Comment added.',
            token=create_token())

    flash('Comment created.', 'success')
    return redirect(url_for('posts.show', id=post_id))


@blueprint.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not g.user:
        abort(403)

    comment = get_comment(id)

    res = preprocess(comment, edit=True, post=comment.post)
    if res:
        return res

    if 'username' in request.form and request.form['username']:
        comment.username = request.form['username']

    comment.content = request.form['content']
    db.session.commit()
    app.logger.info('Edited comment %d.', comment.id)

    if g.json:
        return jsonify(status='success', message='Comment edited',
            token=create_token())

    flash('Comment edited successfully.', 'success')
    return redirect(url_for('posts.show', id=comment.post.id))


@blueprint.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    if not g.user:
        abort(403)

    comment = get_comment(id)

    res = preprocess(comment, delete=True, post=comment.post)
    if res:
        return res

    if request.form['action'] != 'delete':
        return redirect(url_for('posts.show', id=comment.post.id))

    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()

    if g.json:
        return jsonify(status='success', message='Comment deleted',
            token=create_token())

    flash('Comment deleted!', 'success')
    return redirect(url_for('posts.show', id=post_id))
