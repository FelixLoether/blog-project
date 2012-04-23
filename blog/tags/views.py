from blog import app, db, create_token, validate_token
from blog.tags import Tag, prepare_tag_name
from flask import Blueprint, abort, render_template, request, redirect, \
    url_for, g, flash, session

blueprint = Blueprint('tags', __name__)

@blueprint.route('/')
def list():
    tags = db.session.query(Tag).order_by(Tag.name).all()
    return render_template('tags/list.html', tags=tags)

def get_tag(id):
    try:
        return db.session.query(Tag).filter_by(id=id).one()
    except db.NoResultFound:
        app.logger.info('Nonexisting tag requested: %d', id)
        flash('That tag does not exist.', 'error')
        abort(404)

@blueprint.route('/<int:id>')
def show(id):
    tag = get_tag(id)
    return render_template('tags/show.html', tag=tag)

def preprocess(tag, edit):
    if request.method == 'GET':
        session['token'] = create_token()
        return render_template('tags/edit.html', tag=tag, edit=edit)

    if not validate_token():
        if edit:
            return redirect(url_for('tags.edit', id=tag.id))
        else:
            return redirect(url_for('tags.create'))

    return None

@blueprint.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if not g.user:
        abort(403)

    tag = get_tag(id)

    res = preprocess(tag, True)
    if res:
        return res

    tag.name = prepare_tag_name(request.form['name'])
    db.session.commit()
    app.logger.info('Tag edited: %d', tag.id)
    flash('Tag edited successfully.', 'success')
    return redirect(url_for('tags.show', id=tag.id))

@blueprint.route('/create', methods=('GET', 'POST'))
def create():
    if not g.user:
        abort(403)

    res = preprocess(None, False)
    if res:
        return res

    tag = Tag(request.form['name'])
    db.session.add(tag)
    db.session.commit()
    app.logger.info('Tag created: %d', tag.id)
    flash('Tag created successfully.', 'success')
    return redirect(url_for('tags.show', id=tag.id))

@blueprint.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    if not g.user:
        abort(403)

    tag = get_tag(id)

    if request.method == 'GET':
        session['token'] = create_token()
        return render_template('tags/delete.html', tag=tag)

    if not validate_token():
        return redirect(url_for('tags.delete', id=tag.id))

    if request.form['action'] != 'delete':
        return redirect(url_for('tags.show', id=tag.id))

    app.logger.info('Deleting tag %d', tag.id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted!', 'success')
    return redirect(url_for('index'))

app.register_blueprint(blueprint, url_prefix='/tags')
