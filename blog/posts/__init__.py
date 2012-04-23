from blog import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from flask import abort, flash
from datetime import datetime
import math

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

def paginate(query, page):
    result = {}

    if page <= 0:
        abort(404)

    num = app.config['NAVIGATION_PAGE_COUNT'] / 2
    ppp = app.config['POSTS_PER_PAGE']
    start = (page - 1) * ppp
    end = start + ppp

    result['posts'] = posts = query[start:end]
    result['max_page'] = max_page = int(math.ceil(query.count() / float(ppp)))
    result['pages'] = [p for p in xrange(page - num, page + num + 1)
            if 1 < p < max_page]

    if len(posts) == 0:
        flash("We don't have that many posts.", 'error')
        abort(404)

    return result

import views
