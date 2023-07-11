import logging
from datetime import datetime
from selenium.common.exceptions import TimeoutException

# Declare outputs and errors directory paths
outputs_path = "outputs"
logs_path = f"{outputs_path}/logs"
error_path = f"{outputs_path}/errors"

# Setup logging config
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')