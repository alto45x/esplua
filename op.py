import requests
import wget
import urllib2
import urllib
import sys
import shutil
import demjson
import re
import time
from selenium import webdriver
from pyvirtualdisplay import Display
from clint.textui import progress
import os


display = Display(visible=0, size=(800, 600))
display.start()

mozilla_header={'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
def downloader(link,file_name):
    r = requests.get(link, stream=True,headers=mozilla_header)
    if r.status_code == 403:
        return -1
    else:
        print r.status_code
        with open(file_name, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()

driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  # Optional argument, if not specified will search path.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


# or '/usr/lib/chromium-browser/chromedriver' if you use chromium-chromedriver
try:
    driver.get("http://oload.stream/f/wzQmx-tue-k/")
    elem = driver.find_element_by_css_selector('.other-title-bold')
    print str(elem.text)
    filename=elem.text
    button=driver.find_element_by_css_selector('#btnDl')
    print str(button.text)
    button.click()
    while(len(driver.window_handles)>1):
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(6)
    button=driver.find_element_by_css_selector('span#secondsleftouter')
    print str(button.text)
    button.click()
    while(len(driver.window_handles)>1):
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    button=driver.find_element_by_css_selector('a.main-button:nth-child(1)')
    downloadurl=button.get_attribute('href')
    driver.close()
    os.system("killall -9 chromedriver")
    display.stop()
    print str(downloadurl)
    downloader(downloadurl,filename)
except ValueError as e:
    print e,"salah"
