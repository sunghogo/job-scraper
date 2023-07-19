from typing import Dict, List
import json
from datetime import datetime
import os

# Declare and initialize outputs directory and subdirectory paths
# THESE PATHS ARE IMPORTED AND USED IN OTHER UTIL MODULES
outputs_path = "outputs"
screenshots_path = f"{outputs_path}/screenshots"
errors_path = f"{outputs_path}/errors"
data_path = f"{outputs_path}/data"
logs_path = f"{outputs_path}/logs"


# Writes json data in outputs data directory, returns filepath name
def write_json_data(data: List[Dict[str, str]], filename: str, filepath: str = "") -> str:
    if filepath == "":
        full_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename.lower()}.json"
        filepath = f"{data_path}/{full_filename}"
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)
    return filepath


# Opens json file in outputs data directory, returns the json data
def read_json_data(filename: str, filepath: str = "") -> List[Dict[str, str]]:
    if filepath == "":
        filepath = f"{data_path}/{filename.lower()}.json"
    with open(filepath, 'r') as file:
        return json.load(file)


# Delete json file in outputs data directory
def delete_json_data(filename: str, filepath: str = ""):
    if filepath == "":
        filepath = f"{data_path}/{filename.lower()}.json"
    if os.path.exists(filepath):
        os.remove(filepath)


# Writes/Appends to logs in outputs logs directory
def append_log(data: str, log_type: str, filename: str):
    full_filename = f"{datetime.now().strftime('%Y-%m-%d')}_{filename.lower()}.log"
    filepath = ""
    if log_type == "error":
        filepath = f"{errors_path}/{full_filename}"
    else:
        filepath = f"{logs_path}/{full_filename}"
    with open(filepath, 'a') as file:
        file.write(
            f"[{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}]: {data}\n")
