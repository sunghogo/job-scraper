from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from scraper_indeed import scrape_indeed
from scraper_init import init_webdriver

# Initialize webdriver instance
driver = init_webdriver()

# Start scraping
scrape_indeed(driver=driver, search_position="Software Engineer", search_location="New York, NY", search_options={"experience_level": "ENTRY_LEVEL", "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})
scrape_indeed(driver=driver, search_position="Software Engineer", search_location="United States", search_options={"experience_level": "ENTRY_LEVEL", "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})

# Close webdriver
driver.quit()