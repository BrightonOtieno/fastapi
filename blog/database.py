from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args ={"check_same_thread":False})

Base = declarative_base()
