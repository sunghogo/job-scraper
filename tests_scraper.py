# Command to run test:
# pytest tests_scraper.py

import unittest
import pytest
from scraper.scraper import Scraper
import time

class TestScraperMethods(unittest.TestCase):
    # Initialize Scraper module
    scraper = None
    
    # Test whether scraper module was properly initialiszed
    def test_scraper_init(self):
        scraper = Scraper()
        self.assertIsInstance(self.scraper, Scraper)
        self.assertTrue(self.scraper.queue.empty())
        
    # Test whether scraper module stop works
    def test_stop(self):
        self.scraper.stop()
        self.assertTrue(self.scraper.stop_event.is_set())

    # Test whether adding scrape calls to the queue works
    def test_add_scrape(self):
        self.scraper.add_scrape(search_position="Software Engineer",
           search_location="New York", experience_level="ENTRY_LEVEL")
        self.assertFalse(self.scraper.queue.empty())

    # Test whether getting and executing scrape calls from the queue works
    def test_execute_scrape(self):
        self.scraper.execute_scrape()
        self.scraper.queue.task_done()
        self.assertTrue(self.scraper.queue.empty())
    
    # Since debugger keeps track of inactive threads, cannot determine whether thread closes properly through .stop() or .join(), and threading.active_count()
    
    # Test whether adding a scrape call to the queue automatically executes it through the run loop
    def test_scraper_loop(self):
        self.scraper = Scraper()
        self.scraper.add_scrape(search_position="Software Engineer",
           search_location="Austin, TX", experience_level="ENTRY_LEVEL")
        self.scraper.queue.join()
        self.assertTrue(self.scraper.queue.empty())
            

if __name__ == '__main__':
    unittest.main()