import requests
import json

from random import randrange

import constants as const


class ApiHandlerCategories:
    """
    Class used to handle Categories in API

    ...

    Attributes
    ----------
    nb_cat : int
        Number of categories to handle
    
    categories : list
        list of categories retrieved randomly
    
    Methods
    -------
    _get_categories
        Returns all categories retrieved according to the filters 
        defined in the method
    
    get_random_categories
        Returns "nb_cat" random categories 
    """
    
    def __init__(self, nb_cat):
        self.nb_cat = nb_cat
        self.categories = self.get_random_categories
    
    @property
    def _get_categories(self):
        """Returns all categories retrieved according to the filters 
        defined in the method 
        """
        list_cat = []
        list_cat_filtered = []

        url_cat = requests.get(const.URL + 'categories.json')
        json_cat = url_cat.json()
        list_cat = json_cat.get('tags')

        for category in list_cat:
            if (category['products'] >= const.MIN_PRODUCTS_TO_FILTER and category["id"].startswith('fr')) :
                url_category = requests.get(category['url'] + '.json')
                json_category = url_category.json()
                nb_products = int(json_category.get('count'))
                if nb_products != None:
                    if nb_products >= const.MIN_PRODUCTS_TO_FILTER:
                        list_cat_filtered.append(category)

        print("Nb. categories >= 100 products : " + str(len(list_cat_filtered)))
        return list_cat_filtered

    @property
    def get_random_categories(self):
        """Returns "nb_cat" random categories"""
        self.categories = []
        lst = self._get_categories

        for i in range(self.nb_cat):
            index = randrange(0, len(lst))
            while 'lst[index]' in self.categories:
                index = randrange(0, len(lst))
            self.categories.append(lst[index])

        return self.categories