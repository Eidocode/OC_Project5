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

    def get_products(self):
        url_products = requests.get(self.category_url + ".json")
        json_products = url_products.json()
            
        nb_catg_products = json_products.get('count')
        nb_catg_pages = ceil(nb_catg_products / const.PRODUCTS_PER_PAGE)

        nb_prod = self.nb_products
        if self.nb_products > nb_catg_products:
            nb_prod = nb_catg_products

        for i in range(nb_prod):
            rand_num_page = randrange(1, nb_catg_pages)
            rand_url = self.category_url + "/" +str(rand_num_page) + ".json"
            rand_url_products = requests.get(rand_url)
            json_rand_url_products = rand_url_products.json()
            list_rand_url_products = json_rand_url_products.get('products')

            index = randrange(0, len(list_rand_url_products))
            product = list_rand_url_products[index]
            print("Get 1 product from page " + str(rand_num_page) + " : " + product["product_name"])

list_cat = Category(10)

for cat in list_cat.list_categories :
    print("Catégorie : " + cat["name"] + " | " + cat["url"])
    test_prod = Product(cat["url"], 10)
    test_prod.get_products()