import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from urllib.parse import urljoin

date = datetime.datetime.now().strftime("%Y-%m-%d")

# Read csv containing urls
cleantech_links = pd.read_csv('cleantech_urls.csv')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Get links from url homepage
def extract_links(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = [a['href'] for a in soup.find_all('a', href=True)]

        return sorted(set(links))
    
    except requests.exceptions.RequestException as e:
        print(f"{url}: {e}")
        return []

# Get links to pdf documents
def extract_pdf(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].lower().endswith('.pdf')]

        return sorted(set(links))
    
    except requests.exceptions.RequestException as e:
        print(f"{url}: {e}")
        return []

links = []
for index, row in cleantech_links.iterrows():
    url = row['Website']
    x = extract_links(url, headers=headers)
    links.append(x)
links = [link for sublist in links for link in sublist]

pdf = []
for link in links:
    links_pdf = extract_pdf(link, headers)
    pdf.append(links_pdf)
flat_pdf = [link for sublist in pdf for link in sublist]

df = pd.DataFrame(flat_pdf)

df.to_csv(f'pdfs-{date}.csv')
