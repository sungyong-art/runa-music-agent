import requests
from bs4 import BeautifulSoup
import sys

def get_kworb_titles(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        titles = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                # Typically title is in a link or text in the second or third column
                title_cell = cols[1]
                link = title_cell.find('a')
                if link:
                    titles.append(link.text.strip())
                else:
                    titles.append(title_cell.text.strip())
            if len(titles) >= 100:
                break
        return titles
    except Exception as e:
        print(f"Exception: {e}")
        return []

# Try March 11, 2026
url = "https://kworb.net/youtube/charts/us/20260311.html"
print(f"Fetching from {url}...")
titles = get_kworb_titles(url)

if not titles:
    # Try current
    url = "https://kworb.net/youtube/charts/us/index.html"
    print(f"Fetching from {url}...")
    titles = get_kworb_titles(url)

for i, title in enumerate(titles[:100], 1):
    print(f"{i}. {title}")
