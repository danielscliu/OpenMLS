from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging

PATH    = r"chromedriver.exe"
browser = None

# This loads webdriver from the local machine if it exists.
def testWebDriverExist():
    try:
        browser = webdriver.Chrome(PATH)
        print("The path to webdriver_manager was found.")

    # If a webdriver not found error occurs it is then downloaded.
    except:
        print("webdriver not found. Update 'PATH' with file path in the download.")



import time
from selenium import webdriver
from bs4 import BeautifulSoup

# driver = webdriver.Chrome(ChromeDriverManager().install())
DRIVER_PATH  = PATH




def scrapeCourses():
    url = "https://www.bcit.ca/programs/applied-data-analytics-certificate-part-time-5512cert/#courses"
    browser = webdriver.Chrome(DRIVER_PATH)
    browser.get(url)
    courses = browser.find_elements_by_css_selector(".clicktoshow")

    for course in courses:
        start = course.get_attribute('innerHTML')
        soup = BeautifulSoup(start, features= "lxml")
        print(soup.get_text())
        print("***")

    browser.quit()

def scrapeVPL():
    url = "https://vpl.bibliocommons.com/events/search/index"
    browser = webdriver.Chrome(DRIVER_PATH)
    browser.get(url)
    time.sleep(5) ### require the browser some time to load.  important ###

    button = browser.find_element_by_css_selector(".btn-lg")
    for i in range(0,20):
        button.click()
        '''
        If you see the following error increase the sleep time:
        ElementClickInterceptedException: element click intercepted:
        '''
        print("Count: ", str(i))
        time.sleep(4)
    print("done loop")



    courses = browser.find_elements_by_css_selector(".event-row")
    import re
    for e in courses:
        textContent  = e.get_attribute('innerHTML')
        # Beautiful soup removes HTML tags from our content if it exists.
        soup         = BeautifulSoup(textContent, features="lxml")
        rawString    = soup.get_text().strip()

        # Remove hidden characters for tabs and new lines.
        rawString = re.sub(r"[\n\t]*", "", rawString)

        # Replace two or more consecutive empty spaces with '*'
        rawString = re.sub('[ ]{2,}', '*', rawString)

        # Fine tune the results so they can be parsed.
        rawString = rawString.replace("Location", "Location*")
        rawString = rawString.replace("Registration closed", "Registration closed*")
        rawString = rawString.replace("Registration required", "Registration required*")
        rawString = rawString.replace("In Progress", "*In Progress*")
        rawString = rawString.replace("*/*", "/")
        rawString = rawString.replace("Full*","*Full*")

        eventArray = rawString.split('*')

        EVENT_NAME = 0
        EVENT_DATE = 1
        EVENT_TIME = 2
        eventName = eventArray[EVENT_NAME]
        eventDate = eventArray[EVENT_DATE].strip() # remove leading and trailing spaces
        eventTime = eventArray[EVENT_TIME].strip() # remove leading and trailing spaces
        location  = eventArray[len(eventArray)-1]
        print("Name:     " + eventName)
        print("Date:     " + eventDate)
        print("Time:     " + eventTime)
        print("Location: " + location)
        print("***")

    browser.quit()





if __name__ == '__main__':
    scrapeVPL()







