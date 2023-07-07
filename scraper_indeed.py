from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Dict, List
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import math
import time
import random
from scraper_util import webdriver_wait_class, webdriver_screenshot, webdriver_write_data
from scraper_fetch import webdriver_fetch_wait_class

# Setup logging config
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse search strings and options and to construct indeed url
def construct_indeed_url(search_position: str, search_location: str, search_options: Dict[str, str] = None):
    base_url = 'https://www.indeed.com'
    url = f"{base_url}/jobs?q={search_position.replace(' ', '+')}&l={search_location.replace(' ', '+')}"
    if search_options != None:
        for key, value in search_options.items():
            if key == 'experience_level': # "ENTRY_LEVEL"
                url += f"&sc=0kf%3Aexplvl({value})%3B"
            elif key == "sort_date":
                url += f"&sort=date"
            elif key == "date_posted": # "0", "1"
                url += f"&fromage={value}"
            elif key == "filter_dupe": # "0", "1"
                url += f"%filter={value}"
            elif key == "page": # "1", "2", ...
                url += f"&start={str(int(value) * 10 - 10)}"
    return url
    
def scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None):
    # Initialize list containing json job data
    jobs_list = []
    
    # Construct initial indeed url
    url = construct_indeed_url(search_position, search_location, search_options)

    # Fetches initial indeed page, waits for page load, and refetches if it timesout
    webdriver_fetch_wait_class(driver = driver, url = url, class_name = 'jobCard_mainContent', timeout = 15, refetch_times = 3)

    # Screenshot initial load
    webdriver_screenshot(driver = driver, filename = 'indeed_intial_load')

    # Fetch initial HTML and parsed soup
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    
    # Extract number of listed jobs, and calculate number of pages
    job_count = initial_soup.find('div', class_='jobsearch-JobCountAndSortPane-jobCount').get_text().split(' ')[0]
    total_page_num = math.ceil(int(job_count) / 15)
    
    # Loop over and fetch each page of job lisitings
    for page in range(1, total_page_num+1):
        # Construct page indeed url
        search_options["page"] = str(page)
        page_url = construct_indeed_url(search_position, search_location, search_options)

        # Fetches each job page, waits for page load, and refetches if it timesout
        webdriver_fetch_wait_class(driver = driver, url = page_url, class_name = 'jobCard_mainContent', timeout = 15, refetch_times = 3)
        
        # Screenshot initial load
        webdriver_screenshot(driver = driver, filename = f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}_page_{page}")
    
        # Fetch page HTML and parsed soup
        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, 'html.parser')
        jobs = page_soup.find_all('table', class_='jobCard_mainContent')
        jobs_els = driver.find_elements(By.CLASS_NAME, "jobCard_mainContent")
        
        # Extract data from each job listing
        for i, job in enumerate(jobs):
            # Get job id
            job_id = job.find('a').get('data-jk', None)
            job_link = job.find('a').get('href', None)
            
            # Click on each job listing to open job details body description
            jobs_els[i].click()
            time.sleep(2 + random.random())
            
            # Wait for righthand job details body description to load, otherwise return to scraper.py module to exit the webdriver
            try:
                webdriver_wait_class(driver = driver, timeout=15, class_name = 'jobsearch-JobComponent-description', error_string = driver.current_url)
            except TimeoutException:
                return
            
            # Extract text content of interest from lefthand job summary cards
            position = job.find('h2', class_='jobTitle').get_text()
            company = job.find('span', class_='companyName').get_text()
            location = job.find('div', class_='companyLocation').get_text()
            salary = job.find('div', class_='salary-snippet-container')
            if salary != None:
                salary = salary.get_text()
            estimated_salary = job.find('div', class_='estimated-salary-container')
            if estimated_salary != None:
                estimated_salary = estimated_salary.get_text()
            
            # Re-extract and parse html after righthand job details body description loads
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract full job details
            job_details = soup.find('div', class_='jobsearch-JobComponent-description').get_text(separator='\n', strip=True)
        
            # Form json dictionary containing extracted job information
            job_dict = {
                'job_id': job_id,
                "date_posted": datetime.now().strftime('%Y-%m-%d'),
                'position': position,
                'company': company,
                'location': location,
                'salary': salary,
                'estimated_salary': estimated_salary,
                'link': f"https://www.indeed.com{job_link}",
                'job_details': job_details
            }
            
            # Push json dictionary into list
            jobs_list.append(job_dict)
            
        print(f"Indeed {search_position} in {search_location} page {str(page)} complete")

        # Write intermediate output json data file
        webdriver_write_data(data = jobs_list, filename = f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}_page_1_to_{page}")
        
        if page != total_page_num:
            time.sleep(20 + random.random())
    
    # Write final output json data file 
    webdriver_write_data(data = jobs_list, filename = f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}")
    
    print(f"Indeed {search_position} in {search_location} scraped!")