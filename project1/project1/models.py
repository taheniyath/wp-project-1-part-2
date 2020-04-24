import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base

# db = SQLAlchemy(app)

# with app.app_context():
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key = True)
    password = Column(String, nullable = False)
    user_created_on = Column(DateTime, nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def __init__(self, username, password, user_created_on=None):
        self.username = username
        self.password = password
        self.user_created_on = datetime.now()

class Books(Base):
    __tablename__ = "books"
    isbn = Column(Integer, primary_key = True)
    title =Column(String, nullable = False)
    author=Column(String, nullable = False)
    year = Column(Integer, nullable = False)

Base.metadata.create_all(engine)
print("tables created")