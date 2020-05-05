import requests
import json

from random import randrange
from math import ceil

TEST_URL = "https://fr.openfoodfacts.org/categorie/cremes-dessert-vanille.json"
PROD_PER_PAGE = 20

url_prod = requests.get(TEST_URL)
json_prod = url_prod.json()
nb_prod = json_prod.get('count')
nb_page = ceil(nb_prod / PROD_PER_PAGE)

print("Nb total produits : ", nb_prod)
print("Nb de pages : ", nb_page)

for i in range(20):
    nb_rand_page = randrange(1, nb_page)
    rand_url = "https://fr.openfoodfacts.org/categorie/cremes-dessert-vanille/" + str(nb_rand_page) + ".json"
    rand_url_prod = requests.get(rand_url)
    json_rand_url_prod = rand_url_prod.json()
    list_prod_rand_url = json_prod.get('products')
    print("Récupération de tous les produits de la page " + str(nb_rand_page))
    
    index = randrange(0, len(list_prod_rand_url))
    product = list_prod_rand_url[index]
    print("Récupération du produit : " + product["product_name"])







