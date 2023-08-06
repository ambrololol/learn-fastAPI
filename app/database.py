from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:a742141189@localhost/fastapi'
#'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

#open database and take data from database without using SQL statements (SQLAlchemy)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()