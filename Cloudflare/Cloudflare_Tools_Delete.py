"""
This script is used to check for useage of a rule and delete it if it is not in use for the tools section
"""
import requests
import time
import csv
from datetime import timedelta, datetime
import os




CLOUDFLARE_API_TOKEN = input('Cloudflare API token\n')
Zone_ID =  input('What is the Zone ID?\n')
ENDPOINT = 'https://api.cloudflare.com/client/v4/'
user_name = input('computers username \n This can be found on terminal using the command pwd\n')
Zone_name = input('What zone is this for?\n')
graphql_url = 'https://api.cloudflare.com/client/v4/graphql'
start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()[:-7]+'Z'
end_date = datetime.utcnow().isoformat()[:-7]+'Z'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}'
}

Params = {
    'per_page': 1000,
    'page': 1
}

RULE_EXCLUSION_LIST_1 = [
    
]

RULE_EXCLUSION_LIST_2 = [
    
]

DELETED_RULES = {}

rule_list = {}

#function to delete rule id and add to dleted rules dict
def cloudflare_delete(rule_id):
    CLOUDFLARE_API_TOKEN = ''
    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': '<your auth email>',
        'X-Auth-Key': f'{CLOUDFLARE_API_TOKEN}'
    }
    delete_request = requests.delete(f'{ENDPOINT}/zones/{Zone_ID}/firewall/access_rules/rules/{rule_id}',
                                     headers=headers).json()
    if delete_request['success'] == False:
        print("Deletion Failure :", rule_id, " : ", delete_request)
    else:
        print(rule_id, ':', delete_request)
        DELETED_RULES.update({rule_id: ip})

def cloudflare_traffic(ip):
    #see if there is any activity on 1 ip for the last 30 days
    graphql_query = """
    {
      viewer {
        zones(filter: {zoneTag: "%s"}) {
          httpRequestsAdaptiveGroups(

            limit: 2,
            filter: {datetime_geq: "%s", datetime_leq: "%s", clientIP: "%s"}
          ) {
            dimensions {
              datetime
            }

          }
        }
      }
    }""" % (Zone_ID, start_date, end_date, ip)
    traffic = requests.post(graphql_url, headers=headers, json={'query': graphql_query}).json()
    try:
        # print(traffic)
        if traffic['data']['viewer']['zones'][0]['httpRequestsAdaptiveGroups'][0]['dimensions'] != "":
            print(ip + " this is still affective")
            pass
    except:
        #build in for loop for this call. break out of loop after max retry
        if traffic['errors']:
            print(traffic, ip)
            cloudflare_traffic(ip)

        else:
            return 'no logs'



response = requests.get(f'{ENDPOINT}/zones/{Zone_ID}/firewall/access_rules/rules', headers=headers, params=Params).json()
check = response['result']
# print(response)
# print(check)

for rule in check:
    if rule['paused'] is True:
        print(rule + " to be deleted")
        cloudflare_delete(rule['id'])

for rule in check:
    if rule['paused'] is False:
        if Zone_ID == '{ZONEID}':
            if rule['id'] not in RULE_EXCLUSION_LIST_1:
                IP = rule['configuration']['value']
                ID = rule['id']
                rule_list.update({IP: ID})
            else:
                continue
        if Zone_ID == '{ZONEID2}':
            if rule['id'] not in KJB_RULE_EXCLUSION_2T:
                IP = rule['configuration']['value']
                ID = rule['id']
                rule_list.update({IP: ID})
            else:
                continue

for ip in rule_list:
    time.sleep(3)
    if cloudflare_traffic(ip) == 'no logs':
        print(rule_list[ip]+" to be deleted")
        cloudflare_delete(rule_list[ip])

print(DELETED_RULES)


#CSV for deleted rules
string = 'Deleted Rules'
save_path = f'/Users/{user_name}/Desktop/firewall'
csv_file_name = f'{Zone_name}_{string}_{end_date}.csv'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
file_path = os.path.join(save_path, csv_file_name)

# cast to CSV and save on desktop
with open(file_path, 'w', newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    for rule_id, rule_ip in DELETED_RULES.items():
        csv_writer.writerow([rule_id, rule_ip])

    print(f'JSON data has been converted to CSV and saved as {csv_file_name}\n\n\n')


