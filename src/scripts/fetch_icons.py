# scripts/fetch_icons.py
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import time
import json

# Create directories if they don't exist
os.makedirs('src/icons/png', exist_ok=True)
os.makedirs('src/icons/svg', exist_ok=True)

# List of icon sources
ICON_SOURCES = [
    # SVG Sources
    {
        'name': 'simple-icons',
        'url': 'https://api.github.com/repos/simple-icons/simple-icons/contents/icons',
        'base_url': 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/',
        'format': 'svg',
        'type': 'api'
    },
    {
        'name': 'material-design-icons',
        'url': 'https://github.com/google/material-design-icons/tree/master/symbols/web',
        'base_url': 'https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/',
        'format': 'svg',
        'type': 'github'
    },
    {
        'name': 'feather-icons',
        'url': 'https://github.com/feathericons/feather/tree/master/icons',
        'base_url': 'https://raw.githubusercontent.com/feathericons/feather/master/icons/',
        'format': 'svg',
        'type': 'github'
    },
    
    # PNG Sources
    {
        'name': 'icons8-png',
        'url': 'https://icons8.com/icons/set/technology--static',
        'format': 'png',
        'type': 'scrape',
        'selector': 'img.icon'
    },
    {
        'name': 'flaticon-png',
        'url': 'https://www.flaticon.com/free-icons/technology',
        'format': 'png',
        'type': 'scrape',
        'selector': 'img[src*=".png"]'
    }
]

def download_from_github_api(source):
    try:
        response = requests.get(source['url'])
        if response.status_code == 200:
            icons = response.json()
            downloaded = 0
            for icon in icons:
                if icon['name'].endswith(f".{source['format']}"):
                    download_url = icon['download_url']
                    icon_name = icon['name']
                    save_path = f"src/icons/{source['format']}/{icon_name}"
                    
                    if not os.path.exists(save_path):
                        urllib.request.urlretrieve(download_url, save_path)
                        downloaded += 1
                        print(f"Downloaded {icon_name} from {source['name']}")
                        time.sleep(0.1)  # Be gentle with the API
            return downloaded
    except Exception as e:
        print(f"Error downloading from {source['name']} API: {str(e)}")
    return 0

def download_from_github_ui(source):
    try:
        response = requests.get(source['url'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            downloaded = 0
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.endswith(f".{source['format']}"):
                    icon_name = os.path.basename(href)
                    download_url = f"{source['base_url']}{icon_name}"
                    save_path = f"src/icons/{source['format']}/{icon_name}"
                    
                    if not os.path.exists(save_path):
                        urllib.request.urlretrieve(download_url, save_path)
                        downloaded += 1
                        print(f"Downloaded {icon_name} from {source['name']}")
                        time.sleep(0.1)
            return downloaded
    except Exception as e:
        print(f"Error downloading from {source['name']} UI: {str(e)}")
    return 0

def download_from_scrape(source):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(source['url'], headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            downloaded = 0
            for img in soup.select(source['selector']):
                img_url = img['src']
                if not img_url.startswith('http'):
                    img_url = f"https:{img_url}" if img_url.startswith('//') else f"{source['url']}/{img_url}"
                
                icon_name = f"{source['name']}_{downloaded}.{source['format']}"
                save_path = f"src/icons/{source['format']}/{icon_name}"
                
                if not os.path.exists(save_path):
                    try:
                        urllib.request.urlretrieve(img_url, save_path)
                        downloaded += 1
                        print(f"Downloaded {icon_name} from {source['name']}")
                        time.sleep(1)  # Be polite with scraping
                    except Exception as e:
                        print(f"Failed to download {img_url}: {str(e)}")
            return downloaded
    except Exception as e:
        print(f"Error scraping from {source['name']}: {str(e)}")
    return 0

def download_icons(max_icons=1000):
    downloaded_count = 0
    
    for source in ICON_SOURCES:
        if downloaded_count >= max_icons:
            break
            
        print(f"\nFetching from {source['name']}...")
        try:
            if source['type'] == 'api':
                count = download_from_github_api(source)
            elif source['type'] == 'github':
                count = download_from_github_ui(source)
            elif source['type'] == 'scrape':
                count = download_from_scrape(source)
            else:
                print(f"Unknown source type: {source['type']}")
                continue
                
            downloaded_count += count
            print(f"Downloaded {count} icons from {source['name']}")
            
        except Exception as e:
            print(f"Error processing {source['name']}: {str(e)}")
    
    print(f"\nTotal icons downloaded: {downloaded_count}")

if __name__ == "__main__":
    download_icons()