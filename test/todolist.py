import requests
import json
from data import todolist

url = "http://localhost:22222/todolist"

headers = {"Content-Type": "application/json"}


def create_todolist():
    for todo_data in todolist.todo_data_set:
        r = requests.post(url, data=json.dumps(
            todo_data), headers=headers, timeout=1)
        print(r.text)


if __name__ == "__main__":
    create_todolist()
