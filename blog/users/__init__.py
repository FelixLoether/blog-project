from blog import db, app
from sqlalchemy import Column, Integer, String
from passlib.apps import custom_app_context as pwd_context

class User(db.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)

    def __init__(self, name, password):
        app.logger.info('Creating user "%s".', name)
        self.name = name
        self.password = pwd_context.encrypt(password)

    def verify(self, password):
        return pwd_context.verify(password, self.password)
