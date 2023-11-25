from bs4 import BeautifulSoup
import requests
import re
import psycopg2

url = 'https://harrypotter.fandom.com/wiki/Special:AllPages?from=1265'
response_general_page = requests.get(url)

soup = BeautifulSoup(response_general_page.text, 'html.parser')

all_pages_div = soup.find('div', class_='mw-allpages-body')
links = [link.get('href') for link in all_pages_div.find_all('a') if link.get('href')]
try:
    conn = psycopg2.connect('host=127.0.0.1 dbname=telekomHack user=postgres password=postgres')
except psycopg2.Error as e:
    print(e)



try:
    cur = conn.cursor()
except psycopg2.Error as e:
    print(e)

conn.set_session(autocommit=True)



for link in links:
    print(link)
    match = re.search(r'/wiki/(.*)', link)

    if match:
        date = match.group(1)

    link = f"https://harrypotter.fandom.com{link}"
    response_single_page = requests.get(link)
    
    soup = BeautifulSoup(response_single_page.text, 'html.parser')
    try:
        events_section = soup.find('span', id='Events').find_next('ul')
        events = [li.get_text().strip() for li in events_section.find_all('li')]
    except AttributeError:
        print("Events section not found or empty")



    try:
        births_section = soup.find('span', id='Births').find_next('ul')
        births = [li.get_text().strip() for li in births_section.find_all('li')]
    except AttributeError:
        print("Births section not found or empty")



    try:
        deaths_section = soup.find('span', id='Deaths').find_next('ul')
        deaths = [li.get_text().strip() for li in deaths_section.find_all('li')]
    except AttributeError:
        print("Births section not found or empty")

    for event in events:
        try:
            cur.execute('INSERT INTO harry_poter (dates, events) VALUES (%s, %s)', (date, event))
            print('Ok')
        except psycopg2.Error as e:
            print(e)
    

   