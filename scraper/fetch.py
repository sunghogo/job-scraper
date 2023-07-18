from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from util.webdriver_util import fetch_wait_class
from handlers.exceptions_handlers import NoResultsException

# Fetches indeed, and raises a no results exception if there are no results, or a timeout exxception if the jobs do not load correctly
# TIMEOUT AT 10S TRIGGERS RATE LIMIT
def fetch_indeed(driver: WebDriver, url: str, initial_fetch: bool = False):
    if initial_fetch:
        try:
            fetch_wait_class(
            driver=driver, url=url, class_name='jobsearch-NoResult-messageContainer', timeout=15)
            raise NoResultsException()
        except NoResultsException as e:
            raise e
        except TimeoutException:
            pass
    
    fetch_wait_class(
        driver=driver, url=url, class_name='jobCard_mainContent', timeout=15, fetch_times=2)