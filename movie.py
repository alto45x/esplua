from bs4 import BeautifulSoup
import requests
import wget
import urllib2
import urllib
import sys
import shutil
import re


def net21moviemania(link,dl):
    try:
        session_requests = requests.session()
        page = session_requests.get(link, headers = dict(referer = link))
        if page.status_code == 200 :
            bsdata = BeautifulSoup(page.content, 'html.parser')
            datas = bsdata.select("#muvipro_player_content_id")[0].attrs['data-id']
            payload = {'action': 'muvipro_player_content','tab': 'player2','post_id': ''+datas+''}
            #print payload
            try:
                pages =  requests.post('http://21moviemania.site/wp-admin/admin-ajax.php', data = payload)
                bsdatax = BeautifulSoup(pages.content, 'html.parser')
                linksx = bsdatax.find("iframe").attrs['src']
                if  linksx.find("http") != -1:
                    linksdata =  str(linksx).replace('embed','f')
                    print linksdata
                else:
                    linksdata =  str("http:" +linksx).replace('embed','f')
                    print linksdata
            except ValueError as e:
                return e,"salah"
                
    except ValueError as e:
        return e,"salah"
    


if sys.argv != -1:
    try:
        link = str(sys.argv[1])
        #print link
        net21moviemania(link,"data")
        
    except ValueError as e:
        print e