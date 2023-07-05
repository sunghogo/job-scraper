import selenium
from selenium.webdriver.common.by import By
from typing import Dict
from bs4 import BeautifulSoup
import time
import random
import json

def scrape_indeed(driver: selenium.webdriver.chrome.webdriver.WebDriver, position: str, location: str, options: Dict[str, str] = None):
    jobs_list = []
    
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

    driver.get(url)
    total_page_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(1200, total_page_height)
    driver.save_screenshot('outputs/screenshots/get-website-screencap.png')

    # Fetch HTML
    initial_html = driver.page_source
    initial_soup = BeautifulSoup(initial_html, 'html.parser')
    jobs = initial_soup.find_all('table', class_='jobCard_mainContent')
    jobs_el = driver.find_elements(By.CLASS_NAME, "jobCard_mainContent")
    
    # Extract data
    for i, job in enumerate(jobs):
        job_id = job.find('a').get('data-jk', None)
        # link = job.find('a').get('href', None)
        jobs_el[i].click()
        time.sleep(5 + random.random())
        driver.save_screenshot(f"outputs/screenshots/{job_id}.png")
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
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
    # Job Type
    # class="css-fhkva6 eu4oa1w0"
    # class="css-1oqmop4 eu4oa1w0"
    print(jobs_list)

    # Write output html
    # # Open the file in write mode
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())
    
    # Write output json
    with open('outputs/output.json', 'w') as f:
        json.dump(jobs_list, f, indent=4)