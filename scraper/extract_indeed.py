from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import Dict, List
from datetime import datetime, timedelta
import re
import time
import random
from scraper.fetch import fetch_indeed
from util.util import write_json_data
from util.webdriver_util import wait_class
from scraper.url import construct_indeed_url

# Initialize html attribute/class/id names
jobs_summary_container_id_attribute = 'data-testid'
jobs_summary_container_page_next_attribute = 'pagination-page-next'
job_summary_container_div_class = 'job_seen_beacon'
job_summary_container_id_attribute = 'data-jk'
job_summary_container_link_attribute = 'href'
job_summary_container_title_class = 'jobTitle'
job_summary_container_company_class = 'companyName'
job_summary_container_location_class = 'companyLocation'
job_summary_container_date_class = 'date'
job_summary_container_salary_class = 'salary-snippet-container'
job_summary_container_estimated_salary_class = 'estimated-salary-container'
job_detailed_container_div_class = 'jobsearch-RightPane'
job_detailed_container_easy_apply_class = 'jobsearch-IndeedApplyButton-buttonWrapper is-embedded'
job_detailed_container_body_div_class = 'jobsearch-BodyContainer'
job_detailed_container_details_div_class = 'jobDetailsSection'
job_detailed_container_description_div_class = 'jobDescriptionText'

# Navigates through indeed search pages and extracts job listing data
def extract_indeed_pages(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None, total_page_num: int = 1) -> List[Dict[str, str]]:
    # Initialize list containing json job data from page, and json filepath
    list_jobs_data = []
    json_filepath = ""

    # Loop over and fetch each page of job lisitings
    for page in range(1, total_page_num+1):
        # Update search options with page num and construct search page indeed url
        search_options['page'] = str(page)
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

        #  Write/overwrite page results to output json data file
        json_filepath = write_json_data(
            data=list_jobs_data, filename=f"indeed_{search_position.lower().replace(' ', '_')}_{search_location.lower().replace(' ', '_')}", filepath=json_filepath)

        # Sleep 10 seconds between page fetches
        if page != total_page_num:
            time.sleep(10 + random.random())

        # If there are no next page url due to indeed cutting off search results, end search early
        if parsed_page_html.find('a', {jobs_summary_container_id_attribute: jobs_summary_container_page_next_attribute}) is None:
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
    jobs = parsed_page_html.find_all('div', class_= job_summary_container_div_class)
    jobs_els = driver.find_elements(By.CLASS_NAME, job_summary_container_div_class)

    # Extract data from each job listing on page
    for i, job in enumerate(jobs):
        # Get job id
        job_id = job.find('a').get(job_summary_container_id_attribute, None)
        job_link = job.find('a').get(job_summary_container_link_attribute, None)

        # Click on each job listing to open job details body description
        jobs_els[i].click()

        # Wait for righthand job details body description to load, otherwise return to scraper.py module to exit the webdriver
        try:
            wait_class(
                driver=driver, timeout=15, class_name=job_detailed_container_div_class)
        except TimeoutException:
            return

        # Sleep 1.5-4.5 seconds between job detail clicks wait
        time.sleep(1.5 + random.random() + random.random()*2)

        # Extract text content of interest from lefthand job summary cards
        position = job.find('h2', class_=job_summary_container_title_class).get_text()
        company = job.find('span', class_= job_summary_container_company_class).get_text()
        location = job.find('div', class_=job_summary_container_location_class).get_text()
        date = job.find('span', class_=job_summary_container_date_class).find('span').get_text()
        date_posted = datetime.now().strftime('%Y-%m-%d')
        if 'ago' in date:
            days_ago = int(re.find(r'\d+', date))
            date_posted -= timedelta(days_ago)

        # Extract text content for metadata bubble
        salary = job.find('div', class_=job_summary_container_salary_class)
        if salary is not None:
            salary = salary.get_text()
        estimated_salary = job.find('div', class_=job_summary_container_estimated_salary_class)
        if estimated_salary is not None:
            estimated_salary = estimated_salary.get_text()

        # Re-extract and parse html after righthand job details body description loads
        reextracted_html = driver.page_source
        reparsed_html = BeautifulSoup(reextracted_html, 'html.parser')
        job_right_panel = reparsed_html.find('div', class_=job_detailed_container_div_class)

        # Extracts if the listing is easy apply
        easy_apply = 'no'
        easy_apply_button = job_right_panel.find('div', class_= job_detailed_container_easy_apply_class)
        if easy_apply_button is not None:
            easy_apply = 'yes'

        # Extract profile insights section
        # CANNOT extract profile insights unless logged in
        # job_insights =  job_right_panel.find('div', {"id": "mosaic-aboveExtractedJobDescription"})
        # if job_insights is not None:
        #     job_insights = job_insights.get_text(
        #         separator='\n', strip=True)
        
        # Extract righthand job details section
        job_details = job_right_panel.find('div', {'id': job_detailed_container_details_div_class})
        if job_details is not None:
            job_details = job_details.get_text(
                separator='\n', strip=True)

        # Extract righthand job description
        job_description = job_right_panel.find(
            'div', {'id': job_detailed_container_description_div_class})
        if job_description is not None:
            job_description = job_description.get_text(
                separator='\n', strip=True)

        # Form json dictionary containing extracted job information
        job_dict = {
            'job_id': job_id,
            "date_posted": date_posted,
            'position': position,
            'company': company,
            'location': location,
            'salary': salary,
            'estimated_salary': estimated_salary,
            'easy_apply': easy_apply,
            # 'insights': job_insights,
            'detail': job_details,
            'description': job_description,
            'link': f"https://www.indeed.com{job_link}",
        }

        # Push json dictionary into list
        list_page_job_data.append(job_dict)

    # Return list of job data
    return list_page_job_data
