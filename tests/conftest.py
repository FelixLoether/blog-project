import tempfile
import re
from blog import app, db, install


def get_token(data):
    res = re.search(r'\<input type="hidden" name="token" value="((\w|\d)+)"\>',
            data)

    assert res is not None
    return res.group(1)


def pytest_funcarg__dbsetup(request):
    return DbSetup()


def pytest_funcarg__appsetup(request):
    return AppSetup()


class DbSetup:
    def __init__(self, clean=False):
        self.f = tempfile.NamedTemporaryFile(suffix='.db')
        self.path = self.f.name
        app.config['DATABASE_PATH'] = None
        app.config['DATABASE_URL'] = 'sqlite:///' + self.path
        db.make_session()
        install('username', 'password')

    def done(self):
        db.session.remove()
        self.f.close()


class AppSetup(DbSetup):
    def __init__(self):
        DbSetup.__init__(self)
        self.app = app.test_client()

    def login(self, username='username', password='password'):
        return self.app.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)
