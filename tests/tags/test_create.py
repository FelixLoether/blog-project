from tests.conftest import get_token


def create_tag(tagsetup, token, name='test-tag'):
    return tagsetup.app.post('/tags/create', data={
        'token': token,
        'name': name
    }, follow_redirects=True)


def test_anonymous_cannot_get_create_page(tagsetup):
    r = tagsetup.app.get('/tags/create', follow_redirects=True)
    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data
    tagsetup.done()


def test_anonymous_cannot_create_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/create')
    token = get_token(r.data)
    tagsetup.app.get('/logout')
    name = 'name-{0}'.format(token)
    r = create_tag(tagsetup, token, name=name)

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    r = tagsetup.app.get('/tags/')
    assert name not in r.data
    tagsetup.done()


def test_admin_can_get_create_page(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/create')
    assert r.status_code == 200
    assert 'Create Post' in r.data
    tagsetup.done()


def test_admin_can_create_tag(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/tags/create')
    token = get_token(r.data)
    name = 'name-{0}'.format(token)

    r = create_tag(tagsetup, token, name=name)

    assert r.status_code == 200
    assert name in r.data
    assert 'Success' in r.data
    tagsetup.done()


def test_invalid_token_prevents_creation(tagsetup):
    tagsetup.login()
    r = create_tag(tagsetup, 'invalid-token')
    assert 'Tokens did not match.' in r.data
    tagsetup.done()
