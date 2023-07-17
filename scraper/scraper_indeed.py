from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Dict, List
from bs4 import BeautifulSoup
from datetime import datetime
import math
import time
import random
from scraper.scraper_fetch import webdriver_fetch_wait_class, webdriver_wait_class
from util.util import webdriver_screenshot, write_json_data
from handlers.exceptions_handlers import exceptions_handler
from handlers.logs_handlers import logs_scraper_handler


# Parse search strings and options and to construct indeed url
def construct_indeed_url(search_position: str, search_location: str, search_options: Dict[str, str] = None):
    base_url = 'https://www.indeed.com'

    parsed_search_position = search_position.replace(' ', '+')
    parsed_search_location = search_location.replace(
        ' ', '+') if ',' not in search_location else f"{search_location.split(',')[0].replace(' ', '+')}%2C+{search_location.split(',')[1].strip()}"

    url = f"{base_url}/jobs?q={parsed_search_position}&l={parsed_search_location}"

    if search_options != None:
        for key, value in search_options.items():
            if key == 'experience_level' and value != "ALL":  # "ENTRY_LEVEL", "ALL"
                url += f"&sc=0kf%3Aexplvl({value})%3B"
            elif key == "sort_date":
                url += f"&sort=date"
            elif key == "date_posted":  # "1", "3", "7"
                url += f"&fromage={value}"
            elif key == "filter_dupe":  # "0" to turn off dupe filter, "1"
                url += f"&filter={value}"
            elif key == "page":  # "1", "2", ...
                url += f"&start={str(int(value) * 10 - 10)}"

    return url


# Navigates through indeed search pages and extracts job listing data
def extract_indeed_pages(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None, total_page_num: int = 1) -> List[Dict[str, str]]:
    # Initialize list containing json job data from page, and json filepath
    list_jobs_data = []
    json_filepath = ""

    # Loop over and fetch each page of job lisitings
    for page in range(1, total_page_num+1):
        # Construct search page indeed url
        search_options["page"] = str(page)
        page_url = construct_indeed_url(
            search_position, search_location, search_options)

        # Fetches each job page, waits for page load, and refetches if it timesout
        webdriver_fetch_wait_class(
            driver=driver, url=page_url, class_name='jobCard_mainContent', timeout=15, refetch_times=3)

        # Fetch page HTML and parsed soup
        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, 'html.parser')

        # Extract job listings from page, and add to jobs list
        list_page_jobs_data = extract_indeed_page(driver=driver)
        list_jobs_data = list_jobs_data + list_page_jobs_data

        #  Write/appends page results to output json data file
        json_filepath = write_json_data(
            data=list_jobs_data, filename=f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}", filepath=json_filepath)

        # Sleep 20 seconds between page fetches
        if page != total_page_num:
            time.sleep(20 + random.random())

        # If there are no next page url due to indeed cutting off search results, end search early
        if page_soup.find('a', {'data-testid': 'pagination-page-next'}) is None:
            break

    # Return list of job data
    return list_jobs_data


# Navigates through indeed page and extracts each job listing data
def extract_indeed_page(driver: WebDriver) -> List[Dict[str, str]]:
    # Initialize list containing json job data from page
    list_page_job_data = []

    # Fetch page HTML and parsed soup
    page_html = driver.page_source
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # Find both source and parsed job listing elements
    jobs = page_soup.find_all('table', class_='jobCard_mainContent')
    jobs_els = driver.find_elements(By.CLASS_NAME, "jobCard_mainContent")

    # Extract data from each job listing on page
    for i, job in enumerate(jobs):

        # Get job id
        job_id = job.find('a').get('data-jk', None)
        job_link = job.find('a').get('href', None)

        # Click on each job listing to open job details body description
        jobs_els[i].click()

        # Wait for righthand job details body description to load, otherwise return to scraper.py module to exit the webdriver
        try:
            webdriver_wait_class(
                driver=driver, timeout=15, class_name='jobsearch-BodyContainer')
        except TimeoutException:
            return

        # Sleep 1 seconds between job detail clicks wait
        time.sleep(1 + random.random())

        # Extract text content of interest from lefthand job summary cards
        position = job.find('h2', class_='jobTitle').get_text()
        company = job.find('span', class_='companyName').get_text()
        location = job.find('div', class_='companyLocation').get_text()

        # Extract text content for metadata bubble
        salary = job.find('div', class_='salary-snippet-container')
        if salary != None:
            salary = salary.get_text()
        estimated_salary = job.find('div', class_='estimated-salary-container')
        if estimated_salary != None:
            estimated_salary = estimated_salary.get_text()

        # Re-extract and parse html after righthand job details body description loads
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extract righthand job details section
        job_details = soup.find('div', {"id": "jobDetailsSection"})
        if job_details is not None:
            job_details = job_details.get_text(
                separator='\n', strip=True)

        # Extract righthand job description
        job_description = soup.find('div', {"id": "jobDescriptionText"})
        if job_description is not None:
            job_description = job_description.get_text(
                separator='\n', strip=True)

        # Form json dictionary containing extracted job information
        job_dict = {
            'job_id': job_id,
            "date_posted": datetime.now().strftime('%Y-%m-%d'),
            'position': position,
            'company': company,
            'location': location,
            'salary': salary,
            'estimated_salary': estimated_salary,
            'detail': job_details,
            'description': job_description,
            'link': f"https://www.indeed.com{job_link}",
        }

        # Push json dictionary into list
        list_page_job_data.append(job_dict)

    # Return list of job data
    return list_page_job_data


# Scrapes indeed with the specified job search query terms nad options
@logs_scraper_handler(log_message=f"Scraping Indeed for", log_error_message="Scraping failed for")
@exceptions_handler
def scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None) -> List[Dict[str, str]]:
    # Construct initial indeed url
    url = construct_indeed_url(
        search_position, search_location, search_options)
    
    # Check if there are no results
    try:
        webdriver_fetch_wait_class(
        driver=driver, url=url, class_name='jobsearch-NoResult-messageContainer', timeout=5)
        return []
    except:
        pass

    # Fetches initial indeed page, waits for page load, and refetches if it timesout
    webdriver_fetch_wait_class(
        driver=driver, url=url, class_name='jobCard_mainContent', timeout=15, refetch_times=3)

    # Fetch initial HTML and parsed soup
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')

    # Extract number of listed jobs, and calculate number of pages
    job_count = initial_soup.find(
        'div', class_='jobsearch-JobCountAndSortPane-jobCount').get_text().split(' ')[0]
    total_page_num = math.ceil(int(job_count) / 15)

    # Extracts job listings data on each page, and then writes/appends them to output json file
    return extract_indeed_pages(driver=driver, search_position=search_position,
                         search_location=search_location, search_options=search_options, total_page_num=total_page_num)
