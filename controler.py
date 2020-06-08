from colorama import init, deinit, Fore, Back, Style

from model.category import Category
from model.product import Product


init(autoreset=True)

class Controler:
    
    def __init__(self):
        pass

    def get_database_status(self):
        self.category = Category()
        self.product = Product()

        nb_categories = len(self.category.categories_in_db)
        nb_products = len(self.product.products_in_db)

        self.category._destroy()
        self.product._destroy()

        status = "La base contient actuellement : {} catégories | {} produits.".format(nb_categories, nb_products)
        return status
    
    def set_categories(self, nb_categories):
        category = Category()

        categories_to_set = category._get_from_api(nb_categories)
        category.set_to_db(categories_to_set)
        category._destroy()

        print("Controler : set_categories done...")
    
    def set_products(self, nb_products):
        product = Product()

        products_to_set = product._get_from_api(nb_products)
        product.set_to_db(products_to_set)
        product._destroy()

        print("Controler : set_products done...")
    
    def set_product_to_fav(self, product_to_set):
        product = Product()
        product.set_to_fav(product_to_set)
        product._destroy()
        print(product_to_set['name'] + ' a été ajouté aux favoris.')

    def set_products_in_category(self, nb_products, id_category):
        product = Product()
        category = Category()

        this_category = category.get_one_from_db(id_category)
        products_to_set = product._get_from_api(nb_products, this_category)
        product.set_to_db(products_to_set)
        
        product._destroy()
        category._destroy()

        print("Controler : set_products done...")
    
    def get_all_categories_info(self):
        category = Category()
        categories_get = category.get_all_from_db()
        category._destroy()

        for cat in categories_get:
            cat_id = cat[0]
            cat_name = cat[1]
            print(str(cat_id) + " : " + cat_name)
        
        return categories_get
    
    def get_category_info(self, id_category):
        category = Category()
        this_category = {}
        category_info = category.get_one_from_db(id_category)

        for c in category_info:
            this_category['id'] = c[0]
            this_category['name'] = c[1]
            this_category['json_id'] = c[2]
            this_category['url'] = c[3]

        category._destroy()

        if len(category_info) == 0:
            return None
        return this_category

    def get_all_products_info(self, category_id):
        product = Product()
        products = product.get_all_from_a_category(category_id)
        product._destroy()

        for prod in products:
            prod_id = prod[0]
            prod_name = prod[1]
            print(str(prod_id) + " : " + prod_name)
        
        print("--")
        print(str(len(products)) + " produits présents dans cette catégories")
        return products
    
    def get_all_favorites_info(self):
        product = Product()
        favorites = product.get_fav_from_db()
        product._destroy()

        for fav in favorites:
            fav_id = fav[0]
            fav_name = fav[2]
            print(str(fav_id) + " : " + fav_name)
        
        print("--")
        print(str(len(favorites)) + " produits présents dans la liste des favoris")
        return favorites

    def get_product_info(self, product_id, category_id):
        product = Product()
        this_product = {}
        product_info = product.get_one_from_db(product_id)

        for p in product_info:
            this_product['id'] = p[0]
            this_product['name'] = p[1]
            this_product['brand'] = p[2]
            this_product['description'] = p[3]
            this_product['nutriscore'] = p[4]
            this_product['category_id'] = p[5]
            this_product['places'] = p[6]
            this_product['stores'] = p[7]
            this_product['barcode'] = p[8]
        
        product._destroy()

        if int(this_product['category_id']) != int(category_id):
            return None
        return this_product
    
   


deinit()
