from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from util.util import screenshots_path
from datetime import datetime
import random

# Make webdriver wait until class loads, otherwise raises timeout exception
def wait_class(driver: WebDriver, timeout: int, class_name: str):
    timeout += random.random()
    WebDriverWait(driver, timeout=timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    

# Makes webdriver fetch url, wait until class loads, and refetches specified number of times 
# If timing out all the refetches, raises most recent timeout exception
def fetch_wait_class(driver: WebDriver, url:str, class_name: str, timeout: int, refetch_times: int = 0):
    driver.get(url)
    timeout_exception = TimeoutException()
    for i in range(refetch_times):
        try:
            wait_class(driver = driver, timeout=timeout, class_name = class_name)
            return
        except TimeoutException as e:
            timeout_exception = e
            continue
    raise timeout_exception


# Make webdriver screenshot and save the image in outputs screenshots directory
# webdriver.set_window_size() crashes the page
def screenshot(driver: WebDriver, filename: str):
    filepath = f"{screenshots_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}.png"
    driver.save_screenshot(filepath)