import requests
import json
from data import user
import auth
import config

url = f"{config.server_url}/chatroom"
headers = config.headers


def create_chatroom(user):
    token = auth.login(user)
    r = requests.post(url, headers={**headers, **token})
    print(r.text)


def create_chatrooms():
    for user_data in user.user_data_set:
        create_chatroom(user_data)


def get_chatroom(user):
    token = auth.login(user)
    r = requests.get(url, headers={**headers, **token})
    return json.loads(r.text)


if __name__ == "__main__":
    create_chatrooms()
