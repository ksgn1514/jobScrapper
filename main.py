from requests import get
from bs4 import BeautifulSoup

base_url = 'https://weworkremotely.com/remote-jobs/search?=✓&term='
search_term = 'python'

response = get(f"{base_url}{search_term}")
if response.status_code != 200:
    print(f"Error: {response.status_code}")
else:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.find_all('title'))