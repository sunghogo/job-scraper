import undetected_chromedriver as uc

driver = uc.Chrome() # Headless option does not work for chrome version > 108
driver.get('https://nowsecure.nl')
driver.save_screenshot('nowsecure.png')