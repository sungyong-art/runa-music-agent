import requests
import re

url = "https://charts.youtube.com/charts/TopVideos/us/daily"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

# Find all "title" or "name" fields in JSON-like strings
titles = re.findall(r'"title":"(.*?)"', response.text)
if not titles:
    titles = re.findall(r'"name":"(.*?)"', response.text)

print(f"Found {len(titles)} titles.")
for i, t in enumerate(titles[:100], 1):
    print(f"{i}. {t}")
