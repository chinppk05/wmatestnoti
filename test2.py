#!/usr/local/bin/python3
import requests
import time

seconds = time.time()
local_time = time.ctime(seconds)
print("Seconds since epoch =", local_time)	

msg2 = 'Test at : '+local_time

print(msg2)

url = 'https://notify-api.line.me/api/notify'
token = 'Ryn034SAsglah4mmDvBKwz7Zwjx46BfWngmjJpnpmep'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

msg = 'Hello LINE Notify'

r = requests.post(url, headers=headers, data = {'message':msg2})
print (r.text)
