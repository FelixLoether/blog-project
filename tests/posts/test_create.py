from tests.conftest import get_token


def create_post(postsetup, token, title='title', content='content', tags='',
        action='save'):
    return postsetup.app.post('/create', data={
        'token': token,
        'title': title,
        'content': content,
        'tags': tags,
        'action': action
    }, follow_redirects=True)


def test_anonymous_cannot_get_create_page(postsetup):
    r = postsetup.app.get('/create', follow_redirects=True)
    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data
    postsetup.done()


def test_anonymous_cannot_create_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/create')
    token = get_token(r.data)
    postsetup.app.get('/logout')
    title = 'title-{0}'.format(token)
    r = create_post(postsetup, token, title=title)

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    r = postsetup.app.get('/')
    assert title not in r.data
    postsetup.done()


def test_anonymous_cannot_preview_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/create')
    token = get_token(r.data)
    postsetup.app.get('/logout')
    r = create_post(postsetup, token, action='preview')

    assert r.status_code == 403
    assert 'You need to be logged in to view that content' in r.data

    postsetup.done()


def test_admin_can_get_create_page(postsetup):
    postsetup.login()
    r = postsetup.app.get('/create')
    assert r.status_code == 200
    assert 'Create Post' in r.data
    postsetup.done()


def test_admin_can_create_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/create')
    token = get_token(r.data)
    title = 'title-{0}'.format(token)

    r = create_post(postsetup, token, title=title)

    assert r.status_code == 200
    assert title in r.data
    assert 'Success' in r.data
    postsetup.done()


def test_admin_can_preview_post(postsetup):
    postsetup.login()
    r = postsetup.app.get('/create')
    token = get_token(r.data)
    title = 'title-{0}'.format(token)

    r = create_post(postsetup, token, title=title, action='preview')

    assert r.status_code == 200
    assert '<article>' in r.data
    assert title in r.data
    postsetup.done()


def test_invalid_token_prevents_creation(postsetup):
    postsetup.login()
    r = create_post(postsetup, 'invalid-token')
    assert 'Tokens did not match.' in r.data
    postsetup.done()
