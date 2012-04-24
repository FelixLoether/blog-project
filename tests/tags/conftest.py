from blog import db
from blog.tags import Tag
from tests.posts.conftest import PostSetup


def pytest_funcarg__tagsetup(request):
    return TagSetup()


class TagSetup(PostSetup):
    def __init__(self):
        PostSetup.__init__(self)
        t = Tag('test')
        db.session.add(t)
        db.session.commit()
