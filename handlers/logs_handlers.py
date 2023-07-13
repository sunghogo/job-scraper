import logging
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from util.util import append_log

log_filename = 'task_logs'
error_log_filename = 'error_logs'

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles logging events into log files
def logs_scraper_handler(log_message: str, log_error_message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                complete_log_message = f"{log_message} {kwargs['search_position']} in {kwargs['search_location']}"
                append_log(
                    data=complete_log_message, log_type='log', filename=log_filename)
                ret_val = func(*args, **kwargs)
                append_log(
                    data=f"{complete_log_message} finished", log_type='log', filename=log_filename)
                return ret_val
            except Exception as e:
                append_log(data=f"{log_error_message} {kwargs['search_position']} in {kwargs['search_location']}",
                           log_type='log', filename=log_filename)
                append_log(data=str(e),
                           log_type='error', filename=error_log_filename)
        return wrapper
    return decorator
