def test_nonexisting_page_404s(appsetup):
    r = appsetup.app.get('/this-does-not-exist')
    assert r.status_code == 404
    appsetup.done()
