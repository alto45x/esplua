from bs4 import BeautifulSoup
import requests
import sys
import json
import re
import subprocess
import os
from clint.textui import progress
from time import sleep
import jsbeautifier
import string
from pySmartDL import SmartDL
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display


    
iiframelisted = []
gdirvefile = []
dir_download = "/home/kodokijo/tmp/"
nas_dir = "/media/hdd1/Tv_Show"
pathx = "/home/kodokijo/dl/"
via = "oxp"

ua = UserAgent()

is_download = "yes"
digs = string.digits + string.ascii_letters
#mozilla_header={'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
mozilla_header={'User-Agent':''+ua.random+''}
#print (str(mozilla_headerx))
API_ENDPOINT = "http://drmq.stream/v3/loader.php"
api_dl = "https://drmq.stream/cdn/loader-download.php"
api_link = "https://spolak.info/api/source/"


session_requests = requests.session()
hf =  ""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def downloaderx(link,file_name,ext):
    if ext != "" :
        ext= "."+ext
    else:
        ext = ""
    
    if str(file_name).find("Ep.") != -1:
        dir_name = str(file_name).split("-Ep.")[0]
    else:
        dir_name = file_name
    path = nas_dir +"/"+dir_name+"/"+file_name+ext
    print (bcolors.OKGREEN+"Proses  : "+path+bcolors.ENDC)
    dir_dl = nas_dir +"/"+dir_name+"/"
    if not os.path.exists(dir_dl):
        #print (str(path[:-4]))
        os.makedirs(dir_dl)
    obj = SmartDL(link, dir_dl)
    obj.start()
    pathx = obj.get_dest()
    os.rename(pathx,path)
    print (bcolors.OKGREEN+"Proses  : "+path+bcolors.ENDC)
    try:
        if str(pathx).find("srt") != -1:
            mp4s = nas_dir +"/"+dir_name+"/"+file_name+".mp4"
            srtx = nas_dir +"/"+dir_name+"/"+file_name+".srt"
            print (bcolors.OKGREEN+"Proses  : "+mp4s+bcolors.ENDC)
            print (bcolors.OKGREEN+"Proses  : "+pathx+bcolors.ENDC)
            mkvs = nas_dir +"/"+dir_name+"/"+file_name+".mkv"
            if os.path.exists(mp4s):
                print (bcolors.OKGREEN+"Proses  : Coverting MKV"+bcolors.ENDC)
                convet(str(mkvs),mp4s,str(srtx))                
        else:
            print (bcolors.OKGREEN+"Proses  : "+pathx+bcolors.ENDC)
            #print (bcolors.OKGREEN+"Proses  : "+pathx+bcolors.ENDC)
    except ValueError as e:
        print (bcolors.FAIL+"Proses  : Fail Conver"+str(e)+bcolors.ENDC)

def downloader(link,file_name,ext):
    try:
        if str(file_name).find("Ep.") != -1:
            dir_name = str(file_name).split("-Ep.")[0]
        else:
            dir_name = file_name
        path = nas_dir +"/"+dir_name+"/"+file_name+"."+ext
        dir_dl = nas_dir +"/"+dir_name+"/"
        if not os.path.exists(dir_dl):
            #print (str(path[:-4]))
            os.makedirs(dir_dl)
        r = requests.get(link, stream=True,headers=mozilla_header)
        if r.status_code == 403:
            return -1
        else:
            print ("Downloader :  "+file_name)
            print ("Downloader :  Downloading Data "+str(ext))
            try:
                with open(path, 'wb') as f:
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
            except ValueError:
                pass
        try:
            if str(ext) == ("srt"):
                mp4s = nas_dir +"/"+dir_name+"/"+file_name+".mp4"
                print ("Proses  : "+bcolors.OKGREEN+mp4s+bcolors.ENDC)
                print ("Proses  : "+bcolors.OKGREEN+path+bcolors.ENDC)
                mkvs = nas_dir +"/"+dir_name+"/"+file_name+".mkv"
                if os.path.exists(mp4s):
                    print ("Proses  : "+bcolors.OKGREEN+"Coverting MKV"+bcolors.ENDC)
                    convet(mkvs,mp4s,str(path))                
        
        except ValueError as e:
            print (bcolors.FAIL+"Proses  : Fail Conver"+str(e)+bcolors.ENDC)
    except ValueError as e:
        pass
        print (bcolors.FAIL+"Proses  : Fail Conver"+str(e)+bcolors.ENDC)   
def openloadx(links,filenamex):
    display = Display(visible=0, size=(800, 600))
    display.start()
    print ("openloadx :  Display start")
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')  
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    try:
        print ("openloadx :  Get link")
        driver.get(links)
        if str(driver.title).find("mp4") != -1 :
            try:
                elem = driver.find_element_by_css_selector('.other-title-bold')
                print ("openloadx :  Openload "+str(elem.text))
                filename=elem.text
            except:
                pass
                filename = "openload.mp4"
                
            driver.execute_script("document.getElementById('btnDl').click()")
            print ("openloadx :  Openload  Klikked")
            
            while(len(driver.window_handles)>1):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            sleep(6)
            driver.execute_script("document.getElementById('secondsleftouter').click()")
            button=driver.find_element_by_css_selector('#realdl')
            print ("openloadx :  Click to start  Klikked")
            #sleep(6)
            #button.click()
            while(len(driver.window_handles)>1):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            button=driver.find_element_by_css_selector('a.main-button:nth-child(1)')
            downloadurl=button.get_attribute('href')
            driver.close()
            os.system("killall -9 chromedriver")
            display.stop()
            print ("openloadx :  Openload Link "+str(downloadurl))
            
            if str(downloadurl).find("http") != -1:
                print ("openloadx :  "+bcolors.OKGREEN+"Downloading" )
                downloader(downloadurl,filenamex,"mp4")
                print(bcolors.ENDC)
        else:
            print (bcolors.FAIL+"Proses  : Fail "+str(driver.title)+bcolors.ENDC)
            
    except ValueError as e:
        pass
        print (bcolors.FAIL+"Proses  : Fail 2"+str(e)+bcolors.ENDC)
        

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def unpack(p, a, c, k, e=None, d=None):
    while (c):
        c-=1
        if (k[c]):
            p = re.sub("\\b" + baseN(c, a) + "\\b",  k[c], p)
    return p
    
def cekep(link):
    try:        
        page = session_requests.get(link, headers = dict(referer = link))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            datas = bsdata.select("#action-parts")[0].findAll("a")
            return str(len(datas))
    except ValueError as e:
        return e,"salah" 

def getsrtlink(link):
    try:
        page = session_requests.get(link, headers = mozilla_header)
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            title = str(bsdata.find_all("div", class_="title")[0].find("h1").text).replace(" ","-")
            poster = str(bsdata.find_all("div", class_="poster")[0].find("img")['src'])
            #downloader(poster,"folder","jpg")
            return str(title+"|"+poster)
    except ValueError as e:
        return e,"salah" 

        
            
def getiframelink(link,xxc):
    #print (str("Sini def getiframelink"))
    try:
        
        page = session_requests.get(link, headers = dict(referer = link))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            datas = str(bsdata.find_all("div", class_="video-container"))
            #print (str(datas))
            if datas.find("unescape") != -1:
                datastrx =  str(datas[datas.find('unescape( "%')+11:datas.find("/div")-26]).replace("%","")
                if str(datastrx).find(")") != -1:
                    datastrx = str(str(datastrx)[0:str(datastrx).find('" )')-2])
                    #print (str(datastrx))
                datastrx = (bytearray.fromhex(datastrx).decode())
                #print (str(datastrx))
                datastr = BeautifulSoup(datastrx, 'html.parser').find_all("a", class_="btnxy")
                #print (str(datastr[xxc].attrs['href']))
                if str(xxc) != "hls" :
                    try:
                        hf = (str(datastr[0].attrs['href']))
                        data = prosescekliks(str(datastr[0].attrs['href']),link,hf)
                        return data
                    except ValueError as e:
                        return str(e)
                else:
                    hlslink(str(datastr[2].attrs['href']))
            else:
                print (datas)
           

    except ValueError as e:
        print ("error"+str(e))

def prosescekliks(datastr,link,hf):
    srt = ""
    #print (str("Sini def prosescekliks"))
    try:
        #print datastr
        page = session_requests.get(datastr, headers = dict(referer = hf))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            #print (str(bsdata)+"sini")
            try:
                scripl = bsdata.find_all("script")
                #print (len(scripl))
                for i in scripl:
                    if len(str(i))> 500:
                        if str(i).find("Player_Load") != -1:
                            Player_Load = str(i)[str(i).find("Player_Load")+12:str(i).find("if(typeof  FuckA")-21].replace('"',"").split(",")
                            #print (str(Player_Load))
                            srt = Player_Load[1]
                            API_KEY = str(Player_Load[0])
                            #print (API_KEY)
                            # data to be sent to api 
                            data = {'id':API_KEY} 
                            #print (str(data))
                            # sending post request and saving response as response object 
                            r = requests.post(url = API_ENDPOINT, data = data) 

                            # extracting response text 
                            pastebin_url = str(r.text )
                            y = json.loads(pastebin_url)
                            #print(str(y))
                            jsonx = str(y[0]['file'])
                            datax = str(jsonx)+"|"+srt+"|"+API_KEY
                            return str(datax)
                            
            except ValueError as e:
                return ("error s")
        else:
            return ("dis")
    except  ValueError as e:
        return ("error x")
        
def hlslink(links):
    try:
        print (str(links))
        page = session_requests.get(links, headers = dict(referer = links))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            print (str(bsdata)[str(bsdata).find("Download_Load")+15:str(bsdata).find(" });")-5])
            
    except  ValueError as e:
        return (e)

def convet(out,movieName, subtitleName):
    try:
        command = "mkvmerge -q -o "+str(movieName[0:-3]+"mkv")+" "+movieName+" "+subtitleName
        print ("Proses  : Converting "+bcolors.OKGREEN+str(command)+bcolors.ENDC)
        subprocess.call(command.split(), shell=False)
        subprocess.call(["rm", movieName, subtitleName])
        return (bcolors.OKGREEN+"Proses  : Done Conver"+str(out)+bcolors.ENDC)
    except ValueError as e:
        return (bcolors.FAIL+"Proses  : Fail Conver"+str(out)+bcolors.ENDC)


def spolax(api_data,filename,ext,srt):
    try:
        print ("Proses  : "+bcolors.OKGREEN+str(srt)+bcolors.ENDC)
        url = api_link+api_data
        data = {'data':'data'} 
        r = requests.post(url = url, data = data)
        if r.status_code == 200:
            y = json.loads(str(r.text))
            if not str(y['data']).find("We") != -1:
                links = str(y['data'][0]['file'])
                print ("Proses  : "+bcolors.OKGREEN+str(links)+bcolors.ENDC)
                downloader(links,filename,ext)
                print ("Proses  : "+bcolors.OKGREEN+"Done"+bcolors.ENDC)
                downloader(srt,filename,"srt")
            else:
                 print ("Proses  : "+bcolors.FAIL+"Gagal "+str(y['data'])+bcolors.ENDC)      
    except ValueError as e:
        return (bcolors.FAIL+"Proses  : Fail Conver"+str(out)+bcolors.ENDC)       

        
def dramaqunet(link,skip):
    print (bcolors.OKGREEN+"Proses  : Starting Proses "+bcolors.ENDC)
    try:
        srtlink = getsrtlink(link)
    except ValueError as e:
        srtlink = ""
        print ("Proses  : Ceking Episode Of "+bcolors.OKGREEN+namefile+bcolors.ENDC)
    if len(srtlink) >10:
        namefile = str(srtlink.split("|")[0])
    else:
        namefile = link.split("/")[3].replace("/","").replace("nonton-","").replace("indonesia","").replace("subtitle-","")
    
    #print ("Proses  : Ceking Episode Of "+bcolors.OKGREEN+namefile+bcolors.ENDC)
    lenep = int(cekep(link))+1
    print ("Proses  : Episode is "+bcolors.OKGREEN+str(lenep)+bcolors.ENDC)
    print ("Proses  : Geting Iframe link")
    
    if skip > 1:
        xc = int(skip)
        
        print ("Proses  : Skip to Ep "+bcolors.WARNING+str(skip)+bcolors.ENDC)
    else:
        xc = 1
    
    xl = 1
    namefilez = pathx + namefile
    f= open(namefilez+"GriveID.txt","w+")
    for x in range(xc, lenep+1):
        sleep(5)
        try:
            links = link +"/"+(str(x))+"/"
            if x == 1 :
                links = link+"/"
                
            namefilex = str(namefile+"-Ep."+str(x)).replace(" ","-")
            #print(links)
            #print ("Proses  : "+str(x)+"/"+str(lenep)+" Episode" )
            
            iframelink = getiframelink(links,0)
           
            #print (str(iframelink))
            print ("Proses  : Ceking Episode Of "+bcolors.OKGREEN+namefile+" Ep "+str(x)+bcolors.ENDC)
            print (bcolors.OKGREEN+"Proses  : cek link 1"+bcolors.ENDC)
            if str(iframelink).find("videoplayback") != -1 :
                if str(iframelink) is not None:
                    linkas = str(iframelink).split("|")
                    try:
                        #print (str(linkas[0]))
                        if str(linkas[0]).find("videoplayback") != -1 :
                            print (bcolors.OKGREEN+"Proses  : ada http "+bcolors.ENDC)
                            srt = str(linkas[1]).split(".srt")[0]+".srt"
                            if is_download == "yes" :
                                print ("Proses  : "+str(iframelink)[0:25]+"  Link")
                                print ("Proses  : Downloadding  Ep "+namefilex +".mp4")
                                downloaderx(linkas[0],namefilex,"mp4")
                                print ("Proses  : mp4 Done")
                                downloaderx(srt,namefilex,"srt")
                                print ("Proses  : "+srt+" Done")
                            f.write(str(x)+"|"+str(linkas[0])+"|"+srt+"\n")
                            xl = 0
                        else:
                            print (bcolors.FAIL+"Proses  : link 1 no http"+bcolors.ENDC)
                    except ValueError as e:                    
                        print (bcolors.FAIL+"Proses  : Download  Ep "+namefilex+ "Gagal"+bcolors.ENDC)
                else:
                    pass
                #print linkas[1]
                print ("Proses  : Download  Ep "+bcolors.OKGREEN+namefilex+bcolors.ENDC+" Done")
                
            else:
                sleep(10)
                try:
                    
                    print (bcolors.FAIL+"Proses  : Fail Link 1 "+str(iframelink)[0:10]+bcolors.ENDC)
                    print (bcolors.OKGREEN+"Proses  : cek link 2"+bcolors.ENDC)
                    kay = iframelink.split("|")[2]
                    srt = iframelink.split("|")[1]
                    srt = str(srt).split(".srt")[0]+".srt"
                    print ("Proses  : "+bcolors.OKGREEN+srt+bcolors.ENDC)
                    #print (str(kay))
                    data = {'id':kay} 
                    r = requests.post(url = api_dl, data = data) 
                    bsdata = BeautifulSoup(r.content, 'html.parser')
                    a = bsdata.findAll("a")
                    #print (a[]['href'])
                    for ai in a:
                        if str(via) == "op":
                            if str(ai).find("openload") != -1:
                                print ("Proses  : "+str(ai['href']))
                                openloadx(str(ai['href']),namefilex)
                                downloader(srt,namefilex,"srt")
                        else:
                            if str(ai).find("spolak") != -1:
                                idkay = str(ai['href']).split("/f/")[1]
                                print ("Proses  : "+bcolors.OKGREEN+idkay+bcolors.ENDC)
                                spolax(idkay,namefilex,"mp4",srt)
                except ValueError as e:      
                    print (bcolors.FAIL+"Proses  : Fail 2"+str(e)+bcolors.ENDC)
                    pass
               
        except ValueError as e:
            print ("Proses  : Not Done ")
            pass  
        xc = xc +1
    
    f.close()
    print ("Proses  : Done Geting data")

    
try:
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        skip = sys.argv[2]
        dramaqunet(url,int(skip))
    else:
        url = str(sys.argv[1])  
        dramaqunet(url,0)   
except KeyboardInterrupt:
    pass 