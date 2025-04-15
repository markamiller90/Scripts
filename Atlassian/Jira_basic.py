import requests
from ssm_parameter_store import SSMParameterStore


store = SSMParameterStore(prefix='/Audit') # turn this into your SSM PARAM prefix
jira_token = store['JIRA_API_TOKEN']
jira_email = '<your jira user>'

class jira:

    # add ticket to jira
    def jira_ticket(my_company, board, audit_type, ticket_body):
        api_url = f'https://{my_company}.atlassian.net/rest/api/3/issue/'

        issue = {
            'fields': {
                'project': {
                    'key': f'{board}'  # This is the board this will send tickets too
                },
                'summary': f'{audit_type}',
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": f"{ticket_body}",
                                "type": "text"
                            }
                        ]
                        }
                    ]
                },
                'issuetype': {
                    'name': 'Task'
                }
            }
            }

        # Set auth headers
        headers = {'Accept': 'application/json', "Content-Type": "application/json"}

        Jira_request = requests.post(api_url, headers=headers, json=issue, auth=(jira_email, jira_token))

    # Update jira ticket
    def jira_update(my_company, issue_key, new_description):
        api_url = f'https://{my_company}.atlassian.net/rest/api/3/issue/{issue_key}'


        issue = {
            'fields': {
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": f"{new_description}",
                                "type": "text"
                            }
                        ]
                        }
                    ]
                },
                'issuetype': {
                    'name': 'Task'
                }
            }
        }

        # Set auth headers
        headers = {'Accept': 'application/json', "Content-Type": "application/json"}

        Jira_request = requests.put(api_url, headers=headers, json=issue, auth=(jira_email, jira_token))
    
    #Add an attachemtnt to jira
    def jira_attachment(my_company, issue_key, file_name, path_to_file):
        api_url = f'https://{my_company}.atlassian.net/rest/api/3/issue/{issue_key}/attachments'

        files = {
        'file': (f'{file_name}', open(f'{path_to_file}', 'rb'), 'text/plain')
        }

        # Set auth headers
        headers = {'X-Atlassian-Token': 'no-check'}

        Jira_request = requests.post(api_url, headers=headers, files=files, auth=(jira_email, jira_token))
        print(Jira_request.text)
        print(Jira_request.status_code)