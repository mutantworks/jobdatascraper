import json

from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, Text)
from base_logger import logger

Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from configs.py.
    Returns sqlalchemy engine instance
    """
    logger.info("Initiating sql alchemy engine...")
    with open('configs.json') as config_file:
        data = json.load(config_file)

    DB_CONNECTION_STRING = data['DATABASE_CONNECTION_STRING']
    logger.info(f"Database Connection String : {DB_CONNECTION_STRING}")

    return create_engine(DB_CONNECTION_STRING)


def create_table(engine):
    logger.info("Creating tables...")
    Base.metadata.create_all(engine)

class Jobs(Base):
    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column('job_id', Text())
    job_title = Column('job_title', Text())
    company_name = Column('company_name', Text())
    location = Column('location', Text())
    posted_date = Column('posted_date', Text())
    job_description = Column('job_description', Text())

