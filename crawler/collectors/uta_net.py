import requests
from bs4 import BeautifulSoup


def get_uta_net_lyrics(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find(id='kashi_area').get_text().strip()

# TODO ERROR PROTECTION
