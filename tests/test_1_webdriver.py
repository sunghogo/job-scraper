# Command to run test:
# pytest tests/ OR pytest tests/tests_webdriver.py

import unittest
import pytest
from util.webdriver_init import init_webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

class TestWebdriver(unittest.TestCase):
    # Initialize webdriver
    def setUp(self):
        self.driver = init_webdriver()

    def test_init_webdriver(self):
        self.assertIsInstance(self.driver, WebDriver)

    def test_webdriver_close(self):
        with self.assertRaises(WebDriverException):
            self.driver.quit()
            self.driver.get('http://127.0.0.1')

    # Shutdown webdriver
    def tearDown(self):
        if self.driver:
            try:
                self.driver.quit()
            except WebDriverException: # Catch test_web_driver_close() exception
                pass

        
if __name__ == '__main__':
    unittest.main()