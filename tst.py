import requests
from bs4 import BeautifulSoup

url = 'https://harrypotter.fandom.com/wiki/Special:AllPages?from=1265'
response_general_page = requests.get(url)

soup = BeautifulSoup(response_general_page.text, 'html.parser')

# Use the specific selector div.mw-allpages-nav a + a
pagination = soup.select('div.mw-allpages-nav a + a')
pagination_links = [element['href'] for element in pagination]
for pag in pagination_links:
    print(pag)