import requests
import json
from data import user
import config

url = f"{config.server_url}/auth/"


def login(user):
    r = requests.post(url, data=json.dumps(user), headers=config.headers)
    print(r.text)
    return json.loads(r.text)


if __name__ == "__main__":
    login(user.user_data_set[0])
