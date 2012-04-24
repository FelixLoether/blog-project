from blog import db
from blog.tags import Tag
from tests.posts.conftest import PostSetup


def pytest_funcarg__tagsetup(request):
    return TagSetup()


class TagSetup:
    def __init__(self):
        self.postsetup = PostSetup()
        self.app = self.postsetup.app
        self.user = self.postsetup.user
        t = Tag('test')
        db.session.add(t)
        db.session.commit()

    def create_post(self, title='title', content='content'):
        return self.postsetup.create_post(title, content)

    def login(self):
        return self.postsetup.login()

    def done(self):
        self.postsetup.done()
