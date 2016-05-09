import datetime
import random
import requests


class RandomBeerSelector():
    def __init__(self, store_id):
        self.last_update = datetime.datetime.min
        self.available_beers = list()
        self.store_id = store_id

    def should_update(self):
        return datetime.datetime.now() - self.last_update > datetime.timedelta(hours=1)

    def update_beer_list(self):
        self.last_update = datetime.datetime.now()
        self.available_beers = list()
        products_url = 'http://lcboapi.com/products'
        params = {'store_id': self.store_id, 'per_page': 100, 'q': 'beer', 'page': 1}
        beers = requests.get(products_url, params).json()

        total = beers['pager']['total_pages']
        current_page = beers['pager']['current_page']
        while current_page <= total:
            for beer in beers['result']:
                if beer['inventory_count'] > 0:
                    self.available_beers.append(beer)
            current_page += 1
            params['page'] = current_page
            beers = requests.get(products_url, params).json()

    def choose_random_beer(self, blacklist):

        while self.available_beers:
            random_choice = random.randint(0,len(self.available_beers)-1)
            random_beer = self.available_beers[random_choice]
            if random_beer['id'] in blacklist:
                self.available_beers.pop(random_choice)
            else:
                self.available_beers.pop(random_choice)
                return random_beer
        return None
