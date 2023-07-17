from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
from handlers.exceptions_handlers import timeout_exceptions_handler
from typing import Dict, List
import json
from datetime import datetime
import os

# Declare outputs directory paths
outputs_path = "outputs"
screenshots_path = f"{outputs_path}/screenshots"
errors_path = f"{outputs_path}/errors"
data_path = f"{outputs_path}/data"
logs_path = f"{outputs_path}/logs"


# Make webdriver wait until class loads, otherwise raise Timeout Exception
def wait_class(driver: WebDriver, timeout: int, class_name: str):
    # Increase timeout by a random number
    timeout += random.random()
    WebDriverWait(driver, timeout=timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    

# Fetches url, wait until class loads, and refetches specified number of times after specified timeout
def fetch_wait_class(driver: WebDriver, url:str, class_name: str, timeout: int, refetch_times: int = 0):
    # Fetch url
    driver.get(url)
    
    exception = TimeoutException()
    # Wait for page to load, and if it does, shortcircuit function and return
    # Otherwise, after specified refetch_times, grab the most recent exception and raise it
    for i in range(refetch_times):
        try:
            wait_class(driver = driver, timeout=timeout, class_name = class_name)
            return
        except TimeoutException as e:
            exception = e
            continue
    
    # Raise most recent timeout exception
    raise exception


# Saves screenshots in specified screenshots directory
# webdriver.set_window_size() crashes the page
def screenshot(driver: WebDriver, filename: str):
    filepath = f"{screenshots_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}.png"
    driver.save_screenshot(filepath)


# Write/appends output json in specified data directory, returns filepath name
def write_json_data(data: List[Dict[str, str]], filename: str, filepath: str = "") -> str:
    if filepath == "":
        full_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}.json"
        filepath = f"{data_path}/{full_filename}"
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
    return filepath


# Opens output json file in specified data directory, returns the json data
def read_json_data(filename: str, filepath: str = "") -> List[Dict[str, str]]:
    if filepath == "":
        filepath = f"{data_path}/{filename}"
    with open(filepath, 'r') as file:
        json.load(file)


# Delete output json file in specified data directory
def delete_json_data(filename: str, filepath: str = ""):
    if filepath == "":
        filepath = f"{data_path}/{filename}"
    if os.path.exists(filepath):
        os.remove(filepath)


# Writes/Appends to txt logs in specified directory
def append_log(data: str, log_type: str, filename: str):
    full_filename = f"{datetime.now().strftime('%Y-%m-%d')}_{filename}.log"
    filepath = ""
    if log_type == "error":
        filepath = f"{errors_path}/{full_filename}"
    else:
        filepath = f"{logs_path}/{full_filename}"
    with open(filepath, 'a') as file:
        file.write(
            f"[{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}]: {data}\n")
