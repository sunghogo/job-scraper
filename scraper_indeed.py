import selenium

def scrape_indeed(driver: selenium.webdriver.chrome.webdriver.WebDriver, position: str, location: str, options: dict = None):
    sort_posted="1"
    experience_level="ENTRY_LEVEL"
    page="1"
    url = f'https://www.indeed.com/jobs?q={position.replace(" ", "+")}&l={location.replace(" ", "+")}'
    # &sc=0kf%3Aexplvl({experience_level})&fromage={sort_posted}&start={page}
    driver.get(url)
    driver.save_screenshot('get-website-screencap.png')

    # # Fetch HTML
    # html = driver.page_source
    # soup = BeautifulSoup(html, 'html.parser')

    # # Open the file in write mode
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(soup.prettify())