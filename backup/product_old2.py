import requests
import json

from random import randrange
from math import ceil

from category import Category

import constants as const


class Product:

    def __init__(self, category_url):
        self.category_url = category_url
        self.nb_products = 0
        self.nb_pages = 0
        self.products = self._get_products
        
    @property
    def _get_products(self):
        url_products = requests.get(self.category_url + ".json")  # Request Category URL
        json_products = url_products.json()
            
        self.nb_products = int(json_products.get('count'))  # Get Category number of products
        self.nb_pages = ceil(self.nb_products / const.PRODUCTS_PER_PAGE)  # Get Category number of pages

        list_all_prod = []
        self.products = []

        i = 1
        for i in range(self.nb_pages):
            this_url = self.category_url + "/" + str(i) + ".json"
            this_url_products = requests.get(this_url)
            json_this_url_products = this_url_products.json()
            list_this_url_products = json_this_url_products.get('products')
            
            for product in list_this_url_products:
                list_all_prod.append(product)


        # rand_num_page = randrange(1, self.nb_pages)
        # rand_url = self.category_url + "/" + str(rand_num_page) + ".json"
        # rand_url_products = requests.get(rand_url)  # Get content of a random page number
        # json_rand_url_products = rand_url_products.json()
        # list_rand_url_products = json_rand_url_products.get('products')  # Get products in random URL

        # index = randrange(0, len(list_rand_url_products))
        # self.products = list_rand_url_products[index]
        self.products = list_all_prod
        return self.products

prod = Product('https://fr.openfoodfacts.org/categorie/wraps')
print(len(prod.products))

for i in range(10):
    rand_index = randrange(1, len(prod.products))
    print(prod.products[rand_index]['product_name'])