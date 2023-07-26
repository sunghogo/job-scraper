# Command to run test:
# pytest tests_searches.py

import unittest
import pytest
from scraper.scraper import Scraper
import time

class TestScraperMethods(unittest.TestCase):
    # Initialize Scraper module
    scraper = Scraper()
    
    # Test multiple searches
    def test_scraper_loop(self):
      self.scraper.add_scrape(search_position="Software Engineer",
   search_location="New York", experience_level="ENTRY_LEVEL")
      self.scraper.add_scrape(search_position="Software Engineer",
search_location="Austin, TX", experience_level="ENTRY_LEVEL")
      self.scraper.add_scrape(search_position="Software Engineer Entry",
         search_location="United States", experience_level="ENTRY_LEVEL")
      self.scraper.add_scrape(search_position="Software Engineer Junior",
         search_location="United States", experience_level="ENTRY_LEVEL")
      self.scraper.add_scrape(search_position="Software Engineer Internship",
         search_location="United States", experience_level="ENTRY_LEVEL")
      self.scraper.queue.join()
      self.assertTrue(self.scraper.queue.empty())
            

if __name__ == '__main__':
    unittest.main()