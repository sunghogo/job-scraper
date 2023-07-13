import logging
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from util.util import append_log

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles logging events into log files
def logs_handler(log_message: str, log_error_message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                append_log(
                    data=f"{log_message} {kwargs['search_position']} in {kwargs['search_location']}", log_type='log', filename='log')
                return func(*args, **kwargs)
            except Exception as e:
                append_log(data=f"{log_error_message} {kwargs['search_position']} in {kwargs['search_location']}",
                           log_type='log', filename='log')
                append_log(data=str(e),
                           log_type='error', filename='error_log')
        return wrapper
    return decorator
