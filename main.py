import requests
import os
import json


org_id = os.environ.get('ORG_ID')
api_token = os.environ.get('TOKEN')
base_url = os.environ.get('BASE_URL')
api_atlassian_url = os.environ.get('AT_AD_URL', 'https://api.atlassian.com')
admin_atlassian_url = os.environ.get('AT_AD_URL', 'https://admin.atlassian.com/')


# Get token list
def get_api_tokens(org_id, api_token, api_url):
    response = requests.get(f'{api_url}/admin/api-access/v1/orgs/{org_id}/api-tokens',
                            headers={'Authorization': f'Bearer {api_token}'}, params={'pageSize': 1000})
    if response.status_code == 200:
        print('Found tokens')
        return response.json()
    print('No found Tokens')
    return None


# sort the list by users
api_tokens = get_api_tokens(org_id, api_token, api_atlassian_url)
token_users = []
if api_tokens:
    tokens = api_tokens['data']
    for token in tokens:
        user = {
            "name": token['user']['name'],
            "email": token['user']['email'],
            "token_name": token['label'],
            "created": token['createdAt']
        }
        token_users.append(user)

# Creating a list of findings for the AppSec Portal
output_data = []
for user in token_users:
    output_data.append({
        "name": f"Atlassian Token named {user['token_name']} found for user {user['name']}",
        "description": f"Name: {user['name']}\nEmail: {user['email']}\nToken name: {user['token_name']}\nDate: {user['created']}",
        "file_path": "",
        "severity": "Medium",
        "vulnerable_url": f"{admin_atlassian_url}/o/{org_id}/api-tokens"
        })

# Make JSON
with open('audit_log_results.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)
