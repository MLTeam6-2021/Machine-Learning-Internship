import time
from datetime import datetime
import os

from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
import json


class WebScraper:
    browser = None 
    topic_dict = {} 
    topic_df = pd.DataFrame(columns=[
        'Topic Title',
        'Category',
        'Leading Post',
        'Post Replies',
        'Created at',
        'Num Replies',
    ])


    def __init__(self, webdriverPath):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')    
        options.add_argument('--incognito')                     
        options.add_argument('--headless')                   
        self.driver = webdriver.Chrome( \
            executable_path = webdriverPath, \
            options = options)


    def get_topic_title_details(self, topic_soup):
        """
        Get topic title and category
        """
        topic_title = topic_soup.find('a', class_='fancy-title').text.strip()

        title_wraper = topic_soup.find('div', class_='title-wrapper')

        topic_tags = title_wraper.find_all('span', class_='badge-category clear-badge')
        topic_tags = [tag.text for tag in topic_tags]
        
        try: 
            topic_category = topic_tags[0]
        
            if len(topic_tags) == 1:
                topic_tags = []
            else:
                topic_tags = topic_tags[1:]
        except:
            topic_category = ''
            
        return topic_title, topic_category
        
    def get_topic_comments(self, topic_soup):
        """
        Get topic leading post and its replies
        """
        postStream = topic_soup.find('div', class_='post-stream')
        postsDivs = postStream.find_all('div', {'class': ['topic-post clearfix topic-owner regular', 'topic-post clearfix regular']})

        comments = []
        for i in range(len(postsDivs)):
            comment = postsDivs[i].find('div', class_='cooked').text
            #postsDivs[i].find('div', class_='cooked').text.replace('\n', ' ')
            comments.append(comment)
        try:
            leading_comment = comments[0]
            if len(comments) == 1:
                other_comments = []
            else:
                other_comments = comments[1:]
        except:
            leading_comment, other_comments = [], []

        return leading_comment, other_comments
    
    def get_topic_created_at(self, topic_soup):
        """
        Get the topic creation date
        """
        created = topic_soup.find('a', class_="post-date")
        
        if created is None:
            created_at = str(0)
        else:
            created_at = created.find('span', class_='relative-date')['title']
    
        return created_at

    def get_topic_replies_nbr(self, topic_soup):
        """
        Get the topic's no. of replies
        """    
        replies = topic_soup.find('a', class_="posts-map badge-posts heatmaps")
        
        if replies == None:
            nbr_replies = str(0)
        else:
            nbr_replies = replies.find('span', class_='number').text
        
        return nbr_replies
    
    def runApplication(self, baseURL, SITE_NAME):
         
        self.driver.get(baseURL)
        baseHTML = self.driver.page_source

        baseSoup = BeautifulSoup(baseHTML, 'html.parser')
      
        categoryAnchors = baseSoup.find_all('a', class_='category-title-link')

        categoryPageURLs = []
        for i in range(len(categoryAnchors)):
            href = categoryAnchors[i]['href']
            categoryPageURLs.append(baseURL + href)

        for categoryURL in categoryPageURLs:
          
            self.driver.get(categoryURL)

            lastHeight = self.driver.execute_script("return document.body.scrollHeight")
            while (True):
                 
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(0.5)
                
                newHeight = self.driver.execute_script("return document.body.scrollHeight")
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight

            categoryHTML = self.driver.page_source
            categorySoup = BeautifulSoup(categoryHTML, 'html.parser')
            
            topicAnchors = categorySoup.find_all('a', class_='title raw-link raw-topic-link')
 
            topicPageURLs = []
            for i in range(len(topicAnchors)):
                href = topicAnchors[i]['href']
                topicPageURLs.append(baseURL + href)

            for topicURL in topicPageURLs:
                self.driver.get(topicURL)
                topicHTML = self.driver.page_source
                topicSoup = BeautifulSoup(topicHTML, 'html.parser')

                topic_title, topic_category = self.get_topic_title_details(topic_soup)
                leading_comment, other_comments = self.get_topic_comments(topic_soup)
                created_at = self.get_topic_created_at(topic_soup)
                nbr_replies = self.get_topic_replies_nbr(topic_soup)
                
                # Attribute dictionary for each topic in a category
                attribute_dict = {
                            'Topic Title': topic_title,
                            'Category': topic_category,
                            'Leading Post': leading_comment,
                            'Post Replies': other_comments,
                            'Created at': created_at,
                            'Num Replies': nbr_replies}
                
                self.topicDict[topic_title] = attributeDict
                self.topicDataframe = self.topicDataframe.append(attributeDict, ignore_index=True)

        
        timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')

        jsonFilename = SITE_NAME + '_SCRAPED_DATA_' + timeStamp + '.json'
        csvFilename = SITE_NAME + '_SCRAPED_DATA_' + timeStamp + '.csv'
         
        jsonFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), jsonFilename)
        csvFileFullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), csvFilename)

        with open(jsonFileFullPath, 'w') as f:
            json.dump(self.topicDict, f)

        self.topicDataframe.to_csv(csvFileFullPath)



if __name__=='__main__':

    webdriverPath = r'C:\Program Files\Python39\chromedriver'

    baseURL = 'https://forums.tapas.io/'
    
    SITE_NAME = 'TAPAS'

    Webscraper = Webscraper(webdriverPath)

    Webscraper.runApplication(baseURL, SITE_NAME)
