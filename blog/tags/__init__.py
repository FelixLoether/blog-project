from blog import db
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
import re

re_tag_name_sub = re.compile(r'[^\w-]')


def prepare_tag_name(name):
    return re_tag_name_sub.sub('', name.lower())

tag_post_association_table = Table('tag_post_association', db.Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('post_id', Integer, ForeignKey('posts.id')))


class Tag(db.Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    posts = relationship('Post', secondary=tag_post_association_table,
            backref='tags')

    def __init__(self, name):
        self.name = prepare_tag_name(name)

import views
