from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from scraper_indeed import scrape_indeed
from scraper_init import init_webdriver

# Initialize webdriver instance
driver = init_webdriver()

# Start scraping
scrape_indeed(driver=driver, position="Software Engineer", location="United States", options={"experience_level": "ENTRY_LEVEL", "date_posted": "1", "sort_date": "true"})

# Close webdriver
driver.quit()