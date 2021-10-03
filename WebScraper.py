from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import pandas as pd


import re

PATH = r"chromedriver.exe"
browser = None




def scrapeAssessment(address):
    url = f"https://www.bcassessment.ca/"
    browser = webdriver.Chrome(PATH)
    browser.get(url)
    searchBox = browser.find_element_by_css_selector("#rsbSearch")
    ### address = 4321 ewart st## Debugging purposes

    searchBox.send_keys(address)
    time.sleep(3)
    dropdown = browser.find_element_by_css_selector("#ui-id-3")

    print(dropdown.get_attribute("innerHTML"))

    if(dropdown.get_attribute("innerHTML") == "No results"):
        print("Property not found on BCAssessment")
        return -1

    dropdown.click()
    time.sleep(3)
    try:
        assessedVal = browser.find_element_by_css_selector("#lblTotalAssessedValue")
        return assessedVal.get_attribute("innerHTML")
    except Exception as e:
        logging.info(e, "Error at trying to find asseessed value")
        return -1

    finally:
        browser.close()


# This loads webdriver from the local machine if it exists.
def testWebDriverExist():
    try:
        browser = webdriver.Chrome(PATH)
        print("The path to webdriver_manager was found.")
        browser.quit()
    # If a webdriver not found error occurs it is then downloaded.
    except:
        print("webdriver not found. Update 'PATH' with file path in the download.")


def toNum (string):

    try:

        num = string.replace("$", "")
        num = num.replace(",", "")
        num = int(num)
        return num
    except AttributeError:
        return -1


def main():
    scraped_listings = []

    final_listings = pd.DataFrame(columns=["address", "assessedVal", "forSaleVal"])


    city = "burnaby"

    url = f"https://realtylink.org/en/properties~for-sale~{city}?view=Thumbnail&uc=0"
    browser = webdriver.Chrome(PATH)
    browser.get(url)
    time.sleep(3)  ### require the browser some time to load.  important ###
    #### Get how many pages we need ####
    pages = browser.find_elements_by_css_selector(".pager-current")
    page = pages[0].get_attribute("innerHTML")
    split = page.split("/")
    num_Pages = int(split[1]) - 1
    ####
    next_button = browser.find_elements_by_class_name("next")[0]
    scraped_listings = []

    pages_left = num_Pages

    ### how many pages we want to scrape ##
    for i in range(0, 4):
        pages_left -= 1
        next_button.click()
        time.sleep(3)  ### require the browser some time to load.  important ###

        addresses = browser.find_elements_by_class_name("address")

        for i in range(0, len(addresses)):
            ## New page we need to reassign new button##
            next_button = browser.find_elements_by_class_name("next")[0]

            prices = browser.find_elements_by_class_name("price")
            price = (prices[i].get_attribute("innerHTML"))
            soup = BeautifulSoup(price, features="lxml")
            price = soup.get_text().strip()

            add = BeautifulSoup(addresses[i].get_attribute("innerHTML"), features="lxml")
            street = add.select('div')[0].text.strip()

            scraped_listings.append(
                (street, price))

        logging.info(f"{pages_left} pages left to scrape")

    logging.info(f"We've collected : {len(scraped_listings)}")
    browser.close()

    logging.info(f"************* All the Listings in {city}******************")
    for _ in scraped_listings:
        address = _[0]
        assessedVal = scrapeAssessment(address)
        property = dict()
        property["address"] = address
        property["assessedVal"] = toNum(assessedVal)
        property["forSaleVal"] = toNum(_[1])
        final_listings = final_listings.append(property, ignore_index= True)

    final_listings["Difference in Price"] = (final_listings["forSaleVal"] / final_listings["assessedVal"])

    print(final_listings.head(10))
    final_listings.to_csv("scraped listings for Burnaby")

if __name__ == '__main__':
    main()
