import requests
from bs4 import BeautifulSoup

url = 'https://harrypotter.fandom.com/wiki/Harry_Potter_and_the_Deathly_Hallows:_Part_2'
response_general_page = requests.get(url)

soup = BeautifulSoup(response_general_page.text, 'html.parser')

# Use the specific selector div.mw-allpages-nav a + a

events_section = soup.find('div', class_='mw-parser-output').get_text()



print(events_section)

