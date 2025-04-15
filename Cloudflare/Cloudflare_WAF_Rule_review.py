"""
This script is used to pull Cloudflare WAF rules and change the JSON to CSV
"""

import requests
import sys
import json
import csv
import datetime
import os.path



CLOUDFLARE_API_TOKEN = '<API TOKEN>'
Zone_ID =  input('What is the Zone ID?\n')
ENDPOINT = 'https://api.cloudflare.com/client/v4/'
person = input('give me your name\n')
user_name = input('computers username \n This can be found on terminal using the command pwd\n')
Zone_name =  input('What zone is this for?\n')
save_path = f'/Users/{user_name}/Desktop/firewall'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}'
}

response_1 = requests.get(f'{ENDPOINT}/zones/{Zone_ID}/firewall/rules', headers=headers).json()
response_2 = requests.get(f'{ENDPOINT}/zones/{Zone_ID}/firewall/waf/packages/package_id/rules', headers=headers).json()
response_3 = requests.get(f'{ENDPOINT}/zones/{Zone_ID}/rate_limits', headers=headers).json()
response_4 = requests.get(f'{ENDPOINT}/zones/{Zone_ID}/firewall/access_rules/rules', headers=headers).json()
data_1 = json.dumps(response_1['result'])
data_2 = json.dumps(response_2['result'])
data_3 = json.dumps(response_3['result'])
data_4 = json.dumps(response_4['result'])


def current_timestamp():
    # in the format of "2021-01-01 11:11:11.11"
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


# cast to dict
rules = json.loads(data_1)
waf = json.loads(data_2)
rate_limit = json.loads(data_3)
tools = json.loads(data_4)

rule_list = (rules, waf, rate_limit, tools)


for rule in rule_list:
    try:
        string = [ i for i, a in locals().items() if a == rule][0]
        csv_file_name = f'{Zone_name}{string}_{person}_{current_timestamp()}.csv'
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        file_path = os.path.join(save_path, csv_file_name)

        # cast to CSV and save on desktop
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            count = 0
            for record in rule:
                if count == 0:
                    # Writing headers of CSV file
                    header = record.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(record.values())

        print(f'JSON data has been converted to CSV and saved as {csv_file_name}\n\n\n')

    except TypeError as err:
        print(f'issue with {rule}')

