#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta

# Define API information for 100 sources (replace with your actual API information)
site_all_data = {
    'site1': {'name': 'บางพลี', 'water_values': [], 'power_values': []},
    'site2': {'name': 'สามพราน', 'water_values': [], 'power_values': []},
    'site3': {'name': 'ระยอง', 'water_values': [], 'power_values': []},
    'site4': {'name': 'บางปลา2', 'water_values': [], 'power_values': []},
    'site5': {'name': 'ปู่เจ้าสมิงพราย', 'water_values': [], 'power_values': []},
    'site6': {'name': 'อ้อมใหญ่', 'water_values': [], 'power_values': []},
    'site7': {'name': 'แพรกษา', 'water_values': [], 'power_values': []},
    'site8': {'name': 'กำแพงแสน', 'water_values': [], 'power_values': []},
    'site9': {'name': 'ลำโพ', 'water_values': [], 'power_values': []},
    'site10': {'name': 'เชียงใหม่', 'water_values': [], 'power_values': []},
    'site11': {'name': 'พะเยา', 'water_values': [], 'power_values': []},
    'site12': {'name': 'ปลายบาง', 'water_values': [], 'power_values': []},
    'site13': {'name': 'เขาน้อย', 'water_values': [], 'power_values': []},
    'site14': {'name': 'สงขลา', 'water_values': [], 'power_values': []},
    'site15': {'name': 'พิษณุโลก', 'water_values': [], 'power_values': []},
    'site16': {'name': 'ราชบุรี', 'water_values': [], 'power_values': []},
    'site17': {'name': 'บ้านฉาง', 'water_values': [], 'power_values': []},
    'site18': {'name': 'ปากพนัง', 'water_values': [], 'power_values': []},
    'site19': {'name': 'ปากน้ำปราณ', 'water_values': [], 'power_values': []},
    'site20': {'name': 'บางบัวทอง', 'water_values': [], 'power_values': []},
    'site21': {'name': 'ชะอำ', 'water_values': [], 'power_values': []},
    # Add information for other APIs
    # ...
}

def calculate_date_range():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    end_date = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
    start_date = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    
    return start_date, end_date

def get_power_api_data(site_number, start_date, end_date):
    api_url = f'http://allmcl.com/api/getPowerMeterLogBySiteAndPeriod/{site_number}/{start_date.strftime("%Y-%m-%d")}/{end_date.strftime("%Y-%m-%d")}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve power data for site {site_number}. Status code: {response.status_code}")
        return None

def get_water_api_data(site_number, start_date, end_date):
    api_url = f'http://allmcl.com/api/getFlowMeterLogBySiteAndPeriod/{site_number}/{start_date.strftime("%Y-%m-%d")}/{end_date.strftime("%Y-%m-%d")}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve water data for site {site_number}. Status code: {response.status_code}")
        return None

def send_line_notification(access_token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"message": message}
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code != 200:
        print(f"Failed to send Line notification. Status code: {response.status_code}")

def main():
    start_date, end_date = calculate_date_range()

    for site_number in range(1, 22):
        power_api_data = get_power_api_data(site_number, start_date, end_date)
        water_api_data = get_water_api_data(site_number, start_date, end_date)

        if power_api_data and water_api_data:
            water_values = []
            for entry in water_api_data:
                flow_meter_logs = entry.get('flowMeterLogs', [])
                water_values.extend([log['waterDiff'] for log in flow_meter_logs])

            power_values = [entry['powerKwhDiff'] / 10 for entry in power_api_data[0]['powerMeterLog']]

            site_key = f'site{site_number}'
            site_all_data[site_key]['water_values'] = water_values
            site_all_data[site_key]['power_values'] = power_values
        else:
            print(f"No data retrieved for site {site_number}.")

        # Convert water_values to a sequence
        water_sequence = [int(value) for value in water_values]
        print(f"Water Sequence: {water_sequence}")



    # Build a summary message for Line notification
    summary_message = "น้ำเมื่อวาน:\n"
    for site_number, site_info in site_all_data.items():
        site_name = site_info['name']
        water_values = site_info['water_values']

        if water_values:
            summary_message += f"{site_name} : {', '.join(map(str, water_values))} ลบ.ม.\n"
        else:
            summary_message += f"{site_name} : ...\n"


    # Send Line notification with the summary
    access_token = "hOI8xi2ZfwY93FV4UAhvB4NonrwyB3CTGUHRyHXp7tA"  # Replace with your Line Notify access token
    send_line_notification(access_token, summary_message)

if __name__ == "__main__":
    main()
