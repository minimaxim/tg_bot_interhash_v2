import os
import psycopg2
import requests
from bs4 import BeautifulSoup
from loader import DATABASE_URL

def connect_to_db():

    conn = psycopg2.connect(
        host=f'{os.getenv("DATABASE_HOST")}',
        database=f'{os.getenv("DATABASE_NAME")}',
        user=f'{os.getenv("DATABASE_USERNAME")}',
        password=f'{os.getenv("DATABASE_PASSWORD")}'
    )
    return conn


def parser_asic():

    url = "https://whattomine.com/asic"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    asics = soup.find_all("div", {"class": "col-sm"})

    asics_list = []

    for x in asics:
        asics_list += x.text.strip().split('\n')

    new_asics_list = []

    not_accept = ['', 'W', 'Mh/s', 'h/s', 'Gh/s', 'kh/s', 'Th/s']

    for y in asics_list:
        if y not in not_accept:
            if y == 'SHA-256':
                new_asics_list.append('SHA256')
            elif y == 'Myr-Groestl':
                new_asics_list.append('MyrGroestl')
            elif y == 'Blake (14r)':
                new_asics_list.append('Blake14r')
            elif y != 'SHA-256' or y != 'Myr-Groestl' or y != 'Blake (14r)':
                new_asics_list.append(y)


    return new_asics_list


def insert_asic(new_asic):

    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""SELECT * from asics""")
    as_in_db = cur.fetchall()

    second_elements = [row[1] for row in as_in_db]

    for asic in new_asic:
        if asic in second_elements:
            pass
        else:
            cur.execute("""INSERT INTO asics (name) VALUES (%s)""", (asic,))
            conn.commit()

    cur.close()
    conn.close()


def parse_and_save():
    new_asic = parser_asic()
    insert_asic(new_asic)