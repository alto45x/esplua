from bs4 import BeautifulSoup
import requests
import wget
import urllib2
import urllib
import sys
import shutil
import demjson
import re
from clint.textui import progress
from google_drive_downloader import GoogleDriveDownloader as gdd

dir_path = "/media/data/TvShow/";

def regpa(url,tag,clas,value):
    page = requests.get(url)
    if page.status_code == 200 :
        soup = BeautifulSoup(page.content, 'html.parser')
        if clas  == "":
            data = soup.findAll(tag)
            return data
        else:
            data = soup.findAll(tag,{clas:value})
            return data
    else:
        return False 
    
class samehada:
    def samehadaku(self,host,link):
        page = requests.get(link)
        if page.status_code == 200 :
            soup = BeautifulSoup(page.content, 'html.parser')
            data = soup.findAll("div", {"class": "download-eps"})[0].findAll("li")[3].findAll("a")
            if str(data).find("http") != -1:
                for i in data :
                    if i.string == host:
                        try:
                            #print i['href'] + "link 1"
                            link =  requests.get(i['href'])
                            soup = BeautifulSoup(link.content, 'html.parser')
                            data = soup.findAll("div", {"class": "download-link"})[0].findAll("a")
                            #print data[0]['href'] + "link 2"
                            links = requests.get(data[0]['href'])
                            soup = BeautifulSoup(links.content, 'html.parser')
                            datax = soup.findAll("div", {"class": "download-link"})[0].findAll("a")
                            #print datax[0]['href'] + "link 3"
                            linkss = requests.get(datax[0]['href'])
                            return linkss.url
                        except: 
                            return "Error"+str(links)
            else:
                #print "li ke 2"
                data = soup.findAll("div", {"class": "download-eps"})[0].findAll("li")[2].findAll("a")
                for i in data :
                    if i.string == host:
                        try:
                            #print i['href'] + "link 1"
                            link =  requests.get(i['href'])
                            soup = BeautifulSoup(link.content, 'html.parser')
                            data = soup.findAll("div", {"class": "download-link"})[0].findAll("a")
                            #print data[0]['href'] + "link 2"
                            links = requests.get(data[0]['href'])
                            soup = BeautifulSoup(links.content, 'html.parser')
                            datax = soup.findAll("div", {"class": "download-link"})[0].findAll("a")
                            #print datax[0]['href'] + "link 3"
                            linkss = requests.get(datax[0]['href'])
                            return linkss.url
                        except: 
                            return "Error"+str(links)
                        
    def makelist(nop,url):
        tag = "li"
        clas = "class"
        value = "post-item"
        data = regpa(url,tag,clas,value)
        linre = []
        for i in data:
            finda = i.findAll('a', href=True)
            href = str(finda[0]['href'])
            linre.append(href)
        return linre
                
                                    
    
link = str(sys.argv[1])
sameha = samehada()

if str(link).find("episode") != -1:
    Gdlink = sameha.samehadaku("GD",link)
    #print Gdlink
    if Gdlink.find("Error") != -1:
        print str(Gdlink)
        try:
            idfile = Gdlink.split('/')
            gdd.download_file_from_google_drive(file_id=idfile[5],dest_path=paths)
        except: 
            False
                    
    else:
        print Gdlink

else:
    data = sameha.makelist(link)
    for i in data:
        #print str(i)
        if str(i).find("episode") != -1:
            strjdl = str(i).split('/')[5].split('-')
            if str(i).find("one-piece") != -1:
                namefile = strjdl[0]+" "+strjdl[1]+"/"+strjdl[0]+" "+strjdl[1]+" "+strjdl[3]+".mkv"
            else:
                namefile = strjdl[0]+"/"+strjdl[0]+" "+strjdl[1]+" "+strjdl[2]+".mkv"
            
            paths = dir_path + namefile
            Gdlink = sameha.samehadaku("GD",str(i))
            #print Gdlink
            if Gdlink.find("Error") != -1:
                print str(Gdlink)
                try:
                    idfile = Gdlink.split('/')
                    gdd.download_file_from_google_drive(file_id=idfile[5],dest_path=paths)
                except: 
                    False
                    
            else:
                print Gdlink