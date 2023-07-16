from scraper.scraper_indeed import scrape_indeed
from scraper.scraper_init import init_webdriver

def scrape_search(search_position: str, search_location: str, experience_level: str = "ALL"):
    # Initialize webdriver instance
    driver = init_webdriver()

    # Start scraping
    scrape_indeed(driver = driver, search_position = search_position, search_location = search_location, search_options={"experience_level": experience_level, "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})
    
    # Close webdriver
    driver.quit()