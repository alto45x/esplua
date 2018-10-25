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
from bs4 import BeautifulSoup

def downloader(link,file_name):
    mozilla_header={'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
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
    
def openloadx(links):
    display = Display(visible=0, size=(800, 600))
    display.start()

    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    try:
        driver.get(links)
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
    
def layarindo21(link,host,file):
    gclo = "https://gugcloud.club/videoplayback?id="
    try:
        
        session_requests = requests.session()
        page = session_requests.get(link, headers = dict(referer = link))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            datas = bsdata.findAll('div', attrs={'id':'telolet'})[0]['data-telolet']
            try:
                links = gclo+datas
                #print links
                data = requests.get(links, headers = dict(referer = link))
                databs = BeautifulSoup(data.content, 'html.parser')
                value = databs.find_all("script")[2].string
                if value.find("video/mp4") != -1:
                    
                    stjson = value[value.find("360p")-11:value.find("tracks")-11]
                    json_de = demjson.decode(stjson)
                    #print str(stjson)
                    if len(json_de) == 4:
                        linkss = json_de[3]['file']
                    else:
                        linkss = json_de[len(json_de)-1]['file']
                    #print str(json_de)
                    r = requests.get(linkss, stream=True)
                    if r.status_code == 403:
                        openload = value[value.find("fixerror")+11:len(value)-13]
                        fh = open("openloadmovie.txt", "a")
                        fh.write(openload)
                        fh.write("\n\r")
                        fh.close
                        print str(openload)
                    else:
                            print r.status_code
                            with open(file, 'wb') as f:
                                total_length = int(r.headers.get('content-length'))
                                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                                    if chunk:
                                        f.write(chunk)
                                        f.flush()
                
                else:
                    print "null"
                    
                
            except ValueError as e:
                return e,"salah"
                
    except ValueError as e:
        return e,"salah"
    

def net21moviemania(link,host,file):
    try:
        pydata = 'http://'+host+'/wp-admin/admin-ajax.php'
        session_requests = requests.session()
        page = session_requests.get(link, headers = dict(referer = link))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            datas = bsdata.select("#muvipro_player_content_id")[0].attrs['data-id']
            print datas
            payload = {'action': 'muvipro_player_content','tab': 'player2','post_id': ''+datas+''}
            #print payload
            try:
                
                #print pydata
                pages =  requests.post(pydata, data = payload)
                bsdatax = BeautifulSoup(pages.content, 'html.parser')
                linksx = bsdatax.find("iframe").attrs['src']
                if  linksx.find("http") != -1:
                    linksdata =  str(linksx).replace('embed','f')
                    print linksdata
                else:
                    linksdata =  str("http:" +linksx).replace('embed','f')
                    print linksdata
                if linksdata.find("load") != -1:
                    try:
                        openloadx(linksdata)
                    except ValueError as e:
                        print str(e)
            except ValueError as e:
                return e,"salah"
                
    except ValueError as e:
        return e,"salah"
    


if sys.argv != -1:
    try:
        link = str(sys.argv[1])
        aslink  = link.split('/')
        host = aslink[2]
        file = aslink[3]+".mp4"
        if str(host).find("moviemania") != -1:
            net21moviemania(link,host,file)
        elif str(host).find("layarindo21") != -1:
            layarindo21(link,host,file)
        elif str(host).find("indoxx1") != -1:
            net21moviemania(link,host,file)
            
    except ValueError as e:
        print e