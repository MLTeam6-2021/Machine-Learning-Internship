# Outputs data regarding the categories of the Tapas forum

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import csv

chrome_path = r"C:\Users\HP\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

driver.get("https://forums.tapas.io/categories")

#click on categories
# driver.find_element_by_xpath("""//*[@id="ember905"]""").click()
# categories = driver.find_elements_by_class_name("has-description no-logo")
# categories = driver.find_elements(By.XPATH,"//td[contains(@class,'category')]")
categs=[]
categories = driver.find_elements(By.XPATH,"//tr[contains(@class,'has-description no-logo')]")
for category in categories:
    categs.append(category.text + " topics")

header = ['categories']
data = [
    [categs[0] + '\n'],
    [categs[1] + '\n'],
    [categs[2] + '\n'],
    [categs[3] + '\n'],
    [categs[4] + '\n'],
    [categs[5] + '\n'],
    [categs[6] + '\n'],
    [categs[7] + '\n'],
    [categs[8] + '\n'],
    [categs[9] + '\n']
]

with open('tapas_categories.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)

driver.quit()
