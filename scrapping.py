from bs4 import BeautifulSoup
import requests
import re
import psycopg2

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


for index in range(0, 10):
   
    pagination = soup.select('.mw-allpages-nav a')
    pagination_links = [element['href'] for element in pagination]

    if index >= 1:
        response_general_page = requests.get(pagination_links[0])
        soup = BeautifulSoup(response_general_page.text, 'html.parser')
        all_pages_div = soup.find('div', class_='mw-allpages-body')
        links = [link.get('href') for link in all_pages_div.find_all('a') if link.get('href')]
            

    

    try:
        cur.execute('CREATE table harry_potter (date varchar(256), births TEXT, deaths TEXT, events TEXT, etymology TEXT, appearances TEXT, biography TEXT, history TEXT, known_staff TEXT, known_patients TEXT, description TEXT, residents_of_privet_driver TEXT,behind_the_scenes TEXT, magical_education TEXT, magical_government TEXT, magical_creatures TEXT, magical_plants TEXT, pratitioners_of_ancient_magic TEXT)')
        print('Ok')
    except psycopg2.Error as e:
        print(e)

    for link in links:
        print(link)
        match = re.search(r'/wiki/(.*)', link)

        if match:
            date = match.group(1)


        deaths = ''
        events = ''
        births = ''
        etymology = ''
        appearances = ''
        biography = ''
        history = ''
        known_staff = ''
        known_patients = ''
        residents_of_privet_driver = ''
        behind_the_scenes = ''
        magical_education = ''
        magical_government = ''
        magical_plants, magical_creatures, magical_creatures

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
        
        try:
            etymology_section = soup.find('span', id='Etymology').find_next('ul')
            etymology = [li.get_text().strip() for li in etymology_section.find_all('li')]
        except AttributeError:
            print("BirEtymologyths section not found or empty")
        
        try:
            appearances_section = soup.find('span', id='Appearances').find_next('ul')
            appearances = [li.get_text().strip() for li in appearances_section.find_all('li')]
        except AttributeError:
            print("Appearances section not found or empty")
        
        try:
            biography_section = soup.find('span', id='Biography').find_next('ul')
            biography = [li.get_text().strip() for li in biography_section.find_all('li')]
        except AttributeError:
            print("Appearances section not found or empty")

        
        try:
            history_section = soup.find('span', id='History').find_next('ul')
            history = [li.get_text().strip() for li in history_section.find_all('li')]
        except AttributeError:
            print("History section not found or empty")
            
        try:
            known_staff_section = soup.find('span', id='Known_staff').find_next('ul')
            known_staff = [li.get_text().strip() for li in known_staff_section.find_all('li')]
        except AttributeError:
            print("known_staff section not found or empty")

        try:
            known_patients_section = soup.find('span', id='Known_patients').find_next('ul')
            known_patients = [li.get_text().strip() for li in known_patients_section.find_all('li')]
        except AttributeError:
            print("known_patients section not found or empty")

        try:
            residents_of_privet_driver_section = soup.find('span', id='Residents_of_privet_driver').find_next('ul')
            residents_of_privet_driver = [li.get_text().strip() for li in residents_of_privet_driver_section.find_all('li')]
        except AttributeError:
            print("residents_of_privet_driver section not found or empty")
        

        try:
            behind_the_scenes_section = soup.find('span', id='Behind_the_scenes').find_next('ul')
            behind_the_scenes = [li.get_text().strip() for li in behind_the_scenes_section.find_all('li')]
        except AttributeError:
            print("behind_the_scenes section not found or empty")

        
        try:
            magical_education_section = soup.find('span', id='Magical_education').find_next('ul')
            magical_education = [li.get_text().strip() for li in magical_education_section.find_all('li')]
        except AttributeError:
            print("magical_education section not found or empty")

        
        try:
            magical_government_section = soup.find('span', id='Magical_government').find_next('ul')
            magical_government = [li.get_text().strip() for li in magical_government_section.find_all('li')]
        except AttributeError:
            print("magical_government section not found or empty")

        
        try:
            magical_plants_section = soup.find('span', id='Magical_plants').find_next('ul')
            magical_plants = [li.get_text().strip() for li in magical_plants_section.find_all('li')]
        except AttributeError:
            print("magical_plants section not found or empty")

        
        try:
            magical_creatures_section = soup.find('span', id='Magical_creatures').find_next('ul')
            magical_creatures = [li.get_text().strip() for li in magical_creatures_section.find_all('li')]
        except AttributeError:
            print("magical_creatures section not found or empty")

        
        
        try:
            practitioners_of_ancient_magic_section = soup.find('span', id='Practitioners_of_ancient_magic').find_next('ul')
            practitioners_of_ancient_magic = [li.get_text().strip() for li in practitioners_of_ancient_magic_section.find_all('li')]
        except AttributeError:
            print("practitioners_of_ancient_magic section not found or empty")


        try:
            personality_and_traits_section = soup.find('span', id='Personality_and_traits').find_next('ul')
            personality_and_traits = [li.get_text().strip() for li in personality_and_traits_section.find_all('li')]
        except AttributeError:
            print("personality_and_traits section not found or empty")
        
        try:
            relationships_section = soup.find('span', id='Relationships').find_next('ul')
            relationships = [li.get_text().strip() for li in relationships_section.find_all('li')]
        except AttributeError:
            print("relationships section not found or empty")



        
        


        
        if len(deaths) > 0 or len(births) > 0 or len(events) > 0:
            try:
                cur.execute('INSERT INTO harry_potter (dates, events, deaths, births) VALUES (%s, %s, %s, %s)', (date, events, deaths, births))
                print('Ok')
            except psycopg2.Error as e:
                print(e)
        

    