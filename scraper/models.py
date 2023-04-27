import json

from sqlalchemy import create_engine, Column
from sqlalchemy import (Integer, Text)
from sqlalchemy.orm import sessionmaker, declarative_base
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

def recreate_tables(engine):
    logger.info("Recreating tables...")
    Base.metadata.drop_all(engine)
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

    def __repr__(self):
        return f"JOB< job_id:{self.job_id} | job_title:{self.job_title} | location:{self.location} >"

def getJobsByLocation(location):
    """
    Fetch jobs data location wise with ordering
    :param location: Job location
    :return: Jobs list
    """
    if not location:
        logger.error("Location field is empty...")
        return []

    engine = db_connect()
    session = sessionmaker(bind=engine)()

    jobs = session.query(Jobs).filter(Jobs.location.ilike(f"%{location}%")).order_by(Jobs.location).all()
    session.close()

    logger.info(jobs)
    return jobs

def getJobsByTechnology(technology):
    """
    Fetch jobs data technology wise with ordering
    :param technology: Job technology
    :return: Jobs list
    """
    if not technology:
        logger.error("Technology field is empty...")
        return []
    engine = db_connect()
    session = sessionmaker(bind=engine)()

    jobs = session.query(Jobs).filter(Jobs.job_description.ilike(f"%{technology}%")).order_by(Jobs.job_description).all()
    session.close()

    logger.info(jobs)
    return jobs


if __name__ == "__main__":
    getJobsByTechnology("python")