def test_show_post(postsetup):
    r = postsetup.app.get('/1')
    assert r.status_code == 200
    assert 'Title' in r.data
    assert 'the content of the post' in r.data
    postsetup.done()


def test_cannot_view_nonexisting_post(postsetup):
    r = postsetup.app.get('/2')
    assert r.status_code == 404
    assert 'That post does not exist.' in r.data
    postsetup.done()


def test_anonymous_cannot_view_edit_link(postsetup):
    r = postsetup.app.get('/1')
    assert '/1/edit' not in r.data
    postsetup.done()


def test_admin_can_view_edit_link(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1')
    assert '/1/edit' in r.data
    postsetup.done()


def test_anonymous_cannot_view_delete_link(postsetup):
    r = postsetup.app.get('/1')
    assert '/1/delete' not in r.data
    postsetup.done()


def test_admin_can_view_delete_link(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1')
    assert '/1/delete' in r.data
    postsetup.done()
