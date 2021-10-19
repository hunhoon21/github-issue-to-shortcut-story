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
github_token = os.environ["INPUT_GITHUB_TOKEN"]

print(f"label_to_create_shortcut_story: {label_to_create_shortcut_story}")

if data["action"] == "labeled" and data["label"]["name"] == label_to_create_shortcut_story:
    url = 'https://api.app.shortcut.com/api/v3/stories'
    headers = {
        'Content-Type': 'application/json',
        'Shortcut-Token': shortcut_api_token
    }
    body = {
        'name': data["issue"]["title"],
        'description': data["issue"]["body"],
        'workflow_state_id': 500000042,  # productization-unscheduled, should be input variable
        'group_id': '6077d73c-3f22-4a72-9e2b-b79011865fb5',  # Canvas, should be input variable
        'project_id': 3238  # Canvas, should be input variable
    }

    resp = requests.post(url, headers=headers, data=json.dumps(body))
    print(resp.json())

    shortcut_story_id = resp.json()["id"]

    issue_number = data["issue"]["number"]
    
    url = f"{url}/{shortcut_story_id}/comments"
    body = {
        "text": f"This story is related to github issue [#{issue_number}](https://github.com/makinarocks/canvas-mvp/issues/{issue_number})"
    }
    resp = requests.post(url, headers=headers, data=json.dumps(body))
    print(resp.json())

    url = f"{data['issue']['url']}/comments"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }
    body = {
        "body": f"This Github issue is related Shortcut Story num: sc-{shortcut_story_id}"
    }
    resp = requests.post(url, headers=headers, data=json.dumps(body))
    print(resp.json())

else:
    print("this action do not create shortcut story card.")
