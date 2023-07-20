import threading
from queue import Queue
import time
from scraper.scrape_indeed import scrape_indeed
from util.webdriver_init import init_webdriver
from handlers.exceptions_handlers import logging_exceptions_handler
from handlers.logs_handlers import log_scraper_queue_handler

# Scraper module that continuously runs on a thread, and executes scrapes in its queue
class Scraper(threading.Thread):
    # Initialize Thread superclass, queue, events, and starts upon initialization
    def __init__(self):
        super().__init__()
        self.queue = Queue()
        # This ensures the thread will exit when the main program exits
        self.daemon = True
        # Create flag that stops the thread when set
        self.stop_event = threading.Event()
        self.start()
    
    # Stops thread. This method will lead the thread to PERMANENTLY FINISH EXECUTING, and can only be restarted with a NEW INSTANCE of the class
    def stop(self):
        self.stop_event.set()

    # Thread run loop
    def run(self):
        time.sleep(1)
        while not self.stop_event.is_set():
            if not self.queue.empty():
                self.execute_scrape()
                # Signals to queue that task was finished
                self.queue.task_done()

    # Add scrape call to the queue
    @log_scraper_queue_handler
    @logging_exceptions_handler
    def add_scrape(self, search_position: str, search_location: str, experience_level: str = "ALL"):
        self.queue.put((scrape, [], {"search_position": search_position, "search_location": search_location, "experience_level": experience_level}))
    
    # Retrieves and executes scrape call from the queue
    @log_scraper_queue_handler
    @logging_exceptions_handler
    def execute_scrape(self):
        func, args, kwargs = self.queue.get()
        func(*args, **kwargs)


# Scrapes search on job boards
def scrape(search_position: str, search_location: str, experience_level: str = "ALL"):
    # Initialize webdriver instance
    driver = init_webdriver()

    # Start scraping
    scrape_indeed(driver=driver, search_position=search_position, search_location=search_location, search_options={
                  "experience_level": experience_level, "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})

    # Close webdriver
    driver.quit()