from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Dict
from bs4 import BeautifulSoup
import datetime
import random
import json
import logging
from datetime import datetime
from scraper_util import webdriver_wait_class, webdriver_screenshot, webdriver_write_data

# Setup logging config
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None):
    # Initialize list containing json job data
    jobs_list = []
    
    # Parse search options and construct url
    base_url = 'https://www.indeed.com'
    url = f"{base_url}/jobs?q={search_position.replace(' ', '+')}&l={search_location.replace(' ', '+')}"
    if search_options != None:
        for key, value in search_options.items():
            if key == 'experience_level':
                url += f"&sc=0kf%3Aexplvl({value})%3B"
            elif key == "date_posted":
                url += f"&fromage={value}"
            elif key == "sort_date":
                url += f"&sort=date"
            elif key == "page":
                url += f"&start={value}"

    # Fetch indeed url
    driver.get(url)
    
    # Wait for indeed page to load, otherwise return to scraper.py module to exit the webdriver
    try:
        webdriver_wait_class(driver = driver, timeout=60, class_name = 'jobCard_mainContent', error_string = url)
    except TimeoutException:
        return
    
    webdriver_screenshot(driver = driver, filename = f"indeed_intial_load")

    # Fetch HTML
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    jobs = initial_soup.find_all('table', class_='jobCard_mainContent')
    jobs_els = driver.find_elements(By.CLASS_NAME, "jobCard_mainContent")
    
    # Extract data
    for i, job in enumerate(jobs):
        # Get job id
        job_id = job.find('a').get('data-jk', None)
        # link = job.find('a').get('href', None)
        
        # Click on each job listing to open job details body description
        jobs_els[i].click()
        # Wait for job details body description to load, otherwise return to scraper.py module to exit the webdriver
        try:
            webdriver_wait_class(driver = driver, timeout=30, class_name = 'jobsearch-JobComponent-description', error_string = url)
        except TimeoutException:
            return
        
        webdriver_screenshot(driver = driver, filename = f"{job_id}")
        
        position = job.find('h2', class_='jobTitle').get_text()
        company = job.find('span', class_='companyName').get_text()
        location = job.find('div', class_='companyLocation').get_text()
        
        # metadata = job.find('div', class_='metadataContainer')
        salary = job.find('div', class_='salary-snippet-container')
        if salary != None:
            salary = salary.get_text()
        estimated_salary = job.find('div', class_='estimated-salary-container')
        if estimated_salary != None:
            estimated_salary = estimated_salary.get_text()
            
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        job_details = soup.find('div', class_='jobsearch-JobComponent-description').get_text(separator='\n', strip=True)
       
        job_dict = {
            'job_id': job_id,       
            'position': position,
            'company': company,
            'location': location,
            'salary': salary,
            'estimated_salary': estimated_salary,
            'link': f"{base_url}/viewjob?jk={job_id}",
            'job_details': job_details
        }
        
        jobs_list.append(job_dict)

    # Write output json data file
    webdriver_write_data(data = jobs_list, filename = f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}")
    
    print("Indeed scraped!")