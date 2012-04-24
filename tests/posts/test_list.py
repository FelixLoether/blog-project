def test_no_posts(appsetup):
    r = appsetup.app.get('/')
    assert r.status_code == 404  # No posts means no pages.
    assert 'We don&#39;t have that many posts.' in r.data
    appsetup.done()


def test_posts_shown_on_index_page(postsetup):
    r = postsetup.app.get('/')
    assert r.status_code == 200
    assert 'the content of the post' in r.data
    postsetup.done()


def test_not_too_many_pages(postsetup):
    r = postsetup.app.get('/page-2')
    assert r.status_code == 404
    postsetup.done()


def test_pagination_works(postsetup):
    for i in xrange(10):
        postsetup.create_post(str(i), str(i))

    r = postsetup.app.get('/page-2')
    assert r.status_code == 200

    r = postsetup.app.get('/page-3')
    assert r.status_code == 200
    assert 'the content of the post' in r.data
    postsetup.done()


def test_pagination_is_shown(postsetup):
    for i in xrange(10):
        postsetup.create_post(str(i), str(i))

    r = postsetup.app.get('/')
    assert '/page-2' in r.data
    assert '/page-3' in r.data
    postsetup.done()
