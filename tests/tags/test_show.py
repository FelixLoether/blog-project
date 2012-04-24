from blog import db
from blog.tags import Tag


def test_show_tag(tagsetup):
    r = tagsetup.app.get('/tags/1')

    assert r.status_code == 200
    assert 'Tag test' in r.data
    tagsetup.done()


def test_cannot_show_nonexisting_tag(tagsetup):
    r = tagsetup.app.get('/tags/2')

    assert r.status_code == 404
    assert 'That tag does not exist.' in r.data
    tagsetup.done()


def test_show_tag_post_count(tagsetup):
    t = db.session.query(Tag).first()
    r = tagsetup.app.get('/tags/1')
    assert 'no posts.' in r.data

    p = tagsetup.create_post()
    p.tags.append(t)
    r = tagsetup.app.get('/tags/1')
    assert '1 post.' in r.data

    p = tagsetup.create_post()
    p.tags.append(t)
    r = tagsetup.app.get('/tags/1')
    assert '2 posts.' in r.data

    tagsetup.done()


def test_anonymous_cannot_view_edit_link(tagsetup):
    r = tagsetup.app.get('/tags/1')
    assert '/tags/1/edit' not in r.data
    tagsetup.done()


def test_admin_can_view_edit_link(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1')
    assert '/tags/1/edit' in r.data
    tagsetup.done()


def test_anonymous_cannot_view_delete_link(tagsetup):
    r = tagsetup.app.get('/tags/1')
    assert '/tags/1/delete' not in r.data
    tagsetup.done()


def test_admin_can_view_delete_link(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1')
    assert '/tags/1/delete' in r.data
    tagsetup.done()
