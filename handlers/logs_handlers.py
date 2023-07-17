import logging
from selenium.common.exceptions import TimeoutException
from util.util import append_log
from handlers.exceptions_handlers import NoResultsException

# Initialize log filenames
log_filename = 'task_logs'
error_log_filename = 'error_logs'

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles logging events into log files
# Based on arguments passed to scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None) 
def logs_scraper_handler(job_board: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            log_message = f"Scraping {job_board} for {kwargs['search_position']} in {kwargs['search_location']}"
            try:
                append_log(
                    data=log_message, log_type='log', filename=log_filename)
                ret_val = func(*args, **kwargs)
                append_log(
                    data=f"{log_message} finished", log_type='log', filename=log_filename)
                return ret_val
            except TimeoutException as e:
                append_log(data=f"{log_message} failed",
                           log_type='log', filename=log_filename)
                append_log(data=str(e),
                           log_type='error', filename=error_log_filename)
            except NoResultsException as e:
                append_log(data=f"No results on {job_board} for {kwargs['search_position']} in {kwargs['search_location']}",
                           log_type='log', filename=log_filename)
                append_log(data=str(e),
                           log_type='error', filename=error_log_filename)
        return wrapper
    return decorator
