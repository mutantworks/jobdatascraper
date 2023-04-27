# Jobdata Scraper

[![standard-readme compliant](https://img.shields.io/badge/jobdata%20scraper-mutantworks-brightgreen.svg?style=flat-square)](https://github.com/mutantworks/jobdatascraper)



## Table of Contents

- [Exploration](#exploration)
- [Configs](#configs)
- [Usage](#usage)
- [Features](#features)
- [Maintainers](#maintainers)
- [License](#license)

## Exploration

> 1. Libraries to scrape data : 
>    1. Scrapy 
>       > Didn't work out well due to dynamic page randering on indeed website. Tried dynamic agenst and rotating proxies to send requests to indeed pages but somehow elements were not accessible.   
>    2. BeautifulSoup (Didn't work out well due to dynamic page randering on indeed website)
>       > Didn't work out well due to dynamic page randering on indeed website. Tried dynamic agenst to send requests to indeed pages but somehow page was not permissible to access. 
>    3. Selenium 
>       > Crawlers are little bit slow but works well with dynamic content. Most of the properties extracted.
>    4. NLP libraries 
>       > To search for tech words to add technology as a separate column from huge unstructured data of job description.
> 
> 2. SQLAlchemy (https://www.sqlalchemy.org/)
>    > To get rid of raw queries and to use ORM(Object Relational Mapper).
>    
> 3. psycopg2 (https://pypi.org/project/psycopg2/)
>    > To connect with postgresql.



## Configs
> 1. LOG_LEVEL : DEBUG | INFO | WARN | ERROR | CRITICAL
> 2. LOG_FILE : file_name
> 3. LOG_FORMAT : log_format
> 4. DATABASE_CONNECTION_STRING : postgresql+psycopg2://username:password@host/mydatabase

## Usage

To initiate the indeed scraper use below command from ./scraper/ directory. \
Options : \
-p [position] \
-n [number_of_jobs_to_be_scraped]

```sh
$ python indeed_scraper.py -p "software engineer" -n 50
# Crawler will start crawling indeed website and scrap data for 50 jobs for software engineer position 
```
To fetch already scraped data from DB use below command from ./scraper/ directory. \
Options : \
-l [location] \
-n [technology]

This queries will return jobs list in sorted manner.

```sh
$ python models.py -l "pune" -t "python"
# It Will get data of both query. Jobs from pune and Jobs related to python technology. 
```

## Features
> 1. Extract job data from indeed website position wise
> 2. Store data to PostgreSql
> 3. Query data with location and technlogy
> 4. Logging


## Maintainers

[@mutantworks](https://github.com/mutantworks).

## License

[MIT](LICENSE) © Meetkumar Charola