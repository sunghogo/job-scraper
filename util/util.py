from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Dict, List
import json
import logging
from datetime import datetime

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Declare outputs directory paths
outputs_path = "outputs"
screenshots_path = f"{outputs_path}/screenshots"
errors_path = f"{outputs_path}/errors"
data_path = f"{outputs_path}/data"
logs_path = f"{outputs_path}/logs"


# Saves screenshots in specified screenshots directory
# webdriver.set_window_size() crashes the page
def webdriver_screenshot(driver: WebDriver, filename: str):
    filepath = f"{screenshots_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}.png"
    driver.save_screenshot(filepath)


# Write/appends output json in specified data directory
def append_json_data(data: List[Dict[str, str]], filename: str):
    filepath = f"{data_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}.json"
    with open(filepath, 'q') as file:
        json.dump(data, file, indent=4)
    return filepath
        

# Writes/Appends to txt logs in specified directory
def append_log(data: str, request_id: str, log_type: str, filename: str):
    filepath
    if log_type == "error":
        filepath = f"{errors_path}/{datetime.now().strftime('%Y-%m-%d')}_{filename}.txt"
    else:
        filepath = f"{logs_path}/{datetime.now().strftime('%Y-%m-%d')}_{filename}.txt"
            
    with open(f"{errors_path}/{datetime.now().strftime('%Y-%m-%d')}_{filename}.txt", 'a') as file:
            file.write(f"[{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}]: {data}\n")
