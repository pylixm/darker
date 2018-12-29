# -*-coding:utf-8 -*-
import os
import urllib2
import json
import requests

def lib_post( url, data={} ):
    """
    # 使用urllib调用restfull方式的接口
    """
    headers = {"Content-type":"application/json","Accept": "application/json"}
    params = json.dumps(data) if data else {}
    myreq = urllib2.Request(url, params, headers)
    response = urllib2.urlopen( myreq )
    return json.loads( response.read() )
    
def lib_get( url ):
    """
    # 使用urllib调用restfull方式的接口
    """
    myreq = urllib2.Request( url ) 
    response = urllib2.urlopen( myreq )
    return response.read()
    

def testUseRequest( url, data={}, method= 'get' ):
    """
    # 使用request调用restfull方式的接口
    """
    headers = {"Content-type":"application/json","Accept": "application/json"}
    if method=='post':
        if data :
            myreq = requests.post(url, json.dumps(data), headers)
        else:
            myreq = requests.post(url, headers)   
    else:
        if data:
            myreq = requests.get( url , params = data )
        else:
            myreq = requests.get(url, headers)
    with open('test.txt','wb') as file:
        file.write( myreq.content  )
        
    return myreq
    

if __name__=='__main__':
    #data = {'format_dic':{
    #    'asset__id' : ['3,56,1009,198,65', 'in'],
    #    'update_at' : ['2014-12-08,2014-12-11', 'range'],
    #    'manufactory' : ['Dell Inc.', 'contains'],
    #    'cpu_count' : [2, 'gt'],
    #    'ram_size' : [128, 'gt'],  
    #    'page_navi': [6,6]}    
    #    } 
    ##testUseurllib( url, data )
    ##print lib_get( url )
    ##print lib_post( url )
    #data = {'filter_keys': json.dumps({'asset_id':4923}) }
    #print testUseRequest( url, data )
    #?datalist='["4923"]'&type=0&appname=mall_web

    url = "http://10.168.8.26:8000/api/v1.0/users/"
    data = {
        'type':1, 
        'appname':'mall_web',
         }
    resp = testUseRequest( url, data )
    print "ResponseData>>:", resp.text 
    print "status>>>>>>>>:",resp.status_code
    print "headers>>>>>>>:",resp.headers
    print time_stamp
    print ssig 
