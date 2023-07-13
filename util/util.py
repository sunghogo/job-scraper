from selenium.webdriver.chrome.webdriver import WebDriver
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


# Saves screenshots in specified screenshots directory
# webdriver.set_window_size() crashes the page
def webdriver_screenshot(driver: WebDriver, filename: str):
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
