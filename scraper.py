from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
from scraper_indeed import scrape_indeed

def init_webdriver():
    # Setup selenium chrome options
    chrome_options= Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-gpu')

    # Initialize webdriver
    driver=webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Initialize webdriver instance
driver = init_webdriver()

# Start scraping
scrape_indeed(driver, "Software Engineer", "United States", {"experience_level": "ENTRY_LEVEL", "date_posted": "1", "sort_date": "true"})

# Close webdriver
driver.quit()