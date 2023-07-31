# Command to run test:
# pytest tests/ OR pytest tests/tests_webdriver.py

import unittest
import pytest
from util.webdriver_init import init_webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from urllib3.exceptions import MaxRetryError

class TestWebdriver(unittest.TestCase):
    # Initialize webdriver
    def setUp(self):
        self.driver = init_webdriver()

    # Test webdriver initialization
    def test_init_webdriver(self):
        self.assertIsInstance(self.driver, WebDriver)

    # Test webdriver shutdown
    def test_webdriver_close(self):
        with self.assertRaises(MaxRetryError):
            self.driver.quit()
            self.driver.get('http://127.0.0.1')

    # Shutdown webdriver
    # Calling .quit() on an already shutdown driver does not raise an exception
    def tearDown(self):
        if self.driver:
            self.driver.quit()

        
if __name__ == '__main__':
    unittest.main()