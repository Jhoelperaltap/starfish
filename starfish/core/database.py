from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def init_db(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

db_session = None

def get_db_session():
    global db_session
    if db_session is None:
        raise Exception("Database not initialized. Call init_db first.")
    return db_session()
