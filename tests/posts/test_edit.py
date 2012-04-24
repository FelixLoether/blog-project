from tests.conftest import get_token


def edit_post(postsetup, token, title='title', content='content', tags='',
        action='save', url='/1/edit'):
    return postsetup.app.post(url, data={
        'token': token,
        'title': title,
        'content': content,
        'tags': tags,
        'action': action
    }, follow_redirects=True)


def test_anonymous_cannot_get_edit_page(postsetup):
    r = postsetup.app.get('/1/edit', follow_redirects=True)
    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data
    postsetup.done()


def test_anonymous_cannot_edit_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)
    postsetup.app.get('/logout')
    r = edit_post(postsetup, token)

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    r = postsetup.app.get('/')
    assert token not in r.data
    postsetup.done()


def test_anonymous_cannot_preview_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)
    postsetup.app.get('/logout')
    r = edit_post(postsetup, token)

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    r = postsetup.app.get('/')
    assert token not in r.data
    postsetup.done()


def test_admin_can_get_edit_page(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    assert r.status_code == 200
    assert 'Create Post' in r.data
    postsetup.done()


def test_admin_can_edit_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)

    r = edit_post(postsetup, token, title=token)

    assert r.status_code == 200
    assert token in r.data
    assert 'Success' in r.data
    postsetup.done()


def test_admin_can_preview_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)

    r = edit_post(postsetup, token, title=token, action='preview')

    assert r.status_code == 200
    assert '<article>' in r.data
    postsetup.done()


def test_invalid_token_prevents_creation(postsetup):
    postsetup.login()
    r = edit_post(postsetup, 'invalid-token')
    assert 'Tokens did not match.' in r.data
    postsetup.done()


def test_cannot_get_edit_page_for_nonexisting_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/2/edit')

    assert r.status_code == 404
    assert 'That post does not exist.' in r.data
    postsetup.done()


def test_cannot_edit_nonexisting_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)
    r = edit_post(postsetup, token, url='/2/edit')

    assert r.status_code == 404
    assert 'That post does not exist.' in r.data
    postsetup.done()


def test_cannot_preview_nonexisting_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/1/edit')
    token = get_token(r.data)
    r = edit_post(postsetup, token, url='/2/edit', action='preview')

    assert r.status_code == 404
    assert 'That post does not exist.' in r.data
    postsetup.done()
