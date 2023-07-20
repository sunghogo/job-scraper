import logging
from selenium.common.exceptions import TimeoutException
from util.util import append_log
from handlers.exceptions_handlers import NoResultsException

# Initialize log filenames
log_filename = 'task'
error_log_filename = 'error'

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles logging events into log files
# Based on arguments passed to scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None)
def log_scrapes_handler(job_board: str):
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
            except NoResultsException as e:
                append_log(data=f"No results on {job_board} for {kwargs['search_position']} in {kwargs['search_location']}",
                           log_type='log', filename=log_filename)
                append_log(data=str(e),
                           log_type='error', filename=error_log_filename)
            except Exception as e:
                append_log(data=f"{log_message} failed",
                           log_type='log', filename=log_filename)
                append_log(data=str(e),
                           log_type='error', filename=error_log_filename)
        return wrapper
    return decorator


# Decorator that handles logging scraper queue events into error log files
def log_scraper_queue_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            append_log(data=f"Error calling {func.__name__}: {str(e)}",
                        log_type='error', filename=error_log_filename)
    return wrapper