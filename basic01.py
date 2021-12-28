#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 

import requests
url = 'https://notify-api.line.me/api/notify'
token = 'Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


#Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep ชิน
#3IHDRHBTUWBmhGRo6aLMEircbPQDUTfEflQQblrBHKL กลุ่ม
eiei = '5555'
msg = 'ทดสอบบอทสำหรับ Big Data'+' '+eiei + '\n\n' + 'บันทัดใหม่'

r = requests.post(url, headers=headers, data = {'message':msg})
print (r.text)
