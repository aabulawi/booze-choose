import os
import bottle
import sqlite3
import random_beer_selector

app = bottle.Bottle()
static_folder = os.path.join(os.path.realpath(__file__), '..', 'static')
conn = sqlite3.connect('beers.db')
cursor = conn.cursor()


selector = random_beer_selector.RandomBeerSelector(511)

try:
    cursor.execute("CREATE TABLE BeersConsumed (BeerID int);")
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

    consumed_products = cursor.execute("SELECT * FROM BeersConsumed ORDER BY BeerID ASC").fetchall()
    if consumed_products:
        consumed_products = set(zip(*consumed_products)[0])

    choice = selector.choose_random_beer(consumed_products)
    if choice:
        cursor.execute("INSERT INTO BeersConsumed VALUES (%d)" % (choice['id']))
        conn.commit()
    return choice

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8000)