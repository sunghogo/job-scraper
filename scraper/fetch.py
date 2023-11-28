from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from util.webdriver_util import wait_class, fetch_wait_class
from handlers.exceptions_handlers import NoResultsException
import time
import random

# Initialized html div class names
jobs_summary_container_no_result_div_class = 'jobsearch-NoResult-messageContainer'
job_summary_container_div_class = 'job_seen_beacon'
job_summary_container_title_class = 'jobTitle'

# Fetches indeed, and raises a no results exception if there are no results, or a timeout exxception if the jobs do not load correctly
# TIMEOUT AT 10S TRIGGERS RATE LIMIT
def fetch_indeed(driver: WebDriver, url: str):
    try:
        fetch_wait_class(
        driver=driver, url=url, class_name=jobs_summary_container_no_result_div_class, timeout=15)
        raise NoResultsException()
    except NoResultsException as e:
        raise e
    except TimeoutException:
        pass
    
    try:
        wait_class(driver=driver, timeout=15, class_name=job_summary_container_div_class)
    except TimeoutException as e:
        fetch_wait_class(
            driver=driver, url=url, class_name='jobCard_mainContent', timeout=15, fetch_times=2)