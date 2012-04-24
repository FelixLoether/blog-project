from blog import db
from blog.users import User
from blog.posts import Post
from tests.conftest import AppSetup


def pytest_funcarg__postsetup(request):
    return PostSetup()


class PostSetup:
    def __init__(self):
        self.appsetup = AppSetup()
        self.app = self.appsetup.app
        self.user = db.session.query(User).first()
        self.create_post('Title', 'the content of the post')

    def create_post(self, title, content):
        p = Post(title, content, self.user)
        db.session.add(p)
        db.session.commit()
        return p

    def login(self):
        return self.appsetup.login()

    def done(self):
        self.appsetup.done()
