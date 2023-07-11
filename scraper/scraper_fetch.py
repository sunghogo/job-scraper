from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
from handlers.exceptions_handlers import timeout_exceptions_handler

# Make webdriver wait until class loads, otherwise raise Timeout Exception
@timeout_exceptions_handler
def webdriver_wait_class(driver: WebDriver, timeout: int, class_name: str):
    # Increase timeout by a random number
    timeout += random.random()
    WebDriverWait(driver, timeout=timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    

# Fetches url, wait until class loads, and refetches specified number of times after specified timeout
def webdriver_fetch_wait_class(driver: WebDriver, url:str, class_name: str, timeout: int, refetch_times: int = 0):
    # Fetch url
    driver.get(url)
    
    exception = TimeoutException()
    # Wait for page to load, and if it does, shortcircuit function and return
    # Otherwise, after specified refetch_times, grab the most recent exception and raise it
    for i in range(refetch_times):
        try:
            webdriver_wait_class(driver = driver, timeout=timeout, class_name = class_name)
            return
        except TimeoutException as e:
            exception = e
            continue
    
    # Raise most recent timeout exception
    raise exception
