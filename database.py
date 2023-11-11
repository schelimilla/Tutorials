# contains all connection strings for app to connect to my sql

from sqlalchemy import create_engine #for db to connect with app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root:L!9ck$3rvR@localhost:3306/blog_application'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()
