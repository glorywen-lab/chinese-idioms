import urllib.request
import json
import os

url = 'https://raw.githubusercontent.com/pwxcoo/chinese-xinhua/master/data/idiom.json'
target_path = 'debug_logs/xinhua_idioms.json'

if not os.path.exists(target_path):
    print("Downloading idiom dataset...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read()
        with open(target_path, 'wb') as f:
            f.write(content)
    print(f"Downloaded and saved to {target_path}, size: {len(content)} bytes")
else:
    print(f"{target_path} already exists.")
