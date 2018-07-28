import os
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import splinter 
from splinter import Browser


def scrape():
    executable_path = {'executable_path': '/Users/Ben/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}

    # open slinter browser for mars news site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    # now use beautiful soup parser
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the latest mars news
    news_title = soup.find("div", class_="content_title").text
    
    # get the article summary
    news_p = soup.find("div", class_="rollover_description_inner").text
    
    mars_data["Mars_news_title"] = news_title
    mars_data["Mars_summary"] = news_p 

    ##JPL Mars Space Images - Featured Image

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    url_JPL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_JPL)
    
    browser.find_by_id("full_image").click()
    browser.is_element_present_by_text("more info", wait_time=1)
    browser.find_link_by_partial_text("more info").click()
    html = browser.html
    soup = bs(html, "html.parser")
    img = soup.select_one("img.main_image").get("src")
    featured_image_url = 'https://jpl.nasa.gov'+img

    mars_data["Featured_Image"] = featured_image_url

    ## Visit the Mars Weather twitter account and scrap the lates Mars weather tweet.
    import tweepy
    # Twitter API Keys
    from config import consumer_key, consumer_secret, access_token, access_token_secret

    # Setup Tweepy API Authentication
    
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    # parse the html
    html = browser.html
    soup = bs(html, "html.parser")

    latest_tweet = soup.find("div", class_="js-tweet-text-container").text
    mars_data["Weather report"] = latest_tweet
    
    ### Mars Facts - Visit the Mars Facts webpage here and use Pandas to scrape the table 
    # containing facts about the planet including Diameter, Mass, etc.

    import pandas as pd
    
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    tables = pd.read_html(url_mars_facts)
    facts_df = tables[0] 
    # tables

    facts_df.columns = ["description", "value"]
    facts_df.set_index("description")

    # convert dataframe back to html
    mars_html_table = facts_df.to_html(classes = "table")
    mars_table = mars_html_table.replace('\n', ' ')
    mars_data["Mars_Facts"] = mars_table
    
    # Mars Hemispheres

    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"},
    ]

    # browser.visit(mars_url)
    # html = browser.html
    # soup = bs(html, 'html.parser')
    # mars_hemis=[]

    # for i in range (4):
    #     time.sleep(5)
    #     images = browser.find_by_id('h3').click()
    #     images[i].click()
    #     html = browser.html
    #     soup = bs(html, 'html.parser')
    #     partial = soup.find("img", class_="wide-image")["src"]
    #     img_title = soup.find("h2",class_="title").text
    #     img_url = 'https://astrogeology.usgs.gov'+ partial
    #     dictionary={"title":img_title,"img_url":img_url}
    #     mars_hemis.append(dictionary)
    #     browser.back()

    # mars_data['mars_hemis'] = mars_hemis

    browser.quit()
    print(mars_data)
    return mars_data


