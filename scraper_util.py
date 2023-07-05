from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import random
from datetime import datetime
import json
from typing import Dict, List

outputs_path = "outputs"
screenshots_path = f"{outputs_path}/screenshots"
error_path = f"{outputs_path}/error"
data_path = f"{outputs_path}/data"

# Make webdriver wait until class loads, otherwise create error files in specified error directory and raise exception
def webdriver_wait_class(webdriver: WebDriver, timeout: int, class_name: str, error_string: str = ""):
    timout += random.random() * 1
    try:
        WebDriverWait(webdriver, timeout=timeout).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    except:
        webdriver.save_screenshot(f"{error_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_error.png")
        with open(f"{error_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_error.html", 'w', encoding='utf-8') as file:
            file.write(BeautifulSoup(webdriver.page_source, 'html.parser').prettify())          
        logging.error(f"Loading timed out {timeout}s" if error_string == "" else f"Loading timed out {timeout}s: " + error_string)
        raise Exception()

# Saves screenshots in specified screenshots directory
# webdriver.set_window_size() crashes the page
def webdriver_screenshot(webdriver: WebDriver, filename: str):
    filepath = f"outputs/screenshots/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_" + filename
    webdriver.save_screenshot(filepath)
    
# Write output json in specified data directory
def webdriver_write_data(data: List[Dict[str, str]]):
    with open(f"{data_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_data.json", 'w') as f:
        json.dump(data, f, indent=4)
