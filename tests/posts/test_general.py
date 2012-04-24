def test_anonymous_cannot_view_create_post_link(postsetup):
    r = postsetup.app.get('/')
    assert '/create' not in r.data
    postsetup.done()


def test_admin_can_view_create_post_link(postsetup):
    postsetup.login()
    r = postsetup.app.get('/')
    assert '/create' in r.data
    postsetup.done()
