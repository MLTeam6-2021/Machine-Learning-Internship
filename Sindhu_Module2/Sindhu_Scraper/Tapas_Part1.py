from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import time

chrome_path = r"C:\Users\HP\Downloads\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

# driver.get("https://forums.tapas.io/c/announcements")
# driver.get("https://forums.tapas.io/c/events-challenges")
# driver.get("https://forums.tapas.io/c/Off-Topic")
# driver.get("https://forums.tapas.io/c/art-comics")
# driver.get("https://forums.tapas.io/c/writing-novels")
# driver.get("https://forums.tapas.io/c/reviews-feedback")
# driver.get("https://forums.tapas.io/c/collaborations")
# driver.get("https://forums.tapas.io/c/questions")
# driver.get("https://forums.tapas.io/c/answered")
# driver.get("https://forums.tapas.io/c/tech-support-site-feedback")
driver.get("https://forums.tapas.io/c/promotions")

lastHeight = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            
while (True):
    # Scroll to bottom of page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new page segment to load
    time.sleep(0.5)

    # Calculate new scroll height and compare with last scroll height
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
                    
    lastHeight = newHeight
            

element = driver.find_elements(By.XPATH,"//td[contains(@class,'main-link clearfix')]")
for value in element:
    title = value.text
    
reply_elements = driver.find_elements(By.XPATH,"//span[contains(@class,'number')]")
for reply in reply_elements:
    replies = reply.text

view_elements = driver.find_elements(By.XPATH,"//td[contains(@class,'num views')]")
for num in view_elements:
    views = num.text

activity_elements = driver.find_elements(By.XPATH,"//td[contains(@class,'num age activity')]")
for day in activity_elements:
    activity = day.text  

# elems = driver.find_elements(By.XPATH,"//td[contains(@class,'title')]")

# comment_elements = []

# links = []
# for i in range(len(elems)):
#     links.append(elems[i].get_attribute('href'))

# for link in links:
#     print ('navigating to: ' + link)
#     driver.get(link)

#     # do stuff within that page here...
#     comment_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'cooked')]")
#     for comment in comment_elements:
#         comments = comment.text  

#     driver.back()

D = {'titles': [], 'replies': [], 'views': [], 'activity': [],'category': []}

for value,reply,num,day in zip(element,reply_elements, view_elements, activity_elements):
    D['titles'].append(value.text)
    D['replies'].append(reply.text)
    D['views'].append(num.text)
    D['activity'].append(day.text)
    # D['category'].append("announcements")
    # D['category'].append("events and challenges")
    # D['category'].append("off topic")
    # D['category'].append("art-comics")
    # D['category'].append("writing-novels")
    # D['category'].append("reviews-feedback")
    # D['category'].append("collaborations")
    # D['category'].append("questions")
    # D['category'].append("answered")
    # D['category'].append("tech-support-site-feedback")
    D['category'].append("promotions")

# for value,reply,num,day,comment in zip(element,reply_elements, view_elements, activity_elements, comment_elements):
#     D['titles'].append(value.text)
#     D['replies'].append(reply.text)
#     D['views'].append(num.text)
#     D['activity'].append(day.text)
#     D['category'].append("Announcements")
#     D['comments'].append(comment.text)

pd.set_option("display.max_rows", None, "display.max_columns", None)
df = pd.DataFrame(D)

# df.to_csv('tapas_announcements.csv')
# df.to_csv('tapas_events_challenges.csv')
# df.to_csv('tapas_off-topic.csv')
# df.to_csv('tapas_art-comics.csv')
# df.to_csv('tapas_writing-novels.csv')
# df.to_csv('tapas_reviews-feedback.csv')
# df.to_csv('tapas_collaborations.csv')
# df.to_csv('tapas_questions.csv')
# df.to_csv('tapas_answered.csv')
# df.to_csv('tapas_tech-support-site-feedback.csv')
df.to_csv('tapas_promotions.csv')

driver.quit()