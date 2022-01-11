#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

import requests
import re
import json
import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")
mydb = myclient["wma_test"]
mycol = mydb["wma85"]

nowja = datetime.now()

today = str(nowja.day)+"/"+str(nowja.month)+"/"+str(nowja.year+543)

num = 0

time = ["00.00","00.30","01.00","01.30","02.00","02.30","03.00","03.30","04.00","04.30","05.00",
"05.30","06.00","06.30","07.00","07.30","08.00","08.30","09.00","09.30","10.00","10.30","11.00",
"11.30","12.00","12.30","13.00","13.30","14.00","14.30","15.00","15.30","16.00","16.30","17.00",
"17.30","18.00","18.30","19.00","19.30","20.00","20.30","21.00","21.30","22.00","22.30","23.00","23.30"]

head = ["ph","do","ec","temp","bod","cod","time","date","stationid","stationname"]

station_id = [109,110,111,112,113,118,128,129,222,240,248,306]


station_name = ["ชัยนาท",'สิงห์บุรี','ป่าโมก','บางไทร','ปากเกร็ด',"ดาวคะนอง","สำแล","นครสวรรค์","อยุธยา","สมุทรปราการ","อ่างทอง","สามโคก"]


while num < len(station_id):

    url = "http://iwis.pcd.go.th/module/auto_station/auto_station_miniChart.php?locationid="+str(station_id[num])+"&startdate="+str(nowja.year)+"-"+str(nowja.month)+"-"+str(nowja.day)+"+00%3A00&enddate="+str(nowja.year)+"-"+str(nowja.month)+"-"+str(nowja.day)+"+23%3A45&etc=1629930335663"
    
    res = requests.get(url)
    res.encoding = "utf-8"

    y = re.findall(r"series.+",res.text)

    #print(y)
    z = json.dumps(y[0], indent=4)
    json_object = json.loads(z)


    #สร้าง list ข้อมูลหยาบๆ
    n = 0
    chin = [""]
    for i in json_object :
        if i==":" or i == "," :
            n=n+1
            chin.append("")
        elif i == "{" or i == "}" or i == "[" or i == "]" or i == "\'" :
            n=n
        else:
            chin[n] = chin[n]+i



    #สร้าง list ข้อมูลละเอียด แบ่งแยกชัดเจน
    n = 0
    j = 0
    k = 0
    data = []
    for i in chin:
        if i == "name":
            j = n+1
            data.append([])
            while j < len(chin):
                if chin[j] == "name" :
                    break 
            
                data[k].append(chin[j])
                j = j+1
            k = k+1
            j = 0
            
        n=n+1
  
   

    """
    print("---------------------------------------------------------------------------")
    print("ลำดับที่ :", num+1, "/ สถานี :", station_name[num] , " ขนาด", len(data))
    for i in data:
        print(i)
        print("+++++++")
    """

    #แยกค่า parameter แต่ละเวลามารวมกันไว้เป็น list เช่น 10.00 มีค่า a b c d ...
    a = 2
    b = 0
    box = []
    big_box = []
    while a <= ((nowja.hour*2)+2):
        while b < len(data):
            box.append(data[b][a])
            b = b+1
        b = 0
        big_box.append(box)
        box = []
        a = a+1


   
    #สร้าง list ของชื่อประเภทของค่าพารามิเตอร์แต่ละชนิดของแต่ละสถานี
    c = 0
    para = []
    while c < len(data):
        para.append(data[c][0])
        c = c+1

    
    

    #เปลี่ยนค่าพารามิเตอร์จาก string เป็น float
    e = 0
    while e < len(big_box):
        f = 0
        while f < len(big_box[e]):
            big_box[e][f] = float(big_box[e][f])
            f = f+1
        e = e+1
  
    
    #จับคู่ พารามิกเตอร์กับชื่อพารามิเตอร์สร้างเป็น dictionnary
    lake = []
    for i in big_box:
        lake.append(dict(zip(para,i)))


    d = 0
    for i in lake:
        i["time"] = time[d]
        i["date"] = today
        i["name"] = station_name[num]
        i["stationid"] = str(station_id[num])
        d = d+1
    """
    for i in lake:
        mydict = i
        x = mycol.insert_one(mydict)
        print(x)
    """
    mydict = lake[nowja.hour*2]
    x = mycol.insert_one(mydict)
    print(x)
    

    num = num+1

print("complete!!")
