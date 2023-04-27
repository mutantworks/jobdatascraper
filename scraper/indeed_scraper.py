from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from base_logger import logger
from pipeline import DataPipeLine



class Scraper:

    # Driver Configs
    logger.info("Setting up chrome drivers...")
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    logger.info("Driver's setup successful...")

    base_url = 'https://indeed.com/'
    jobs_to_be_scraped = 50

    def __init__(self, position = "software developer", location = "india"):
        self.position = position
        self.location = location
        self.extracted_jobs = []

    def LoadIndeed(self):
        logger.info("Initiating indeed crawler...")
        logger.info(f"Crawling URL : {Scraper.base_url} | Position : {self.position} | Location : {self.location}")
        Scraper.driver.get(Scraper.base_url)
        job_position_field = Scraper.driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
        job_position_field.send_keys(self.position)

        initial_search_button = Scraper.driver.find_element(By.XPATH, '//*[@id="jobsearch"]/button')
        initial_search_button.click()

    def ExtractJobList(self):
        logger.info("Extracting Job URLs...")

        while len(self.extracted_jobs) <= Scraper.jobs_to_be_scraped:
            Scraper.driver.implicitly_wait(3)
            job_cards = Scraper.driver.find_elements(By.XPATH,
                                             '//*[(@id = "mosaic-provider-jobcards")]//*[contains(concat( " ", @class, " " ), concat( " ", "eu4oa1w0", " " ))]')

            for job in job_cards:
                if job.get_attribute('href') is not None:
                    job_details = {'job_id' : job.get_attribute('id').split('_')[-1]}
                    self.extracted_jobs.append({"job_url" : job.get_attribute('href'), "job_details" : job_details})

            try:
                navigation_buttons = Scraper.driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-13p07ha", " " ))]')
                next_page_url = navigation_buttons[0].get_attribute('href') if len(navigation_buttons) < 2 else navigation_buttons[-1].get_attribute('href')
                Scraper.driver.get(next_page_url)

            except Exception as e:
                logger.error("Element extraction failed...")
                pass

    def ExtractIndividualJobData(self):
        logger.info("Extracting individual job data...")

        for job in self.extracted_jobs[:Scraper.jobs_to_be_scraped+1]:
            logger.info(f"Job in process : {job['job_url']}")
            Scraper.driver.get(job["job_url"])

            # Extract Job Title
            try:
                job["job_details"]["job_title"] = ""
                job["job_details"]["job_title"] = Scraper.driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "jobsearch-JobInfoHeader-title", " " ))]//span').text

            except Exception as e:
                logger.error(f"Element extraction failed : JOB TITLE")
                pass

            # Extract Company Name
            try:
                job["job_details"]["company_name"] = ""
                job["job_details"]["company_name"] = Scraper.driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-1cjkto6", " " ))]//a').text

            except Exception as e:
                logger.error(f"Element extraction failed for JOB : COMPANY NAME")
                pass

            # Extract Job Location
            try:
                job["job_details"]["location"] = ""
                job["job_details"]["location"] = Scraper.driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-6z8o9s", " " ))]//div').text

            except Exception as e:
                logger.error(f"Element extraction failed for JOB : LOCATION")
                pass

            # Extract Posted Date
            try:
                job["job_details"]["posted_date"] = ""
                date_posted = Scraper.driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "css-5vsc1i", " " ))]')
                for element in date_posted:
                    job["job_details"]["posted_date"] += (element.text + " ")

            except Exception as e:
                logger.error(f"Element extraction failed for JOB : POSTED DATE")
                pass

            try:
                job["job_details"]["job_description"] = ""
                job_description = Scraper.driver.find_element(By.XPATH, '//*[(@id = "jobDescriptionText")]')
                for element in job_description.find_elements(By.XPATH, '*'):
                    job["job_details"]["job_description"] += (element.text + " | ")

            except Exception as e:
                logger.error(f"Element extraction failed for JOB : JOB DESCRIPTION")
                pass

            logger.info(f"Job Details : {job['job_details']}")


    def LoadJobs(self):
        logger.info("Loading extracted data to DB...")
        logger.info(f"Total Extracted Jobs : {len(self.extracted_jobs)}")

        dp = DataPipeLine()
        for job in self.extracted_jobs:
            dp.process_item(job['job_details'])

        logger.info("Job data loaded to PostreSQL !")


if __name__ == "__main__":
    s = Scraper()
    s.LoadIndeed()
    s.ExtractJobList()
    s.ExtractIndividualJobData()
    s.LoadJobs()


