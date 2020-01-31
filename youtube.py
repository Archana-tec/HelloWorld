import webbrowser
import urllib.request as req
from bs4 import BeautifulSoup

input_func = input('Enter the song to be played: ')
query = input_func.replace(' ','+')

url = ('https://www.youtube.com/results?search_query=' + query)
source_code = req.urlopen(url, timeout = 15)

soup = BeautifulSoup(source_code, "html.parser")
songs = soup.find_all('div', {'class':'yt-lockup-video'})
song = songs[0].contents[0].contents[0].contents[0]

try:
    link = song['href']
    webbrowser.open('https://www.youtube.com' + link)
except KeyError:
    print("Sorry nothing there")
