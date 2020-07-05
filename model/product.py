from colorama import init, deinit, Fore

from database.database_manager import DatabaseManager
from api.api_handler_products import ApiHandlerProducts
from model.category import Category


init(autoreset=True)


class Product:
    """
    Class used to manipulate products

    ...

    Attributes
    ----------


    Methods
    -------
    get_all_from_db
        Returns a list containing all products from database

    get_one_from_db(product_id)
        Returns a product from database defined by product_id

    get_barcodes_from_db
        Returns a list with barcodes values from database

    test_condition(condition, message)
        Returns True or False if 'condition'

    test_product(product, list_barcodes)
        Test some keys and values from dict product

    _set_key_value(product, value)
        Returns a value if value exist in product.keys

    _get_value_for_db(categorie, product)
        Returns a tuple with define values based on categorie and product

    _get_from_api(nb_prod)
        Returns a list of products recovered from API

    get_all_from_a_category(category_id)
        Returns a list containing all products in a category, defined
        by category_id

    get_fav_from_db(self):
        Returns a list containing all products from table Favoris

    set_to_db(datas_to_inject)
        Set a tuple of products to set in database

    set_to_fav(self, product):
        Set product to database in table Favoris
    """

    def __init__(self):
        self.products_in_db = self.get_all_from_db()

    def get_all_from_db(self):
        """Returns a list containing all products from database
        """
        db_manager = DatabaseManager()
        list_products = []

        query_get_products = """SELECT * FROM Products"""

        list_products = db_manager.get_query(query_get_products)
        db_manager._destroy()
        return list_products

    def get_one_from_db(self, product_id):
        """Returns a product from database

        Parameters
        ----------
        product_id : int
            ID of the product to get
        """

        db_manager = DatabaseManager()
        this_product = []

        query_get_products = """SELECT * FROM Products WHERE id
                                 = """ + str(product_id)

        this_product = db_manager.get_query(query_get_products)
        db_manager._destroy()
        return this_product

    def get_barcodes_from_db(self):
        """Returns a list with barcodes values from database
        """
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
        """Returns True or False if 'condition'

        Parameters
        ----------
        condition
            The condition to verify

        message : string
            The message to print
        """

        pass_test = True

        if condition:
            pass_test = False
            print(Fore.YELLOW + message)

        return pass_test

    def test_product(self, product, list_barcodes):
        """Test some keys and values from dict product

        Parameters
        ----------
        product : dict
            Contains product values to test

        list_barcode: list
            List of products barcodes in database
        """

        test_pkey = self.test_condition(not('product_name' in product.keys()),
                                        "Unable to find key product_name...")

        if test_pkey:
            test_pcode = self.test_condition(product['code'] in list_barcodes,
                                             product['product_name'] +
                                             " already in list or database...")

            test_pname = self.test_condition(product['product_name'] == "",
                                             "Product doesn't have a name...")
        else:
            return False

        return test_pkey == test_pcode == test_pname

    def _set_key_value(self, product, value):
        """Returns a value if value exist in product.keys,
        else, returns NONE value

        Parameters
        ----------
        product : dict
            Contains product keys and values

        value
            The value to check in keys
        """

        if value in product.keys():
            return product[value]
        return None

    def _get_value_for_db(self, category, product):
        """Returns a tuple with define values based on categorie and product

        Parameters
        ----------
        category
            Current category

        product
            Current product
        """
        product_name = product['product_name']
        product_brand = self._set_key_value(product, 'brands')
        product_description = self._set_key_value(product, 'ingredients_text')
        product_nutriscore = self._set_key_value(product, 'nutriscore_grade')
        product_places = self._set_key_value(product, 'purchase_places')
        product_stores = self._set_key_value(product, 'stores')
        product_barcode = product['code']

        product_values = (product_name, product_brand, product_description,
                          product_nutriscore, category[0], product_places,
                          product_stores, product_barcode)

        return product_values

    def _get_from_api(self, nb_prod, categories_in_db='default'):
        """Returns a list of products recovered from API

        Parameters
        ----------
        nb_prod : int
            Number of products to recover
        """

        list_products = []
        barcodes = []
        category = Category()

        if categories_in_db == 'default':
            categories_in_db = category.categories_in_db

        barcodes = self.get_barcodes_from_db()
        i = 0

        for cat in categories_in_db:
            print(Fore.BLUE + str(i+1) + " : " + cat[1])
            products = ApiHandlerProducts(cat[3], nb_prod)
            nb = 0
            for product in products.products:
                is_viable = self.test_product(product, barcodes)
                if is_viable:
                    this_product = self._get_value_for_db(cat, product)
                    list_products.append(this_product)
                    barcodes.append(product['code'])
                    str1 = "{}. {} viable...".format(
                                        str(nb+1), product['product_name'])
                    print(Fore.GREEN + str1)
                    nb += 1
                else:
                    print(Fore.RED + "Product not viable...")
                    continue

            i += 1
        category._destroy()

        return list_products

    def get_all_from_a_category(self, category_id):
        """Returns a list containing all products in a category

        Parameters
        ----------
        category_id : int
            ID of the category where all products will be returned
        """

        db_manager = DatabaseManager()
        list_products = []

        query_get_products = """SELECT * FROM Products WHERE
                                 category_id = """ + category_id

        list_products = db_manager.get_query(query_get_products)
        db_manager._destroy()

        return list_products

    def get_fav_from_db(self):
        """Returns a list containing all products from table Favoris
        """
        db_manager = DatabaseManager()
        list_fav = []

        query_get_favorites = """SELECT Favoris.id, Favoris.product_id,
                                 Products.name, Products.brand,
                                 Products.description, Products.nutriscore,
                                 Products.places, Products.stores,
                                 Products.barcode, Favoris.added_date
                                 FROM Products INNER JOIN Favoris
                                 ON Favoris.product_id = Products.id"""

        list_fav = db_manager.get_query(query_get_favorites)
        db_manager._destroy()

        return list_fav

    def set_to_db(self, datas_to_inject):
        """Set a tuple of products in database

        Parameters
        ----------
        datas_to_inject : tuple
            Contains values to be injected in database
        """

        db_manager = DatabaseManager()

        insert_query = """INSERT INTO Products
                            (name, brand, description, nutriscore, category_id,
                             places, stores, barcode)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        db_manager.set_query(insert_query, datas_to_inject, True)
        db_manager._destroy()

    def set_to_fav(self, product):
        """Set product to database in table Favoris

        Parameters
        ----------
        product : tuple
            Contains values to be injected in table Favoris
        """
        db_manager = DatabaseManager()

        insert_query = """INSERT INTO Favoris
                            (product_id)
                            VALUES (%s)"""

        db_manager.set_query(insert_query, (str(product['id']),), False)
        db_manager._destroy()

    def _destroy(self):
        print(Fore.LIGHTYELLOW_EX + "Instance Product has been deleted")
        del self


deinit()
