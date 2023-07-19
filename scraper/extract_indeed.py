from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import Dict, List
from datetime import datetime
import time
import random
from scraper.fetch import fetch_indeed
from util.util import write_json_data
from util.webdriver_util import wait_class
from scraper.construct_url import construct_indeed_url


# Navigates through indeed search pages and extracts job listing data
def extract_indeed_pages(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None, total_page_num: int = 1) -> List[Dict[str, str]]:
    # Initialize list containing json job data from page, and json filepath
    list_jobs_data = []
    json_filepath = ""

    # Loop over and fetch each page of job lisitings
    for page in range(1, total_page_num+1):
        # Update search options with page num and construct search page indeed url
        search_options["page"] = str(page)
        page_url = construct_indeed_url(
            search_position, search_location, search_options)

        # Fetch new job page
        fetch_indeed(driver=driver, url=page_url)

        # Extract page HTML and parsed soup
        extracted_page_html = driver.page_source
        parsed_page_html = BeautifulSoup(extracted_page_html, 'html.parser')

        # Extract job listings from page, and add to jobs list
        list_page_jobs_data = extract_indeed_page(driver=driver)
        list_jobs_data = list_jobs_data + list_page_jobs_data

        #  Write/appends page results to output json data file
        json_filepath = write_json_data(
            data=list_jobs_data, filename=f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}", filepath=json_filepath)

        # Sleep 30 seconds between page fetches
        if page != total_page_num:
            time.sleep(30 + random.random())

        # If there are no next page url due to indeed cutting off search results, end search early
        if parsed_page_html.find('a', {'data-testid': 'pagination-page-next'}) is None:
            break

    # Return list of job data
    return list_jobs_data


# Navigates through indeed page and extracts each job listing data
def extract_indeed_page(driver: WebDriver) -> List[Dict[str, str]]:
    # Initialize list containing json job data from page
    list_page_job_data = []

    # Extract page HTML and parsed soup
    extracted_page_html = driver.page_source
    parsed_page_html = BeautifulSoup(extracted_page_html, 'html.parser')

    # Find both source and parsed job listing elements
    jobs = parsed_page_html.find_all('table', class_='jobCard_mainContent')
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
            wait_class(
                driver=driver, timeout=15, class_name='jobsearch-BodyContainer')
        except TimeoutException:
            return

        # Sleep 1 seconds between job detail clicks wait
        time.sleep(1.5 + random.random() + random.random())

        # Extract text content of interest from lefthand job summary cards
        position = job.find('h2', class_='jobTitle').get_text()
        company = job.find('span', class_='companyName').get_text()
        location = job.find('div', class_='companyLocation').get_text()

        # Extract text content for metadata bubble
        salary = job.find('div', class_='salary-snippet-container')
        if salary is not None:
            salary = salary.get_text()
        estimated_salary = job.find('div', class_='estimated-salary-container')
        if estimated_salary is not None:
            estimated_salary = estimated_salary.get_text()

        # Re-extract and parse html after righthand job details body description loads
        reextracted_html = driver.page_source
        reparsed_html = BeautifulSoup(reextracted_html, 'html.parser')

        # Extract righthand job details section
        job_details = reparsed_html.find('div', {"id": "jobDetailsSection"})
        if job_details is not None:
            job_details = job_details.get_text(
                separator='\n', strip=True)

        # Extract righthand job description
        job_description = reparsed_html.find(
            'div', {"id": "jobDescriptionText"})
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
