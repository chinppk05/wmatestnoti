#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 



import requests
import json
from datetime import date

today = date.today()
y = today.year
m = today.month
d = today.day


url = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/1/2022-01-02/2022-01-02"

bangpli_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/1/2022-01-02/2022-01-02"
sampran_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/2/2022-01-02/2022-01-02"
rayong_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/3/2022-01-02/2022-01-02"
bangpla2_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/4/2022-01-02/2022-01-02"
puchao_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/5/2022-01-02/2022-01-02"
omyai_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/6/2022-01-02/2022-01-02"
praegsa_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/7/2022-01-02/2022-01-02"
kps_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/8/2022-01-02/2022-01-02"
lumpo_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/9/2022-01-02/2022-01-02"
cnx_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/10/2022-01-02/2022-01-02"




testapi = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/"+"7"+"/2022-01-02/2022-01-02"

payload={}
headers = {}

#response = requests.request("GET", url, headers=headers, data=payload)

#print(response.text)

#data = response.json()

#print(data)

#print(data[0]['waterDiff'])

list_scada = ["1","2","3","4","5","6","7","8","9","10"]

#print(len(list_scada))

all_data = []
i = 0
while i < len(list_scada):
    #print(i)
    url_api = "http://www.allmcl.com/api/getFlowMeterLogBySiteAndPeriod/"+list_scada[i]+"/"+str(y)+"-"+str(m)+"-"+str(d)+"/"+str(y)+"-"+str(m)+"-"+str(d)
    #print(url_api)

    response = requests.request("GET", url_api , headers=headers, data=payload)
    data = response.json()

    all_data.append(data)

    #print(url_api)
    i = i+1

#print(all_data)



water_daily = [
    {
    "station_id" : 1,
    "station" : "เทศบาลตำบลบางพลี จังหวัดสมุทรปราการ",
    "waterdaily" : ""
    },
    {
    "station_id" : 2,
    "station" : "เทศบาลเมืองสามพราน จังหวัดนครปฐม",
    "waterdaily" : ""
    },
    {
    "station_id" : 3,
    "station" : "เทศบาลนครระยอง จังหวัดระยอง",
    "waterdaily" : ""
    },
    {
    "station_id" : 4,
    "station" : "เทศบาลตำบลบางปลา แห่งที่ 2  จังหวัดสมุทรปราการ",
    "waterdaily" : ""
    },
    {
    "station_id" : 5,
    "station" : "เทศบาลเมืองปู่เจ้าสมิงพราย จังหวัดสมุทรปราการ",
    "waterdaily" : ""
    },
    {
    "station_id" : 6,
    "station" : "เทศบาลตำบลอ้อมใหญ่ จังหวัดนครปฐม",
    "waterdaily" : ""
    },
    {
    "station_id" : 7,
    "station" : "เทศบาลเมืองแพรกษา จังหวัดสมุทรปราการ",
    "waterdaily" : ""
    },
    {
    "station_id" : 8,
    "station" : "องค์การบริหารส่วนตำบลกำแพงแสน จังหวัดนครปฐม",
    "waterdaily" : ""
    },
    {
    "station_id" : 9,
    "station" : "องค์การบริหารส่วนตำบลลำโพ จังหวัดนนทบุรี",
    "waterdaily" : ""
    },
    {
    "station_id" : 10,
    "station" : "เทศบาลนครเชียงใหม่",
    "waterdaily" : ""
    },
]

"""
for i in water_daily:
    print(i)
    print ("--------------------------------------------------")
"""


n = 0
for i in all_data:
  
    if len(i) == 0:
        water_daily[n]["waterdaily"] = "ไม่มีข้อมูล"
    else:
       water_daily[n]["waterdaily"] = i[0]["waterDiff"]
    n = n+1

print(water_daily)

url = 'https://notify-api.line.me/api/notify'
token = 'drjIP0BKslpQO0YyzVs7dMrlT8DDRPkdtrbYdHK23cj'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

#G1gMDFgZrhGCa4rXePJP36PhEM3UejaSPUBvk1GDijv กลุ่ม scada
#Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep ชิน
#3IHDRHBTUWBmhGRo6aLMEircbPQDUTfEflQQblrBHKL กลุ่ม

msg = ""
n = 0
for i in water_daily:
    print(i)
    msg = msg+ "\n\n"+water_daily[n]["station"]+" : "+"\n"+str(water_daily[n]["waterdaily"])+" ลบ.ม" 
    n = n+1

r = requests.post(url, headers=headers, data = {'message':msg})
print (r.text)