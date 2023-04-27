from sqlalchemy.orm import sessionmaker
from models import db_connect, create_table, Jobs
from base_logger import logger

class DataPipeLine:
    def __init__(self):
        """
        Initializes database connection and session maker
        Creates tables
        """
        logger.info("Initiating data pipeline...")
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item):

        # Write iterm to DB.
        session = self.Session()
        job = Jobs()

        existing_job = session.query(Jobs).filter_by(job_id=item['job_id']).first()
        if existing_job is not None:
            job = existing_job

        logger.info(f"ITEM : {item}")
        try:
            job.job_id = item['job_id']
            job.job_title = item['job_title']
            job.company_name = item['company_name']
            job.location = item['location']
            job.posted_date = item['posted_date']
            job.job_description = item['job_description']

            if existing_job:
                session.commit()
            else:
                session.add(job)
                session.commit()

        except Exception as e:
            session.rollback()
            logger.error("Item cannot be inserted!! Parameter(s) missing...")

        finally:
            session.close()



