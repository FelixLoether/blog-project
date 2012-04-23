from blog import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime

class Post(db.Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    _creation_time = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref=backref('posts'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.user = author
        self._creation_time = datetime.utcnow()

    @property
    def creation_time(self):
        if not isinstance(self._creation_time, unicode):
            return self._creation_time

        return datetime.strptime(self._creation_time, '%Y-%m-%d %H:%M:%S.%f')

import views
