def test_login_page_exists(appsetup):
    r = appsetup.app.get('/login')
    assert r.status_code == 200
    appsetup.done()


def test_login(appsetup):
    r = appsetup.login()
    assert 'You have logged in.' in r.data
    appsetup.done()


def test_login_with_wrong_password(appsetup):
    r = appsetup.login(password='invalid password')
    assert 'Invalid username or password.' in r.data
    appsetup.done()


def test_login_with_wrong_username(appsetup):
    r = appsetup.login(username='invalid username')
    assert 'Invalid username or password.' in r.data
    appsetup.done()


def test_logout(appsetup):
    appsetup.login()
    r = appsetup.app.get('/logout', follow_redirects=True)
    assert 'You have logged out.' in r.data
    appsetup.done()


def test_show_login_link(appsetup):
    r = appsetup.app.get('/')
    assert '/login' in r.data
    assert '/logout' not in r.data
    appsetup.done()


def test_show_logout_link(appsetup):
    appsetup.login()
    r = appsetup.app.get('/')
    assert '/logout' in r.data
    assert '/login' not in r.data
    appsetup.done()
