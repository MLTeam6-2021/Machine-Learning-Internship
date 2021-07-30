# Outputs data regarding the categories of the Tapas forum

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

chrome_path = r"C:\Users\HP\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

driver.get("https://forums.tapas.io/categories")

print ("Forum Title: Tapas Forum")

#click on categories
# driver.find_element_by_xpath("""//*[@id="ember905"]""").click()
# categories = driver.find_elements_by_class_name("has-description no-logo")
# categories = driver.find_elements(By.XPATH,"//td[contains(@class,'category')]")
categories = driver.find_elements(By.XPATH,"//tr[contains(@class,'has-description no-logo')]")

print ("\nCategories: ")
for category in categories:
    print (category.text + " topics")

driver.quit()