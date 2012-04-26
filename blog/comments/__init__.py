from blog import app, db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Comment(db.Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    _creation_time = Column(String)
    username = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('comments'))

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', backref=backref('comments'))

    def __init__(self, content, post, user=None, username=None):
        self.content = content
        self.post = post
        self.user = user
        self.username = username
        self._creation_time = datetime.utcnow()

    @property
    def creation_time(self):
        if not isinstance(self._creation_time, unicode):
            return self._creation_time

        return datetime.strptime(self._creation_time, '%Y-%m-%d %H:%M:%S.%f')

from views import blueprint
app.register_blueprint(blueprint, url_prefix='/comments')
