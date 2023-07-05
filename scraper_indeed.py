import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict
from bs4 import BeautifulSoup
import time
import random
import json
import os
import logging
from datetime import datetime

# Setup logging config
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_indeed(driver: selenium.webdriver.chrome.webdriver.WebDriver, position: str, location: str, options: Dict[str, str] = None):
    # Initialize list containing json job data
    jobs_list = []
    
    # Parse options and construct url
    base_url = 'https://www.indeed.com'
    url = f"{base_url}/jobs?q={position.replace(' ', '+')}&l={location.replace(' ', '+')}"
    if options != None:
        for key, value in options.items():
            if key == 'experience_level':
                url += f"&sc=0kf%3Aexplvl({value})%3B"
            elif key == "date_posted":
                url += f"&fromage={value}"
            elif key == "sort_date":
                url += f"&sort=date"
            elif key == "page":
                url += f"&start={value}"

    # Fetch url and wait until page loads
    driver.get(url)
    timeout = 60
    try:
        WebDriverWait(driver, timeout=timeout, pollingrate=1).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobCard_mainContent')))
    except:
        driver.save_screenshot(f"outputs/screenshots/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_error.png")
        with open(f"outputs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_error.html", 'w', encoding='utf-8') as file:
            file.write(BeautifulSoup(driver.page_source, 'html.parser').prettify())
        logging.error(f"Loading timed out {timeout}s for: {url}")

        return
    
    # Take a screenshot
    # total_page_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    # driver.set_window_size(1200, total_page_height)
    driver.save_screenshot(f"outputs/screenshots/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_website_screencap.png")

    # Fetch HTML
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    jobs = initial_soup.find_all('table', class_='jobCard_mainContent')
    jobs_els = driver.find_elements(By.CLASS_NAME, "jobCard_mainContent")

    print(len(jobs))
    print(len(jobs_els))
    # Extract data
    for i, job in enumerate(jobs):
        job_id = job.find('a').get('data-jk', None)
        # link = job.find('a').get('href', None)
        jobs_els[i].click()
        time.sleep(5 + random.random())
        driver.save_screenshot(f"outputs/screenshots/{job_id}.png")
        
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
        if soup == None:
            time.sleep(10 + random.random())
            print("Delayed!")
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
        
        print(job_dict)
        jobs_list.append(job_dict)
    # Job Type
    # class="css-fhkva6 eu4oa1w0"
    # class="css-1oqmop4 eu4oa1w0"
    print(jobs_list)

    # Write output html
    # # Open the file in write mode
    # with open('outputs/output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())
    
    # Write output json
    with open('outputs/output.json', 'w') as f:
        json.dump(jobs_list, f, indent=4)

    for file_name in os.listdir('./outputs'):
        if os.path.isfile(file_name):
            print(file_name)