import logging
from selenium.common.exceptions import TimeoutException
from util.util import webdriver_screenshot

# Declare outputs and errors directory paths
outputs_path = "outputs"
error_path = f"{outputs_path}/errors"


# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles general exceptions by printing the message and then raising them
def exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}", exc_info=False)
            raise e
    return wrapper


# Decorator that handles timeout exceptions by printing the message and then raising them
# Based on arguments passed to scraper_util.py: webdriver_wait_class(driver: WebDriver, timeout: int, class_name: str)
def timeout_exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException:
            webdriver_screenshot(
                driver=kwargs['driver'], filename='timeout_exception.png')
            raise TimeoutException(
                f"Waiting for {kwargs['class_name']} at {kwargs['driver'].current_url} timed out after {kwargs['timeout']}s")
    return wrapper
