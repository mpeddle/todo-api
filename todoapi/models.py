from sqlalchemy import Column, Integer, String
from todoapi.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=False)
    text = Column(String(500), unique=False)

    def __init__(self, title=None, text=None):
        self.title = title
        self.text = text

    def api_dict(self):
        return {'id': self.id, 'title':self.title, 'text':self.text}
