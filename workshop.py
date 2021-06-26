import requests
import sqlite3


def main(capital):
    try:
        r = requests.get(f'https://restcountries.eu/rest/v2/capital/{capital}')
        name = r.text.split('"')[3]
        domain = r.text.split('"')[7]
        phone_index = r.text.split('"')[19]
        currency = r.text.split('"')[77]
        region = r.text.split('"')[33]
        time_zone = r.text.split('"')[53]
        return [f"Name: {name}",f"Region: {region}", f"Timezone: {time_zone}", f"Currency: {currency}", f"Domain: {domain}"]
    except:
        pass




conn = sqlite3.connect('countries_db.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS countries 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20),
        domain VARCHAR(10),
        phone_index INTEGER,
        time_zone INTEGER,
        currency VARCHAR(10),
        region VARCHAR(10)
        )''')

rows = []

