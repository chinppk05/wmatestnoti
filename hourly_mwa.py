#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


from bs4 import BeautifulSoup
from typing import Counter
import requests
import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")
mydb = myclient["wma_test"]
mycol = mydb["wma87"]

nowja = datetime.now()

station_id = ["T3","S5","S4","T4","S7","S6","T2","S2","S17","S18","S20"]
station_name = ["วัดบ้านแป้ง","วัดโพธิ์แดงเหนือ","วัดมะขาม","สะพานพระนั่งเกล้า ","สะพานพระพุทธยอดฟ้า","คลองลัดโพธิ์","โรงไฟฟ้าพระนครใต้","ร้งสิตไซฟอน","พงษ์เพชร","โรงผลิตน้ำสามเสน","คลองน้ำอ้อม"]

counter = 0

while (counter < len(station_id)):
    url = "http://rwc.mwa.co.th/page/stats/table.php?id="+station_id[counter]+"&dt2="+str(nowja.year)+"-"+str(nowja.month)+"-"+str(nowja.day)+"&ntype=1HOUR"
    res = requests.get(url)
    res.encoding = "utf-8"
    
    soup = BeautifulSoup(res.text, 'html.parser')

    courses = soup.find_all('td')
    course_list = []

    for course in courses:
        obj = course.string
        course_list.append(obj)
    
    data = []
    hour = []
    i = 0

    while i < len(course_list):
        if i == 0 :
            #print("start !!!!")
            hour.append(course_list[i])
            i = i+1       
        elif i %13 == 0 :
            #print(i,"++++++++++++++++++++++++++++")
            data.append(hour)
            hour = []
            hour.append(course_list[i])
            i = i+1
        else:
            #print("data")
            hour.append(course_list[i])
            i = i+1

    col = ['order','datetime','time','ph','salt','turb','tds','chlorophyll','do','temp','depth','conduct','wlevel','bga']
    all_data = []
    
    i = 0
    while i < 24 :
        mwa_data = dict(zip(col,data[i]))
        all_data.append(mwa_data)
  
        all_data[i]['stationid'] = station_id[counter]
        all_data[i]['stationname'] = station_name[counter]
        i = i+1

    counter = counter+1
    x = mycol.insert_one(all_data[nowja.hour])
    """
    print(all_data[nowja.hour])
    print("--------------------------------------------------------------------------------------")
    print("\n\n")
    """

print("Complete!!")
