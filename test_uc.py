import undetected_chromedriver as uc
from util.util import append_log
from util.webdriver_util import screenshot
import time
from scraper.scrape_indeed import scrape_indeed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def driver_init_chrome():
    driver = uc.Chrome(headless=True,use_subprocess=False)
    return driver

def driver_init_chromium():
    options = uc.ChromeOptions()
    options.binary_location = '/opt/chromium/chrome-linux/chrome'
    driver = uc.Chrome(headless=True,use_subprocess=False,options=options)
    return driver

def driver_init_selenium():
    options = Options()
    options.binary_location = '/opt/chromium/chrome-linux/chrome'
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                           "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver
    
try:
    driver = driver_init_chrome()
    append_log(data="driver init worked", log_type='error', filename='sneed')
    try:
        driver.get('https://nowsecure.nl')
        time.sleep(5)
        screenshot(driver, 'nowsecure.png')
        driver.get('https://www.indeed.com')
        time.sleep(5)
        driver.save_screenshot('indeed.png')
        screenshot(driver, 'indeed.png')
        append_log(data="It worked", log_type='error', filename='sneed')
        driver.quit()
    except Exception as e:
        append_log(data=f"It failed: {str(e)}", log_type='error', filename='sneed')
except Exception as e:
    append_log(data=f"driver init failed: {str(e)}", log_type='error', filename='sneed')
    
try:
    driver = driver_init_chrome()
    scrape_indeed(driver=driver, search_position='Software Engineer', search_location='United States', search_options={
                  "experience_level": 'ENTRY_LEVEL', "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})
    driver.quit()
    append_log(data="scrape worked", log_type='error', filename='sneed')
except Exception as e:
    append_log(data=f"scrape failed: {str(e)}", log_type='error', filename='sneed')
    
# time.sleep(120)