#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

import requests
from datetime import datetime

now = datetime.now() # current date and time
time = now.strftime("%H:%M:%S")


url = 'https://notify-api.line.me/api/notify'
token = 'Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


#Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep ชิน
#3IHDRHBTUWBmhGRo6aLMEircbPQDUTfEflQQblrBHKL กลุ่ม
eiei = '5555'
msg = '\nทดสอบการแจ้งเตือน Big Data \nทุกๆ 5 นาที \n'+'ขณะนี้เวลา '+ time +'\n\n' + 'Complete!!'

r = requests.post(url, headers=headers, data = {'message':msg})
print (r.text)
