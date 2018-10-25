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

gclo = "https://gugcloud.club/videoplayback?id="


def job(url,filename):
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    f.write(u.read())
    f.close()
    
def downloader(link,file_name):
    r = requests.get(link, stream=True)
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
    

    
def net21moviemania(link,host,file):
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
                stjson = value[value.find("autostart")+43:value.find("tracks")-11]
                json_de = demjson.decode(stjson)
                #print len(json_de)
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
        net21moviemania(link,host,file)
        
    except ValueError as e:
        print e