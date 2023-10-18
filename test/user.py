import requests
import json
from data import user
import config

admin_url = f"{config.server_url}/admin/user"
url = f"{config.server_url}/user"

headers = {"Content-Type": "application/json"}


def create_admin():
    r = requests.post(admin_url, data=json.dumps(
        user.admin_data), headers=headers)
    print(r.text)


def create_users():
    for user_data in user.user_data_set:
        r = requests.post(url, data=json.dumps(user_data), headers=headers)
        print(r.text)
