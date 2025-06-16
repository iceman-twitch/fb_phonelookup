from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
from requests.auth import HTTPProxyAuth
import re
import random
import string
import time
import sys
import os, platform
import io
from bs4 import BeautifulSoup
from lxml import html
import threading

ua = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
]


path = 'proxyscrape_premium_socks_proxies.txt'
f = open( path ,'r')
valid_proxy = {}
num = 0
for x in f:

    valid_proxy[ num ] = x.replace('\n','')
    # print( str( num + 1 ) + ' ' + str( proxies[ num ] ) )
    num = num + 1

l = len( valid_proxy )
f.close()

proxy_username = ''
proxy_password = ''

class Facebook:
    def __init__( self ):
        self.version = 'None'

    def SetupSession( self ):
        self.s = requests.Session()

    def GetUserAgent( self ):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]   
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        #return user_agent_rotator.get_random_user_agent()
        return random.choice( ua )

    def GetProxy( self ):
        return random.choice(valid_proxy)

    def LookUpPhone( self, number, isproxy = False, lookupname = '' ):
        self.SetupSession()
        fb = 'https://www.facebook.com'
        rec = 'https://www.facebook.com/login/identify/?ctx=recover&ars=royal_blue_bar'
        m_rec = 'https://m.facebook.com/login/identify/?ctx=recover&c=https%3A%2F%2Fm.facebook.com%2F&multiple_results=0&from_login_screen=0&_rdr'

        s1 = self.s.get(fb)
        s2 = self.s.get(m_rec)
        datr = s2.cookies.get_dict()['datr']
        sb = s1.cookies.get_dict()['sb']
        fr = s1.cookies.get_dict()['fr']
        soup = BeautifulSoup( s2.text,'html.parser' )
        lsd = soup.find('input', {'name': 'lsd'}).get('value')
        #print("lsd: " + lsd)
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        #print("jazoest: " + jazoest)
        did_submit = soup.find('input', {'name': 'did_submit'}).get('value')
        #print("did_submit: " + did_submit)
        #print( "Address: " + number )
        useragent = self.GetUserAgent()
        headers = {
            'Origin': 'https://m.facebook.com',
            'Upgrade-Insecure-Requests':	'1',
            'DNT':	'1',
            'Content-Type':	'application/x-www-form-urlencoded',
            'User-Agent':	useragent,
            'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'cookie': 'sb=' + sb + '; fr=' + fr + '; datr=' + datr + '; m_pixel_ratio=1; wd=2520x939; locale=hu_HU',
            'Sec-Fetch-Site':	'same-origin',
            'Sec-Fetch-Mode':	'navigate',
            'Sec-Fetch-User':	'?1',
            'Sec-Fetch-Dest':	'document'
        }
        myobj = {
        'did_submit': did_submit,
        'email': number,
        'jazoest': jazoest,
        'lsd': lsd
        }
        if isproxy:
            server = self.GetProxy()
            #proxy = {'https': "socks5://" + proxy_username + ":" + proxy_password + "@" + server + ":1080" }
            proxy = { 
                'http': 'socks5://' + server,
                'https': 'socks5://' + server 
            }
            l = requests.post('https://m.facebook.com/login/identify/?ctx=recover&search_attempts=1&alternate_search=0', data = myobj, headers=headers, proxies=proxy )
        else:
            l = requests.post('https://m.facebook.com/login/identify/?ctx=recover&search_attempts=1&alternate_search=0', data = myobj, headers=headers)
        l.raise_for_status()
        #print( 'Status Code: ' + str( l.status_code ) )
        tree = html.fromstring( l.content ) #printing element
        result = tree.xpath( '/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/text()' ) #printing Result
        if len(result) > 0:
            #with io.open( "found/" + number + ".html", "w", encoding="utf-8") as f:
            #    f.write(l.text)
            #    f.close()
            print( 'Status Code: ' + str( l.status_code ) + ' | Name: ' + result[0] )
            avatar = tree.xpath( '/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/i/style' )
            #print( str(avatar) )
            #if len(avatar) > 0:
                #print( 'Avatar: ' + str(avatar[0]) )
            #if lookupname == result[0]:
                #print('Found Profile with Phone Number')
        else:
            with io.open( "notfound/" + number + ".html", "w", encoding="utf-8") as f:
                f.write(l.text)
                f.close()
            print( 'Status Code: ' + str( l.status_code ) + ' | No Person Found: ' + number )
        
        
        # //*[@id="root"]/div[2]/div/div/div[1]/i # Avatar or Something
        # //*[@id="root"]/div[2]/div/div/div[2]/div # To Get The Name or Something
        
        #if lookupname != '':
        #    if lookupname in l.text:
        #        print('Found Profile with Phone Number')

#if __name__ == "__main__":
def test():
    fb = Facebook()
    fb.LookUpPhone( 'number', False, 'name' )
    time.sleep(3)

def write_list():
    b = list(range(10001, 99999))
    #shuffle(b)
    try:
        f = open('list.txt','w')
        for x in b:
            try:
                f.write( str(x) + '\n')
            except:
                pass
        f.close()
    except:
        pass

def test2():
    tmb = {}
    f = open('list.txt','r')
    num = 0
    for x in f:
        try:
            tmb[num] = x
            num = num + 1
        except:
            pass
    print( len( tmb ) )
    print( random.choice( tmb ) )
    f.close()

def test3():
    tmb = {}
    f = open('list.txt','r')
    num = 0
    for x in f:
        try:
            tmb[num] = x
            num = num + 1
        except:
            pass

    key = random.randint( 0, 89998 - 1 )
    fb = Facebook()
    #fb.LookUpPhone( random.choice( tmb ).replace('\n','')  )
    print( 'Key: ' + str( key ) )
    fb.LookUpPhone( tmb[ key ].replace('\n','')  )


def LookUpPhone( number, isproxy=False, name='' ):
    fb = Facebook()
    fb.LookUpPhone( number, isproxy, name  )


def test4():
    tmb = {}
    f = open('list.txt','r')
    num = 0
    for x in f:
        try:
            tmb[num] = x.replace('\n','')
            num = num + 1
        except:
            pass
    l = len( tmb )
    threads = {}
    threads_count = 10
    index = 0
    if os.path.exists('./index'):
        with io.open( "index", "r", encoding="utf-8" ) as f:
            index = int(f.read() )

    sleep = 0.2

    for x in range( index, 100 ):

        for y in range( 0, threads_count - 1 ):
            threads[y] = threading.Thread( target = LookUpPhone, kwargs = { 'number': tmb[ index ] } )
            index = index + 1
            with io.open( "index", "w", encoding="utf-8") as f:
                f.write( str(index) )
                f.close()
            time.sleep( sleep )
        
        for y in range( 0, threads_count - 1 ):
            threads[y].start()
            time.sleep( sleep )
        
        for y in range( 0, threads_count - 1 ):
            threads[y].join()
            time.sleep( sleep )


write_list()
#test4()