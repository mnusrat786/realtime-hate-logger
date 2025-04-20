import requests
import os

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

url = "https://raw.githubusercontent.com/hate-alert/HateXplain/master/Data/dataset.json"
target_path = "data/HateXplain.json"

response = requests.get(url)

if response.status_code == 200:
    with open(target_path, "wb") as f:
        f.write(response.content)
    print(" HateXplain.json downloaded and saved to /data/")
else:
    print(f" Failed to download. Status code: {response.status_code}")
