#mass removal of checks on repos
import github3
import requests

gh = github3.login('{USERNAME}', '{PAT TOKEN}')
org = gh.organization("{org}")
repos = [
 """add repos in an array""",
]
for repo in repos:
    branches=['main','master','develop','dev/stable']
    
    for branch in branches:
        if branch:
            headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': 'Bearer {PAT TOKEN}',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = '{"contexts":["{add check to strip"]}'#checks to strip
            response = requests.delete(
                f'https://api.github.com/repos/{org}/{repo}/branches/{branch}/protection/required_status_checks/contexts',
                headers=headers,
                data=data,
            )
            print(response.content)
            print(f'{repo}\'s checks stripped')
        else:
            print(f'{branch} doesnt exits')
