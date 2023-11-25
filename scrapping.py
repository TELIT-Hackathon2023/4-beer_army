from bs4 import BeautifulSoup
import requests
import re
import psycopg2

def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.replace('"', "")
    s = s.replace('[1]', "")
    s = s.replace('_', " ")
    s = s.replace(':', "")
    s = s.replace('%', " ")
    s = s.strip()
    
    return s



url = 'https://harrypotter.fandom.com/wiki/Special:AllPages'
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
try:
    cur.execute('CREATE table harry_potter (full_data TEXT)')
    print('Ok')
except psycopg2.Error as e:
    print(e)

for index in range(0, 25):
   
    if index == 0:
        url = 'https://harrypotter.fandom.com/wiki/Special:AllPages'

    if index == 1:
        
        response_general_page = requests.get(url)
        soup = BeautifulSoup(response_general_page.text, 'html.parser')
        pagination = soup.select('.mw-allpages-nav a')
        pagination_links = [element['href'] for element in pagination]
        print(pagination_links[0])
        pagination_l = f"https://harrypotter.fandom.com{pagination_links[0]}"
        response_general_page = requests.get(pagination_l)
        soup = BeautifulSoup(response_general_page.text, 'html.parser')
        all_pages_div = soup.find('div', class_='mw-allpages-body')
        links = [link.get('href') for link in all_pages_div.find_all('a') if link.get('href')]
        url = pagination_l

    elif index > 1:
        
        response_general_page = requests.get(url)
        soup = BeautifulSoup(response_general_page.text, 'html.parser')
        pagination = soup.select('.mw-allpages-nav a + a')
        pagination_links = [element['href'] for element in pagination]
        print(pagination_links[0])
        pagination_l = f"https://harrypotter.fandom.com{pagination_links[0]}"
        response_general_page = requests.get(pagination_l)
        soup = BeautifulSoup(response_general_page.text, 'html.parser')
        all_pages_div = soup.find('div', class_='mw-allpages-body')
        links = [link.get('href') for link in all_pages_div.find_all('a') if link.get('href')]
        url = pagination_l

    

    

    for link in links:
        
       
        data_full = ''
        
        link = f"https://harrypotter.fandom.com{link}"
        response_single_page = requests.get(link)
        
        soup = BeautifulSoup(response_single_page.text, 'html.parser')
        try:
            data_full = soup.find('div', class_='mw-parser-output').get_text()
            data_full = normalize_text(data_full)
        except AttributeError:
            print("section not found or empty")



        if len(data_full) > 0:
            try:
                cur.execute('INSERT INTO harry_potter (full_data) VALUES (%s)', [data_full])
                print('Ok')
            except psycopg2.Error as e:
                print(e)
        
        


        
        
        

    