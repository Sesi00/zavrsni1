import sqlite3
import yaml
import pandas as pd
import streamlit as st

# Učitavanje YAML fajla
with open('users.yml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

@st.cache_data
def load_data():
    df = pd.read_csv('Travel_details.csv', delimiter=',', encoding='latin-1')
    return df

df = load_data()

# Povezivanje sa SQLite bazom
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Kreiranje tablice users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        name TEXT,
        password TEXT
    )
''')


# Kreiranje tablice travel_details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS travel_details (
        Trip_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Destination_city TEXT,
        Destination_country TEXT,
        Start_date DATE,
        End_date DATE,
        Duration_days INTEGER,
        Traveler_name TEXT,                     
        Traveler_age INTEGER,
        Traveler_gender TEXT,
        City_of_residence TEXT,
        Traveler_nationality TEXT,
        Accommodation_type TEXT,
        Accommodation_cost INTEGER,
        Transportation_type TEXT,      
        Transportation_cost INTEGER      
)
''')



def load_data_to_sqlite(connection):
    df.to_sql('travel_details', connection, if_exists='append', index=False)
    connection.commit()

load_data_to_sqlite(connection)

# Ubacivanje korisničkih podataka u tablicu
for username, user_data in data['credentials']['usernames'].items():
    email = user_data['email']
    name = user_data['name']
    password = user_data['password']

     # Provjera da li email već postoji u tablici
    cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.execute('''
            INSERT INTO users (email, name, password)
            VALUES (?, ?, ?)
        ''', (email, name, password))
        print(f"User {email} added to the database.")
    else:
        print(f"User {email} already exists in the database. Skipping insertion.")

# Čuvanje promjena i zatvaranje veze
connection.commit()
connection.close()


