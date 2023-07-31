# Command to run test:
# pytest tests/ OR pytest tests/tests_scraper.py

import unittest
import pytest
from scraper.scraper import Scraper

# Since debugger keeps track of inactive threads, cannot determine whether thread closes properly through .stop() or .join(), and threading.active_count()
class TestScraper(unittest.TestCase):
    # Initialize Scraper module
    def setUp(self):
        self.scraper = Scraper()
    
    # Test whether scraper module was properly initialiszed
    def test_scraper_init(self):
        self.assertIsInstance(self.scraper, Scraper)
        self.assertTrue(self.scraper.queue.empty())
        
    # Test whether scraper module stop works
    def test_stop(self):
        self.scraper.stop()
        self.assertTrue(self.scraper.stop_event.is_set())

    # Test whether adding/executing scrape calls to/from the queue works
    def test_add_execute_scrape(self):
        self.scraper.add_scrape(search_position="Frontend",
           search_location="New York", experience_level="ENTRY_LEVEL")
        self.assertFalse(self.scraper.queue.empty())
        self.scraper.execute_scrape()
        self.scraper.queue.task_done()
        self.assertTrue(self.scraper.queue.empty())
    
    # Test whether adding a scrape call to the queue automatically executes it through the run loop
    def test_scraper_loop(self):
        self.scraper.add_scrape(search_position="Frontend",
           search_location="Austin, TX", experience_level="ENTRY_LEVEL")
        self.scraper.queue.join()
        self.assertTrue(self.scraper.queue.empty())
        
    # Shutdown Scraper module
    def tearDown(self):
        if self.scraper:
            self.scraper.stop()
            

if __name__ == '__main__':
    unittest.main()