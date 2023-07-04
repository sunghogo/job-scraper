from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup

# Setup selenium chrome options
chrome_options= Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-gpu')

# Initialize webdriver
driver=webdriver.Chrome(options=chrome_options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

position="Software+Engineer"
location="United+States"
sort_posted="1"
experience_level="ENTRY_LEVEL"
page="1"
url = f'https://www.indeed.com/jobs?q={position}&l={location}&sc=0kf%3Aexplvl({experience_level})&fromage={sort_posted}&start={page}'
driver.get(url)
driver.save_screenshot('get-website-screencap.png')

# Fetch HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Open the file in write mode
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

# Quit driver
driver.quit()