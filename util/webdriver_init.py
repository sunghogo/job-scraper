import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

# Initializes Selenium chromium browser and settings
def init_webdriver() -> WebDriver:
    # Setup selenium chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Setting logging level for browser to 'WARNING' and above
    chrome_options.add_argument("--log-level=3")
    chrome_options.set_capability('goog:loggingPrefs', {'browser': 'WARNING'})

    # Initialize webdriver
    driver = uc.Chrome(headless=True,use_subprocess=False,version_main=104,options=chrome_options)
    
    return driver
