CLOUDFLARE_API_TOKEN =  #global api key
Zone_ID =  input('What is the Zone ID?\n')
ENDPOINT = 'https://api.cloudflare.com/client/v4/'


headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': '<your auth email>',
    'X-Auth-Key': f'{CLOUDFLARE_API_TOKEN}'
}
rule_id = [
  
           ]

for rule in rule_id:
    delete_request = requests.delete(f'{ENDPOINT}/zones/{Zone_ID}/firewall/access_rules/rules/{rule_id}', headers=headers)
    print(rule, ':', delete_request.json())
