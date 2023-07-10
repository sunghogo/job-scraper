import logging  # Setup logging config

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Decorator that handles exceptions by printing the message and then raising them
def handle_exceptions_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}", exc_info=True)
            raise e
    return wrapper
