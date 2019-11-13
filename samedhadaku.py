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
def slinks(link):
    print ("Deep link 1")
    try:
        link =  requests.get(link)
        soup = BeautifulSoup(link.content, 'html.parser')
        form = soup.findAll("form")
        #print (str(form))
        input = soup.findAll("input")
        value =  str(input[0]['value'])
        url = str(form[0]['action'])
        name  = str(form[0]['name'])
        API_ENDPOINT = str(form[0]['action'])
        try:
            datax = {'eastsafelink_id':value} 
            r = requests.post(url = API_ENDPOINT, data = datax)
            soup = BeautifulSoup(r.content, 'html.parser')
            data = soup.findAll("script")
            for i in data:
                if str(i).find("generate") != -1:
                    slink = str(i)[str(i).find("a='")+3:str(i).find("';window")]
                    if str(slink).find("http") != -1:
                        return str(slink)
                    else:
                        return str("No link")
        except ValueError as e: 
            return ("Error"+str(e))
    except ValueError as e: 
        return ("Error"+str(e))
        
def slinkss(link):
    print ("Deep link 2")
    try:
        link =  requests.get(link)
        soup = BeautifulSoup(link.content, 'html.parser')
        data = soup.findAll("a")
        #print (len(data))
        for i in data:
            if str(i).find("?r=") != -1:
                link =  requests.get(str(i['href']))
                return (str(link.url))
            
    except ValueError as e: 
        return ("Error"+str(e)) 

        
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
                           
                            link =  slinks(i['href'])
                            linkss = slinkss(link)
                            return linkss
                        except: 
                            return "Error"+str(links)
            else:
                #print "li ke 2"
                data = soup.findAll("div", {"class": "download-eps"})[0].findAll("li")[2].findAll("a")
                for i in data :
                    if i.string == host:
                        try:
                            link =  slinks(i['href'])
                            linkss = slinkss(link)
                            return linkss
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