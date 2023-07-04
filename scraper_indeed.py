import selenium
from typing import Dict

def scrape_indeed(driver: selenium.webdriver.chrome.webdriver.WebDriver, position: str, location: str, options: Dict[str, str] = None):
    url = f'https://www.indeed.com/jobs?q={position.replace(" ", "+")}&l={location.replace(" ", "+")}'
    if options != None:
        for key, value in options.items():
            if key == "experience_level":
                url += f'&sc=0kf%3Aexplvl({value})%3B'
            elif key == "date_posted":
                url += f'&fromage={value}'
            elif key == "sort_date":
                url += f'&sort=date'
            elif key == "page":
                url += f'&start={value}'

    driver.get(url)
    driver.save_screenshot('get-website-screencap.png')

    # # Fetch HTML
    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')

    # # Open the file in write mode
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())