import requests
import json

from random import randrange

URL = 'https://fr.openfoodfacts.org/'

class Category:
    
    def __init__(self, nb_cat):
        self.nb_cat = nb_cat
        self.list_categories = self.get_random_categories
    

    @property
    def _get_categories(self):
        list_cat = []
        list_cat_filtered = []

        url_cat = requests.get(URL + 'categories.json')
        json_cat = url_cat.json()
        list_cat = json_cat.get('tags')

        for category in list_cat:
            if (category["products"] >= 50 and category["id"].startswith('fr')) :
                list_cat_filtered.append(category)
        return list_cat_filtered

    @property
    def get_random_categories(self):
        self.list_categories = []
        lst = self._get_categories

        for i in range(self.nb_cat):
            index = randrange(0, len(lst))
            self.list_categories.append(lst[index])
        return self.list_categories