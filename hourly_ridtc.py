#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

import requests
import pymongo
from datetime import datetime

nowja = datetime.now()

myclient = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")
mydb = myclient["wma_test"]
mycol = mydb["wma89"]

station_id = [1,2,3,4,5,6,7,8,9]
counter = 0 

while (counter < len(station_id)):
    url = "http://wq-thachin.rid.go.th/api/stat?siteId="+str(station_id[counter])+"&period=60&fromDate="+str(nowja.year)+"-"+str(nowja.month)+"-"+str(nowja.day)+"&toDate="+str(nowja.year)+"-"+str(nowja.month)+"-"+str(nowja.day+1)
    payload={}
    headers = {
        'Cookie': 'sessionId=s%3AFZC3Gl06ksNv_WdqQgnGEI5VX7HcZu9N.b3tcMb5%2BnjUb%2BqnwEiQOiD%2BbdiH%2Bs7gxs4Pv3rYinq4'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    counter = counter+1

    eiei = response.json()
    data = eiei["data"]

   
    n = 0
    for i in data:
        wtf = data[n]
        del wtf['phSeverity']
        del wtf['phMainten']
        del wtf['salinitySeverity']
        del wtf['salinityMainten']
        del wtf['tdsSeverity']
        del wtf['tdsMainten']
        del wtf['doSeverity']
        del wtf['doMainten']
        del wtf['tempSeverity']
        del wtf['tempMainten']
        del wtf['conductivitySeverity']
        del wtf['conductivityMainten']
        del wtf['waterLevelSeverity']
        del wtf['waterLevelMainten']
        n = n+1
    
    
    mydict = data[nowja.hour]
    x = mycol.insert_one(mydict)

print("Complete!!",counter)
