import requests
import json
from data import user
import auth
import config
import chatroom

url = f"{config.server_url}/message"
headers = config.headers
message_content = {"content": "안녕하세요. 상담 요청합니다."}


def create_message(user):
    token = auth.login(user)
    chatroom_id = chatroom.get_chatroom(user)

    r = requests.post(
        f"{url}/create/{chatroom_id['chatroom_id']}", data=json.dumps(message_content), headers={**headers, **token})
    print(r.text)


def create_messages():
    for user_data in user.user_data_set:
        create_message(user_data)


if __name__ == "__main__":
    create_messages()
