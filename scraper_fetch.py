from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scraper_util import webdriver_wait_class

# Fetches url, and refetches specified number of times after specified timeout
def webdriver_fetch_wait_class(driver: WebDriver, url:str, class_name: str, timeout: int, refetch_times: int = 0, refetch_counter: int = 0):
    # Fetch url
    driver.get(url)
    
    # Wait for page to load, otherwise return to scraper.py module to exit the webdriver
    try:
        webdriver_wait_class(driver = driver, timeout=timeout, class_name = class_name, error_string = url)
    except TimeoutException:
        if refetch_counter >= refetch_times:
            return
        else:
            print(f"Refetching {url} {refetch_counter + 1}x")
            webdriver_fetch_wait_class(driver = driver, url = url, class_name = class_name, timeout = timeout, refetch_times = refetch_times, refetch_counter = refetch_counter + 1)