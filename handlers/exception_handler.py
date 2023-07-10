import logging
import datetime import datetime

# Declare outputs and errors directory paths
outputs_path = "outputs"
error_path = f"{outputs_path}/errors"

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Decorator that handles general exceptions by printing the message and then raising them
def handle_exceptions_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}", exc_info=True)
            raise e
    return wrapper


# Decorator that handles timeout exceptions by printing the message and then raising them
def handle_timeout_exceptions_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            kwargs["driver"].save_screenshot(
                f"{error_path}/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_timeout_exception.png")
            logging.error(
                f"Waiting for {kwargs['class_name']} timed out after {kwargs['timeout']}s")
            raise e
    return wrapper
