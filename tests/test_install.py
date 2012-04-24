from blog import db
from blog.users import User


def test_install_creates_user(dbsetup):
    assert db.session.query(User).filter_by(name='username').count() == 1
    dbsetup.done()


def test_install_creates_user_with_correct_password(dbsetup):
    u = db.session.query(User).filter_by(name='username').one()
    assert u.verify('password')
    assert not u.verify('incorrect password')
    dbsetup.done()
