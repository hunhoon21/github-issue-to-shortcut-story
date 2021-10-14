import os
import json
import requests


print(os.environ)
print("-" * 30)
with open(os.environ["GITHUB_EVENT_PATH"]) as f:
    data = json.load(f)
print(f"github_event: {data}")
print("-" * 30)

label_to_create_shortcut_story = os.environ["INPUT_LABEL_TO_CREATE_SHORTCUT_STORY"]
shortcut_api_token = os.environ["INPUT_SHORTCUT_API_TOKEN"]

print(f"label_to_create_shortcut_story: {label_to_create_shortcut_story}")

if data["action"] == "labeled" and data["label"]["name"] == label_to_create_shortcut_story:
    url = 'https://api.app.shortcut.com/api/v3/stories'
    headers = {
        'Content-Type': 'application/json',
        'Shortcut-Token': '61614d17-06ec-4f5f-87c7-3c5f950731c4'
    }
    body = {
        'name': data["issue"]["title"],
        'description': data["issue"]["body"],
        'workflow_state_id': 500000042,  # productization-unscheduled
        'group_id': '6077d73c-3f22-4a72-9e2b-b79011865fb5',  # Canvas
        'project_id': 3238  # Canvas
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))
    print(resp.json())
else:
    print("this action do not create shortcut story card.")
