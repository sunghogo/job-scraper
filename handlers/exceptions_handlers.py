import logging
from selenium.common.exceptions import TimeoutException
from util.webdriver_util import screenshot

# Declare outputs and errors directory paths
outputs_path = "outputs"
error_path = f"{outputs_path}/errors"


# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Custom Exception Classes
class NoResultsException(Exception):
    def __init__(self, message="NoResultsException: No results found"):
        super().__init__(message)


# Decorator that handles general exceptions by printing the message and then raising them
def exceptions_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}", exc_info=False)
            raise e
    return wrapper


# Decorator that handles timeout exceptions by forming the message and then raising them
# Based on arguments passed to scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None))
def timeout_exceptions_handler(job_board: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TimeoutException:
                raise TimeoutException(
                    f"Timed out waiting for {job_board} for {kwargs['search_position']} in {kwargs['search_location']} at {kwargs['driver'].current_url}")
        return wrapper
    return decorator


# Decorator that handles screenshotting from webdriver upon exception, and then raising the exception upwards
# Based on arguments passed to scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None))
def screenshot_exceptions_handler(job_board: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if type(e) is not NoResultsException:
                    screenshot(
                        driver=kwargs['driver'], filename=f"{job_board}_{kwargs['search_position']}_{kwargs['search_location']}_{type(e)}_exception")
                    raise e
        return wrapper
    return decorator


# Decorator that handles no result exceptions by forming the message and then raising them
# Based on arguments passed to scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None))
def no_results_exceptions_handler(job_board: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NoResultsException:
                raise NoResultsException(
                    f"No results on {job_board} for {kwargs['search_position']} in {kwargs['search_location']}")
        return wrapper
    return decorator
