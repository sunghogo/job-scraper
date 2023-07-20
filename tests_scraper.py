# Command to run test:
# pytest tests_scraper.py

import unittest
import pytest
from scraper.scraper import Scraper
import logging

class TestScraperMethods(unittest.TestCase):
    # # Initialize Scraper module
    scraper = Scraper()
    
    # Test whether scraper module was properly initialiszed
    def test_scraper_init(self):
        self.assertIsInstance(self.scraper, Scraper)
        self.assertTrue(self.scraper.queue.empty())
        
    # Test whether scraper module stop works
    def test_stop(self):
        self.scraper.stop()
        self.assertTrue(self.scraper.stop_event.is_set())
    
    # Test whether scraper module resume works
    def test_resume(self):
        self.scraper.resume()
        self.assertFalse(self.scraper.stop_event.is_set())

    # Test whether adding scrape calls to the queue works
    def test_add_scrape(self):
        self.scraper.stop()
        self.scraper.add_scrape(search_position="Software Engineer",
           search_location="New York", experience_level="ENTRY_LEVEL")
        self.assertFalse(self.scraper.queue.empty())

    # Test whether getting and executing scrape calls from the queue works
    def test_execute_scrape(self):
        self.scraper.execute_scrape()
        self.scraper.queue.task_done()
        self.assertTrue(self.scraper.queue.empty())

if __name__ == '__main__':
    unittest.main()