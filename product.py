from colorama import init, deinit, Fore, Back, Style

import constants as const

from database_manager import DatabaseManager
from api_handler_products import ApiHandlerProducts
from category import Category


init(autoreset=True)

class Product:
    
    def __init__(self):
        pass

    def get_barcodes_from_db(self):
        db_manager = DatabaseManager()
        barcodes = []
        barcodes_from_db = []

        query_get_barcode = """SELECT barcode FROM Products """

        barcodes_from_db = db_manager.get_query(query_get_barcode)
        for code in barcodes_from_db:
            barcodes.append(code[0])
        
        db_manager._destroy()
        return barcodes

    def test_condition(self, condition, message):
        pass_test = True

        if condition:
            pass_test = False
            print(Fore.YELLOW + message)

        return pass_test
    
    def test_product(self, product, list_barcodes):
        test_pkey = self.test_condition(not('product_name' in product.keys()),
                            "Unable to find key product_name...")
        
        if test_pkey:
            test_pcode = self.test_condition(product['code'] in list_barcodes,
                                product['product_name'] + " already in list or database...")
            
            test_pname = self.test_condition(product['product_name'] == "",
                                "Product doesn't have a name...")
        else :
            return False
        
        return test_pkey == test_pcode == test_pname
    
    def _set_key_value(self, product, value):
        if value in product.keys():
            return product[value]
        return None

    def _get_value_for_db(self, categorie, product):
        product_name = product['product_name']
        product_brand = self._set_key_value(product, 'brands')
        product_description = self._set_key_value(product, 'ingredients_text')
        product_nutriscore = self._set_key_value(product, 'nutriscore_grade')
        product_places = self._set_key_value(product, 'purchase_places')
        product_stores = self._set_key_value(product, 'stores')
        product_barcode = product['code']

        product_values =  (product_name, product_brand, product_description, product_nutriscore,
                            categorie[0], product_places, product_stores, product_barcode)
        
        return product_values


    def _get_from_api(self, nb_prod):
        list_products = []
        barcodes = []
        category = Category()
        categories_in_db = category.categories_in_db

        barcodes = self.get_barcodes_from_db()
        i = 0
        for category in categories_in_db:
            print(Fore.BLUE + str(i+1) + " : " + category[1])
            products = ApiHandlerProducts(category[3], nb_prod)
            nb = 0
            for product in products.products:
                is_viable = self.test_product(product, barcodes)
                if is_viable:
                    this_product = self._get_value_for_db(category, product)
                    list_products.append(this_product)
                    barcodes.append(product['code'])
                    print(Fore.GREEN + str(nb+1) + ". " + product['product_name'] + " viable...")
                    nb += 1
                else:
                    print(Fore.RED + "Product not viable...")
                    continue
            
            i += 1

        return list_products
    
    def set_to_db(self, datas_to_inject):
        db_manager = DatabaseManager()

        insert_query = """INSERT INTO Products
                            (name, brand, description, nutriscore, category_id, places, stores, barcode)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        db_manager.set_query(insert_query, datas_to_inject)
        db_manager._destroy()
    
    def _destroy(self):
        print(Fore.LIGHTYELLOW_EX + "Instance Product has been deleted")
        del self


# product = Product()
# liste = product._get_from_api(const.PRODUCTS_PER_CATG)

# product.set_to_db(liste)
# product._destroy()

deinit()