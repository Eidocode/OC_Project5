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

        # nb_prod = self.nb_products
        # if self.nb_products > nb_catg_products: # Check if nb_products is greater than Category number of products 
        #                                         # to avoid a bug in range(nb_product) below...
        #     nb_prod = nb_catg_products
        
        rand_num_page = randrange(1, self.nb_pages)
        rand_url = self.category_url + "/" + str(rand_num_page) + ".json"  
        rand_url_products = requests.get(rand_url)  # Get content of a random page number
        json_rand_url_products = rand_url_products.json()
        list_rand_url_products = json_rand_url_products.get('products')  # Get products in random URL

        index = randrange(0, len(list_rand_url_products))
        self.products = list_rand_url_products[index]
        #print("|--> Get 1 product from page " + str(rand_num_page) + " : " + self.products[-1]["product_name"])
        
        return self.products