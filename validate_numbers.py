import requests
import io
import sys, os
from time import sleep
import threading
import re
import random
import string

path = 'proxyscrape_premium_socks_proxies.txt'
f = open( path ,'r')
proxies = {}
num = 0
for x in f:

    proxies[ num ] = x.replace('\n','')
    # print( str( num + 1 ) + ' ' + str( proxies[ num ] ) )
    num = num + 1

l = len( proxies )
f.close()

def GetProxy( p ):
    print( p )


def Ping( proxy, number ):

    post_url = 'https://www.ipqualityscore.com/phone-number-validator/lookup/HU/'


    proxiesDict = {
        'http' : "socks5://1.2.3.4:1080",
        'https' : "socks5://1.2.3.4:1080"
    }

    number = ''

    post = { 'phone': number }

    requests.post( post_url, data = post, proxies = proxiesDict )


for x in range( 1 ):

    ip = proxies[ x ]
    proxiesDict = {

        'http' : "socks5://" + str( ip ),
        'https' : "socks5://" + str( ip )

    }
    try: 
        #url ='https://www.ipqualityscore.com/phone-number-validator/lookup/HU/number'
        #url = 'https://www.instagram.com/data/shared_data/'
        #url = 'https://ident.me'
        url = 'https://facebook.com'
        #'https://api.ipify.org?format=json'
        #{"ip":"188.156.168.166"}
        s = requests.Session()
        r = s.get( url, proxies = proxiesDict, timeout = 5 )
        with io.open( "test.html", "w", encoding="utf-8" ) as f:
            f.write(r.text)
            f.close()
        #print( r.text )
    except:
        print( 'Error TIMEOUT: ' + str( ip ) )

