import re
import random
import string
import time
import sys
import os, platform
import io
import threading

import fb_bot

def GetProxies():
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
    return proxies

def GetProxy( k ):
    proxies = GetProxies()
    return proxies[ k ]

def LookUpPhone( number, isproxy=True, name='' ):
    fb = fb_bot.Facebook()
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
    threads_count = 20
    index = 0
    if os.path.exists('./index'):
        with io.open( "index", "r", encoding="utf-8" ) as f:
            index = int(f.read() )

    sleep = 0.05
    
    for x in range( index, 89998 - 1 ):

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

test4()