# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import types

# Create a new SQLAlchemy type that remove trailing whitespaces
class StrippedString(types.TypeDecorator):
    '''
    Returns CHAR values with spaces stripped
    '''

    impl = types.String

    def process_bind_param(self, value, dialect):
        "No-op"
        return value

    def process_result_value(self, value, dialect):
        "Strip the trailing spaces on resulting values"
        return value.rstrip()

    def copy(self):
        "Make a copy of this type"
        return StrippedString(self.impl.length)

# Helper to map and register a Python class to a db table
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column('email', StrippedString(60))
    password = Column('password', StrippedString(60))
    minetime = Column('minetime', Integer)
    config = Column('config', StrippedString(200))

    def __repr__(self):
        return "<User(id='%s',email='%s', password='%s', minetime='%s', config'%s')>" % (self.id, self.email, self.password, self.minetime, self.config)

    @staticmethod
    def list(session):
        return session.query(User).all()

