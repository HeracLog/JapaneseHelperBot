import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options 
from bs4 import BeautifulSoup as soup
from download import downloadImages

link : str = "https://japanesepod101.tumblr.com/"

fireFox_Options = Options()
fireFox_Options.add_argument("-headless")

driver : webdriver = webdriver.Firefox(options= fireFox_Options)

print("Started driver")
driver.get(link)

wait_time : int = 2

imgsFile = open("imgs.txt","w")
turns : int= 0
try:
    while turns <  100:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)
        souped_Data = soup(driver.page_source,"lxml")
        imgs : list = [s.get("src") for s in ((souped_Data.find("section",{"id":"posts"})).find("div",{"class":"main"})).find_all("img")]
        print(len(imgs))
        turns+=1

    imgsFile.write(str(imgs))
except Exception as e:
    print("oopsie ",e)
driver.quit()
print("Session ended")
downloadImages()