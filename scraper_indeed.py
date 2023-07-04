import selenium
from typing import Dict
from bs4 import BeautifulSoup

def scrape_indeed(driver: selenium.webdriver.chrome.webdriver.WebDriver, position: str, location: str, options: Dict[str, str] = None):
    jobs = []
    
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
    driver.save_screenshot('get-website-screencap.png')

    # Fetch HTML
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    job_els = soup.find_all('table', class_='jobCard_mainContent')
    
    for job in job_els:
        job_id = job.find('a').get('data-jk', None)
        link = job.find('a').get('href', None)
        position = job.find('h2', class_='jobTitle').get_text()
        company = job.find('span', class_='companyName').get_text()
        location = job.find('div', class_='companyLocation').get_text()
        # salary = job.find('div', class_='heading6 tapItem-gutter metadataContainer')
        salary = job.find('div', class_='salary-snippet-container')
        if salary != None:
            salary = salary.get_text()
       
        job_dict = {
            'job_id': job_id,       
            'position': position,
            'company': company,
            'location': location,
            'salary': salary,
            'link': f"{base_url}/viewjob?jk={job_id}"
        }
        jobs.append(job_dict)
        
    print(jobs)

    # # Open the file in write mode
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())