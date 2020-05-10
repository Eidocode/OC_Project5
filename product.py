import requests
import json

from random import randrange
from math import ceil

from category import Category

import constants as const


class Product:

    def __init__(self, category_url, nb_products):
        self.category_url = category_url
        self.nb_products = nb_products
        self.products = self._get_products
        
    @property
    def _get_products(self):
        url_products = requests.get(self.category_url + ".json")  # Request Category URL
        json_products = url_products.json()
            
        nb_catg_products = int(json_products.get('count'))  # Get Category number of products
        nb_catg_pages = ceil(nb_catg_products / const.PRODUCTS_PER_PAGE)  # Get Category number of pages

        nb_prod = self.nb_products
        if self.nb_products > nb_catg_products: # Check if nb_products is greater than Category number of products 
                                                # to avoid a bug in range(nb_product) below...
            nb_prod = nb_catg_products

        self.products = []
        for i in range(nb_prod):
            rand_num_page = randrange(1, nb_catg_pages)
            rand_url = self.category_url + "/" + str(rand_num_page) + ".json"  # Get a random page number
            rand_url_products = requests.get(rand_url)
            json_rand_url_products = rand_url_products.json()
            list_rand_url_products = json_rand_url_products.get('products')  # Get products in random URL

            index = randrange(0, len(list_rand_url_products))
            self.products.append(list_rand_url_products[index])
            print("|--> Get 1 product from page " + str(rand_num_page) + " : " + self.products[-1]["product_name"])
        
        return self.products

list_catgs = Category(10)
list_prods = []

for cat in list_catgs.categories :
    print("Catégorie : " + cat["name"] + " | " + str(cat["products"]) + " products" + " | "+ cat["url"])
    test_prod = Product(cat["url"], 10)
    for product in test_prod.products:
        list_prods.append(product)
        print('<--| Add ' + product["product_name"] + ' to list...')
    print ("LISTE : {} products".format(len(list_prods)))



