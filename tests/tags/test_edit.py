from tests.conftest import get_token


def edit_tag(tagsetup, token, name='test', url='/tags/1/edit'):
    return tagsetup.app.post(url, data={
        'token': token,
        'name': name
    }, follow_redirects=True)


def test_anonymous_cannot_get_edit_page(tagsetup):
    r = tagsetup.app.get('/tags/1/edit', follow_redirects=True)
    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data
    tagsetup.done()


def test_anonymous_cannot_edit_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1/edit')
    token = get_token(r.data)
    tagsetup.app.get('/logout')
    r = edit_tag(tagsetup, token)

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    r = tagsetup.app.get('/tags/')
    assert token not in r.data
    tagsetup.done()


def test_admin_can_get_edit_page(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1/edit')
    assert r.status_code == 200
    assert 'Create Post' in r.data
    tagsetup.done()


def test_admin_can_edit_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1/edit')
    token = get_token(r.data)

    r = edit_tag(tagsetup, token, name=token)

    assert r.status_code == 200
    assert token in r.data
    assert 'Success' in r.data
    tagsetup.done()


def test_invalid_token_prevents_creation(tagsetup):
    tagsetup.login()
    r = edit_tag(tagsetup, 'invalid-token')
    assert 'Tokens did not match.' in r.data
    tagsetup.done()


def test_cannot_get_edit_page_for_nonexisting_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/2/edit')

    assert r.status_code == 404
    assert 'That tag does not exist.' in r.data
    tagsetup.done()


def test_cannot_edit_nonexisting_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/1/edit')
    token = get_token(r.data)
    r = edit_tag(tagsetup, token, url='/tags/2/edit')

    assert r.status_code == 404
    assert 'That tag does not exist.' in r.data
    tagsetup.done()
