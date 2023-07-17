from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from util.webdriver_util import fetch_wait_class
from handlers.exceptions_handlers import NoResultsException

# Fetches indeed, and raises a no results exception if there are no results, or a timeout exxception if the jobs do not load correctly
def fetch_indeed(driver: WebDriver, url: str, initial_fetch: bool = False):
    if initial_fetch:
        try:
            fetch_wait_class(
            driver=driver, url=url, class_name='jobsearch-NoResult-messageContainer', timeout=10)
            raise NoResultsException()
        except TimeoutException:
            pass
    
    fetch_wait_class(
        driver=driver, url=url, class_name='jobCard_mainContent', timeout=10, refetch_times=3)