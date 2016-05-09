import os
import bottle
import sqlite3
import random_beer_selector
import datetime

app = bottle.Bottle()
static_folder = os.path.join(os.path.realpath(__file__), '..', 'static')
conn = sqlite3.connect('beers_with_dates.db')
cursor = conn.cursor()


selector = random_beer_selector.RandomBeerSelector(511)

try:
    cursor.execute("CREATE TABLE BeersConsumed (BeerID int, Name varchar(255), DateSelected DATE);")
except:
    pass

@app.route('/', method='GET')
def home_page():
    return bottle.static_file("index.html", root=static_folder)

@app.route('/static/<filename>')
def send_static(filename):
    return bottle.static_file(filename, root=static_folder)

@app.route('/beer-select')
def select_beer_from_store():
    if selector.should_update():
        selector.update_beer_list()

    consumed_products = cursor.execute("SELECT * FROM BeersConsumed ORDER BY DateSelected DESC").fetchall()
    consumed_products_set = set()
    if consumed_products:
        consumed_products_set = set(zip(*consumed_products)[0])

    choice = selector.choose_random_beer(consumed_products_set)
    if choice:
        cursor.execute("INSERT INTO BeersConsumed VALUES (?, ?, ?)", (choice['id'], choice['name'], datetime.datetime.now()))
        conn.commit()
        #recent = cursor.execute("Select * FROM BeersConsumed Order by ")
    choice["previous"] = list()
    for i in range(0,min(len(consumed_products), 10)):
        choice["previous"].append(list(consumed_products[i]))
    return choice

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8000)