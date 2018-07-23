import os
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
    news_p = soup.find("div", class_="article_teaser_body").text
    
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

    ## Mars Weather


    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    # parse the html
    html = browser.html
    soup = bs(html, "html.parser")

    # find, scrape and print the latest tweet
    latest_tweet = soup.find("div", class_="js-tweet-text-container").text
    mars_data["Mars_Weather"] = latest_tweet

    
    ### Mars Facts - Visit the Mars Facts webpage here and use Pandas to scrape the table 
    # containing facts about the planet including Diameter, Mass, etc.

    url_mars_facts = "https://space-facts.com/mars/"

    tables = pd.read_html(url_mars_facts)
    facts_df = tables[0] 
    # tables

    facts_df.columns = ["description", "value"]
    facts_df.set_index("description")

    # convert dataframe back to html
    mars_table = facts_df.to_html
    mars_data["Mars_Facts"] = mars_table
    # Mars Hemispheres


    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"},
    ]

    browser.quit()

    return mars_data


