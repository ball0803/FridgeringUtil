
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

options = uc.ChromeOptions() 
options.headless = False 
driver = uc.Chrome(use_subprocess=True, options=options) 
driver.get('https://www.wongnai.com/recipes/tags/thai-food-recipes?sort.type=1&type=1')

with open("links2.txt", "w") as f:
    while True:
    # for i in range(10):
        try:
            btn = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-AxirZ")))
            btn.click()
        except:
            print("No more pages")
            break

    h2_elements = driver.find_elements(By.TAG_NAME, "h2")
    for h2 in h2_elements:
        a = h2.find_elements(By.TAG_NAME, "a")
        if a:
            f.write(a[0].get_attribute("href") + "\n")
            print(a[0].get_attribute("href"))