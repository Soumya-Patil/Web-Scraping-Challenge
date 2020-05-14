from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    # Visit the Mars news page. 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    #dictionary  to load the news content 
    news = {}

    # parse html and navigate 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('li', class_="slide")
    nl = '\n'

    # Loop through returned results
    for result in results:    
    # Error handling
        try:
        # Identify and return news title
            news_title = result.find("div", class_='content_title').text
            
            # Identify and return paragraph text
            news_p = result.div.find("div", class_="article_teaser_body").text
            
            # add results only if title and paragraph text are available
            if (news_title and news_p):

                 mars_data["News Title"] = news_title
                 mars_data["Paragraph Text"] = news_p
                
                
        except ElementDoesNotExist:
            print("Error!")

    browser.quit()
            
    
    # Visit JPL Mars Space Images - Featured Image

    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
     
     #You click in buttons. Splinter follows any redirects, and submits forms associated with buttons."""

    browser.find_link_by_partial_text('FULL IMAGE').first.click()
    browser.find_link_by_partial_text('more info').first.click()

    # navigate to the side column to fetch the largest sized image 
    browser.click_link_by_partial_text('1920 x 1200')

     # store it in the variable
    featured_image_url = browser.url
    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url

    browser.quit()

    # Visit Mars Twitter Page

    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # parse the html and navigate through an instance of Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Inspect the webpage to find element "article" encloses the tweets, fetch the first tweet out of it 
    mars_weather = soup.body.find_all("article")[0].text

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather

    browser.quit()

    # Visit the Mars Fact Page
    
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # pass url string to the read_html method of Pandas
    mars_facts_table = pd.read_html(url)
    mars_facts_table
    
    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_facts_table

    browser.quit()


    # Visit the Mars Astrogeology Page
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # visit the webpage through the instance and parse the html

    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    # navigate through the parse tree to find the hemisphere header texts
    click_text= []
    for x in range(4):
        text = soup.find_all('h3')[x].text
        click_text.append(text)
        x += 1
    
    # click on the links with the header texts and store img url and title as key-value pairs and append it to a list 

    hemisphere_image_urls = []

    for x in range(4):
        browser.find_link_by_partial_text(click_text[x]).first.click()
        
        title = browser.find_by_tag('h2.title').text
        browser.click_link_by_text('Sample') #Sample is a clickable link to the full-size image
        
        image_url = browser.windows[1].url   # copy image url 
        hemisphere_image_urls.append({"Title": title, "Img_URL": image_url})
        
        # designate current Image window as a window & close
        window = browser.windows[1] 
        window.close()  
        
        # switch to the main window 
        browser.windows[0]
        
        # go back to the previous page 
        browser.back()
        
        #increment for next clickable header text
        x += 1

    # Add the hemisphere results to the mars data dictionary
    mars_data['mars_astrogeology'] = hemisphere_image_urls

    browser.quit()

    return mars_data



        
















            
       

