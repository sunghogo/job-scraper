from scraper.scraper_indeed import scrape_indeed
from util.webdriver_init import init_webdriver

def scrape(search_position: str, search_location: str, experience_level: str = "ALL"):
    # Initialize webdriver instance
    driver = init_webdriver()

    # Start scraping
    scrape_indeed(driver = driver, search_position = search_position, search_location = search_location, search_options={"experience_level": experience_level, "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})
    
    # Close webdriver
    driver.quit()
