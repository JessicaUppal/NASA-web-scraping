# Import dependancies 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():
    # Path to driver
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Scrape and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "facts": mars_facts(),
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
    }
    # Return data from scrape
    return data

# Scrape mars news site
def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Find news title and paragraph and save in a variable 
    slide_elem = news_soup.select_one('div.list_text')
    news_title = slide_elem.find("div", class_="content_title").get_text()
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    # Return data
    return news_title, news_p

# Scrape mars space images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    # Click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parsing html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # Return the image
    return img_url


def mars_facts():

     # Scrape mars facts html into a dataframe 
    df = pd.read_html("https://galaxyfacts-mars.com")[0]
    # Set columns of dataframe
    df.columns = ["Description", "Mars", "Earth"]
    # Return dataframe as html 
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url + 'index.html')

    # Click and return href
    hemisphere_url = []
    for i in range(4):
        browser.find_by_css("a.product-item img")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']
        # Add hemisphere to list
        hemisphere_url.append(hemi_data)
        # Return to browser
        browser.back()
    # Return list 
    return hemisphere_url


def scrape_hemisphere(html_text):
    # parsing html with soup
    hemisphere_text = soup(html_text, "html.parser")


    title_text = hemisphere_text.find("h2", class_="title").get_text()
    image_text= hemisphere_text.find("a", text="Sample").get("href")

    hemispheres = {
        "title": title_text,
        "img_url": image_text
    }

    return hemispheres


if __name__ == "__main__":

    # Print scraped data
    print(scrape())
