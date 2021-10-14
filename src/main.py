import os
import json

print(os.environ)
print("-" * 30)
with open(os.environ["GITHUB_EVENT_PATH"]) as f:
    data = json.load(f)
print(f"github_event: {data}")