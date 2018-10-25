from bs4 import BeautifulSoup
import requests
import wget
import urllib2
import urllib
import sys
import shutil
import re


def net21moviemania(link,host):
    try:
        
        req = urllib2.Request(link)
        content = urllib2.urlopen(req).read()
        if content != "" :
            bsdata = BeautifulSoup(content, 'html.parser')
            datas = bsdata.select("#jw-video")
            file = open(host+'.txt','w') 
            file.write(str(bsdata)) 
            file.close()

                
    except ValueError as e:
        return e,"salah"
    

link = "https://cat3korean.com/japan-18/good-execution-substitute-wife-2017.html"
aslink  = link.split('/')
host = aslink[2]
net21moviemania(link,host)
