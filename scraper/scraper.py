from queue import Queue
from scraper.scrape_indeed import scrape_indeed
from util.webdriver_init import init_webdriver

scraper_queue = Queue()

# Scrapes search on job boards
def scrape(search_position: str, search_location: str, experience_level: str = "ALL"):
    # Initialize webdriver instance
    driver = init_webdriver()

    # Start scraping
    scrape_indeed(driver=driver, search_position=search_position, search_location=search_location, search_options={
                  "experience_level": experience_level, "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})

    # Close webdriver
    driver.quit()


# Put scrape call into queue
def scraper_put(search_position: str, search_location: str, experience_level: str = "ALL"):
    scraper_queue.put(scrape, {search_position: search_position, search_location: search_location, experience_level: experience_level})
    
# Retrieves scrape calls from the queue and executes it
def scraper_get():
    function = scraper_queue.get()
    function()
