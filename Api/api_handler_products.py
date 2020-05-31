import requests
import json

from random import randrange
from math import ceil
from colorama import init, deinit, Fore, Back, Style

import utils.constants as const


init(autoreset=True)

class ApiHandlerProducts:
    """
    Class used to handle Products in API

    ...

    Attributes
    ----------
    category_url : string
        Category URL to browse
    
    nb_products : int
        Number of products in Category
    
    nb_pages : int
        Number of pages in category. By default, a category contains
        20 products
    
    nb_prod_to_get : int
        Number of products to get randomly in category. Define during 
        instantiation
    
    products : list
        List of products retrieved randomly
    
    Methods
    -------
    _get_all_products
        Returns a list of all products in the category
    
    get_random_products
        Returns a list of "nb_prod" products retrieved randomly
        
    """

    def __init__(self, category_url, nb_prod):
        self.category_url = category_url
        self.nb_products = 0
        self.nb_pages = 0
        self.nb_prod_to_get = int(nb_prod)
        self.products = self.get_random_products
        
    @property
    def _get_all_products(self):
        """Returns a list of all products in the category"""

        url_products = requests.get(self.category_url + ".json")  # Request Category URL
        json_products = url_products.json()
            
        self.nb_products = int(json_products.get('count'))  # Get Category number of products
        self.nb_pages = ceil(self.nb_products / const.PRODUCTS_PER_PAGE)  # Get Category number of pages

        list_all_prod = []

        i = 1
        for i in range(self.nb_pages):
            this_url = self.category_url + "/" + str(i) + ".json"
            this_url_products = requests.get(this_url)
            json_this_url_products = this_url_products.json()
            list_this_url_products = json_this_url_products.get('products')
            
            for product in list_this_url_products:
                list_all_prod.append(product)

        return list_all_prod
    
    @property
    def get_random_products(self):
        """Returns a list of "nb_prod" products retrieved randomly"""

        list_category_prods = self._get_all_products
        list_rand_prods = []

        nb_prod_to_get = self.nb_prod_to_get
        if self.nb_prod_to_get > len(list_category_prods):
            nb_prod_to_get = len(list_category_prods)
            print(Fore.YELLOW + "There are only " + str(nb_prod_to_get) +" products available in this category.")
        
        for i in range(nb_prod_to_get):
            index = randrange(0, len(list_category_prods))
            prod = list_category_prods.pop(index)
            list_rand_prods.append(prod)
            i += 1
        
        return list_rand_prods

deinit()