from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


# Initializes Selenium chromium browser and settings
def init_webdriver():
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
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                           "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver
