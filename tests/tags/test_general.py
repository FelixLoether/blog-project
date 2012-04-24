def test_anonymous_cannot_view_create_tag_link(tagsetup):
    r = tagsetup.app.get('/')
    assert '/tags/create' not in r.data
    tagsetup.done()


def test_admin_can_view_create_tag_link(tagsetup):
    tagsetup.login()
    r = tagsetup.app.get('/')
    assert '/tags/create' in r.data
    tagsetup.done()
