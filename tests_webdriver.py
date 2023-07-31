# Command to run test:
# pytest tests_webdriver.py

import unittest
import pytest
from util.webdriver_init import init_webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

class TestWebdriverInitialization(unittest.Testcase):
    # Initialize webdriver
    driver = None
    
    def test_init_webdriver(self):
        driver = init_webdriver()
        self.assertIsInstance(self.driver, WebDriver)
        
    def test_webdriver_close(self):
        with self.assertRaises(WebDriverException):
            self.driver.quit()
            self.driver.get('http://127.0.0.1')
        
if __name__ == '__main__':
    unittest.main()