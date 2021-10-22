import re
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
    # create shortcut story from github issue
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
    
    # create shortcut story comment for recording github issue number
    url = f"{url}/{shortcut_story_id}/comments"
    body = {
        "text": f"This story is related to github issue [#{issue_number}](https://github.com/makinarocks/canvas-mvp/issues/{issue_number})"
    }
    resp = requests.post(url, headers=headers, data=json.dumps(body))
    print(resp.json())

    # create github issue comment for recording shortcut story card
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

elif data["action"] == "unlabeled" and data["label"]["name"] == label_to_create_shortcut_story:
    comments_url = data["issue"]["comments_url"]
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}"
    }
    resp = requests.get(comments_url, headers=headers)
    comments = resp.json()

    reg_expr = re.compile("This Github issue is related Shortcut Story num: sc-[\d]*")

    story_id = ""
    for comment in comments[::-1]:
        for text in reg_expr.finditer(comment["body"]):
            story_id = text[52:]
        if story_id:
            break
    
    if story_id:
        url = f"https://api.app.shortcut.com/api/v3/stories/{story_id}"
        headers = {
            'Content-Type': 'application/json',
            'Shortcut-Token': shortcut_api_token
        }
        resp = requests.delete(url, headers=headers)
        print(resp.json())

else:
    print("this action do not create shortcut story card.")
