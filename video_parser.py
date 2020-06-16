import requests
from bs4 import BeautifulSoup

URL = 'https://football.ua/video/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': '*/*'}


def get_html(url):
    """Get site we need"""
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    """Get last and second last video from site"""
    soup = BeautifulSoup(html, "html.parser")
    new_video = str(soup.find_all("div", {'class': 'intro'})).split()
    new_video = new_video[8][6:new_video[8].find('.html') + 5]
    return new_video


def parse():
    """Start parsing"""
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print("Error")
