import github3
import requests

gh = github3.login('user-name', 'PAT token')
org = gh.organization("ORG NAME")
Company = '<Your company name here>'
repos = [
    """add list of repos here in an array for example
    'frontend',
    'we-win',"""
]
for repo in repos:
    headers = ({
    'Accept': 'application/vnd.github+json',
    'Authorization': 'Bearer {PAT TOKEN}',
    'X-GitHub-Api-Version': '2022-11-28',
    })

    response = (requests.get(f'https://api.github.com/repos/{Company}/{repo}/hooks', headers=headers))
    response = response.json()

    for resp in response:
        _tmp_url = resp['config']['url']
        _id = resp['id'] if '{name of webhook to strip for example snyk or checkmarx}' in _tmp_url else None
        if _id is not None:
            headers =({'Accept': 'application/vnd.github+json', 'Authorization': 'Bearer {PAT TOKEN}', 'X-GitHub-Api-Version': '2022-11-28',})
            response = (requests.delete(f'https://api.github.com/repos/{org}/{repo}/hooks/{_id}', headers=headers))
            print(response.status_code) #204
    print(f'{repo} complete')
