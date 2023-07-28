import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options 
from bs4 import BeautifulSoup as soup
from download import downloadImages


# Link to be scraped 
# Shouldnt change for this use
link : str = "https://japanesepod101.tumblr.com/"

# Added the option to start firefox in headless mode
fireFox_Options = Options()
fireFox_Options.add_argument("-headless")

# Creates driver to be used
driver : webdriver = webdriver.Firefox(options= fireFox_Options)

# Gets the link
print("Started driver")
driver.get(link)

# Waits for 2 seconds
# In general the minimum is 1 as by the websites robots.txt
wait_time : int = 2

# Opens an image file to save the links to
# Yes I could have just passed the list as an argument but im sleep deproved so do it yourself smh
imgsFile = open("imgs.txt","w")
# Turns to scrape the link
# Not really smart i could just compare the link height but oh well
turns : int= 0
# Tries to get all the image links
try:
    while turns <  100:
        # Scrolls to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Sleeps to give it time
        time.sleep(wait_time)
        # Soups the page source
        souped_Data = soup(driver.page_source,"lxml")
        # Gets all the image links from the source
        imgs : list = [s.get("src") for s in ((souped_Data.find("section",{"id":"posts"})).find("div",{"class":"main"})).find_all("img")]
        # Prints number of images in the list and increments the turns variable
        print(len(imgs))
        turns+=1

    # After the loop we write the list to a file
    # Yes I could have serialized it but I will do all these fixes laterrrr
    imgsFile.write(str(imgs))
# In case of an exception it logs it out
except Exception as e:
    print("oopsie ",e)
# Quits the driver
driver.quit()
print("Session ended")
# Starts to download the images
downloadImages()