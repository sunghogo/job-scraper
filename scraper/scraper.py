from threading import Thread
from queue import Queue
import time
from scraper.scrape_indeed import scrape_indeed
from util.webdriver_init import init_webdriver
from handlers.exceptions_handlers import logging_exceptions_handler
from handlers.logs_handlers import log_scraper_queue_handler, log_webdriver_handler


class Scraper(threading.Thread):
    """
    Scraper class that continuously runs on a thread, and executes ScrapeTasks in its queue.

    Args:
        threading.Thread: Thread superclass to run the Scraper object
    """
    
    def __init__(self):
        """
        Initializes and runs Scraper object.
        
        Upon initialization, Scraper object will initialize and start superclass Thread object, queue, and flags.
        """
        
        super().__init__()
        self.queue = Queue()
        self.daemon = True # This ensures the thread will exit when the main program exits
        self.stop_event = threading.Event() # Creates Thread flag that stops the thread when set
        self.pause = False
        self.start() # Starts superclass thread object
    
    
    def stop(self):
        """
        Stops Scraper object.
        
        This method will PERMANENTLY stop the super Thread object and can only be restarted with a NEW INSTANCE.
        """
        
        self.stop_event.set()


    def pause(self):
        
        
        
    def run(self):
        """
        Starts Scraper object.
        
        Forever loops and executes scrapes every 3 seconds until the object is stopped.
        """
        
        while not self.stop_event.is_set():
            time.sleep(3)
            if not self.queue.empty():
                self.execute_scrape()
                self.queue.task_done()  # Signals to queue that task was finished


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
@log_webdriver_handler
@logging_exceptions_handler
def scrape(search_position: str, search_location: str, experience_level: str = "ALL"):
    # Initialize webdriver instance
    driver = init_webdriver()

    # Start scraping
    scrape_indeed(driver=driver, search_position=search_position, search_location=search_location, search_options={
                  "experience_level": experience_level, "date_posted": "1", "sort_date": "true", "filter_dupe": "0"})

    # Close webdriver
    driver.quit()