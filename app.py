import os
import bottle
import requests
import sqlite3
import random

app = bottle.Bottle()
static_folder = os.path.join(os.path.realpath(__file__), '..', 'static')
conn = sqlite3.connect('beers.db')
cursor = conn.cursor()
print static_folder
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
    store_id = 511
    total_pages = get_number_of_pages(store_id)
    order = range(1,total_pages+1)
    random.shuffle(order)

    consumed_products = cursor.execute("SELECT * FROM BeersConsumed ORDER BY BeerID ASC").fetchall()
    if consumed_products:
        consumed_products = set(zip(*consumed_products)[0])

    for page in order:
        products = get_shuffled_set_of_products(page, store_id)
        for product in products:
            if product['id'] not in consumed_products and in_stock(store_id, product['id']):
                cursor.execute("INSERT INTO BeersConsumed VALUES (%d)" % (product['id']))
                conn.commit()
                return product
    return None

def get_number_of_pages(store_id):
    products_url = 'http://lcboapi.com/products'
    params = {'store_id': store_id, 'per_page': 100, 'q': 'beer'}
    return requests.get(products_url, params).json()['pager']['total_pages']

def get_shuffled_set_of_products(page, store_id):
    products_url = 'http://lcboapi.com/products'
    params = {'store_id': store_id, 'per_page': 100, 'q': 'beer', 'page':page}
    products = requests.get(products_url, params).json()['result']
    random.shuffle(products)
    return products

def in_stock(store_id, product_id):
    inventory_url = 'http://lcboapi.com/stores/%d/products/%d/inventory' % (store_id, product_id)
    data = requests.get(inventory_url).json()
    if data['result']['quantity'] > 0:
        return True
    return False

if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8000)