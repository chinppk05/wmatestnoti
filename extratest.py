#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 


import datetime
from datetime import datetime
from datetime import date
import requests
import json
import pymongo

staion = 1
staion_num = 1
initrun = datetime.now()
while staion_num < 52:
    url = "https://wma-project-277408.et.r.appspot.com/grafana-api/"+str(staion)+"/query"
    # payload ตั้งต้นก่อนดัดแปลง
    pl = {
        "app": "dashboard",
        "requestId": "Q120",
        "timezone": "browser",
        "panelId": 23763571993,
        "dashboardId": None,
        "range": {
        "from": "2021-08-24T09:19:53.372Z",
        "to": "2021-08-25T15:19:53.372Z",
        "raw": {
                "from": "now-6h",
                "to": "now"
        }
    },
    "timeInfo": "",
    "interval": "30s",
    "intervalMs": 30000,
    "targets": [
        {
                "refId": "A",
                "data": "",
                "target": "water_data_series",
                "type": "table",
                "datasource": "JSON-1X"
        },
        {
            "refId": "B",
            "data": "",
            "target": "another_series",
            "type": "timeseries",
            "datasource": "JSON-1X"
        }
    ],
    "maxDataPoints": 618,
    "scopedVars": {
        "__interval": {
            "text": "30s",
            "value": "30s"
        },
        "__interval_ms": {
            "text": "30000",
            "value": 30000
        }
    },
    "startTime": 1604157593373,
    "rangeRaw": {
        "from": "now-6h",
        "to": "now"
    },
    "adhocFilters": []
    }

    # เทส payload ตั้งต้น
    # print(type(pl))

    # payloadที่แท้จริง
    payload = json.dumps(pl)

    new_payload = json.loads(payload)

    """
    print(new_payload)
    print(type(new_payload))

    for i, v in enumerate(new_payload):
    print(i, v)

    """
    when = new_payload['range']
    # print(when)

    when_i = when['from']
    # print(when_i)
    when_f = when['to']
    # print(when_f)

    #    print(type(when_i))

    today = date.today()
    """
        print("Current year:", today.year)
        print("Current month:", today.month)
        print("Current day:", today.day)
        """
    y = today.year
    m = today.month
    dd = today.day

    range = str(y)+'-'+str(m)+'-'+str(dd-1)+'T07:19:53.372Z'
    range2 = str(y)+'-'+str(m)+'-'+str(dd)+'T07:19:53.372Z'
    # print(range,"\n",range2)

    pl['range']['from'] = range
    pl['range']['to'] = range2

    # payloadที่แท้จริง
    payload = json.dumps(pl)
    headers = {
    'Authorization': 'Basic YXBpLXVzZXI6UXlqZnE2SDl6aVJXYmYyUFBSNVFwZFdH',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    """
        #เขียนไฟล์
        with open('data2.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
    """
    #print(json.dumps(response.json(), indent=2))

    #print(json.dumps(response.json(), indent=2))

    wma = response.json()

    # เปิดไฟล์ต้นฉบับดู
    # print(wma)
    # print(type(wma))
    # print(len(wma))

    # เจาะเข้า dict
    wma_2 = wma[0]

    """
        #เทสข้อมูล
        print(wma_2)
        print("")
        print(len(wma_2))


        #ดูพารามิเตอร์ใน dict
        for i, v in enumerate(wma_2):
        print(i, v)

        #ลองเทส
        #print(wma_2["columns"])
        #print(type(wma_2["rows"]))


        #เช็ค columns
        for i in wma_2["columns"]:
        print(i)
    """

    # เจาะเข้า dict : columns => ได้เป็น list
    wma_c = wma_2["columns"]

    # ลองเทส colomns
    # print(type(wma_2col))
    # print(wma_2col[0])

    # ดึงข้อมูลจาก column มาสร้าง list ใส่ para
    para = []
    n = 0
    for i in wma_c:
        k = wma_c[n]
        # print(k['text'])
        para.insert(n, k['text'])
        n = n + 1
        # print(para)

        # เจาะเข้า dict : rows
    wma_row = wma_2["rows"]
    # print(len(wma_row))
    if len(wma_row) != 0:

        # print(wma_row)
        # print(len(wma_row))

        # เจาะเข้า list ใน rows อีกที
        wma_r = wma_row[0]
        # print(wma_r)
        # print(len(wma_r))

        """
            n = 0
            for i in wma_r:
            print("ที่ ", n , "ค่า ", i, "ประเภท", type(i))
            """
        # ข้อมูลสุดท้าย The last ก่อนนำไปใช้
        wma_data = dict(zip(para, wma_r))
        # print(wma_data)

        # print("\n\n\n")
        # print(wma_data['timestamp'])

        ts01 = wma_data['timestamp']*0.001

        # print(ts01)

        ts02 = int(ts01)
        # print(ts02)

        timestamp = ts02
        dt_object = datetime.fromtimestamp(timestamp)

        #print("dt_object =", dt_object)
        #print("type(dt_object) =", type(dt_object))
        # print(dt_object.year)
        # print(dt_object.month)
        # print(dt_object.day)

        wma_data["year"] = dt_object.year
        wma_data["month"] = dt_object.month
        wma_data["day"] = dt_object.day

        #print(wma_data)
        
        # เพิ่มข้อมูล
        myclient = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")
        #myclient = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")
        mydb = myclient["wma_test"]
        mycol = mydb["wmatestja"]
        mydict = wma_data

        x = mycol.insert_one(mydict)
        # print(x)
        print("station : ",staion_num," is success!!")
    staion_num = staion_num+1
    staion = staion+1

endrun = datetime.now()

print ('start at '+initrun+' ; end at '+endrun)