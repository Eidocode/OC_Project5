import mysql.connector

from colorama import init, deinit, Fore, Back, Style

from product import Product

import constants as const


init(autoreset=True)

def is_ascii(str):
    for char in str:
        if ord(char) > 128:
            return False
    return True

def test_product(condition, message, nb_try, bool_prod):
    bool_prod = True
    for nb in range(nb_try):
        if condition and nb < 2 and bool_prod:
            print(Fore.YELLOW + message)
            print(Fore.YELLOW + "Attempt to find another product... " + str(nb + 1) + "/3...")
            get_prod = Product(catg[3])
        elif not condition:
            break
            bool_prod = True
        else:
            print(Fore.YELLOW + "Attempt to find another product... " + str(nb + 1) + "/3...")
            bool_prod = False
    
    return bool_prod

def get_product_datas(product, value):
    if value in product.products.keys():
        return product.products[value]
    return None


try:
    connx = mysql.connector.connect(
        host = const.SRV_IP,
        user = const.USER_ID,
        password = const.USER_PWD,
        database = const.DB_NAME
    )

    query_insert_products = """INSERT INTO Products
                            (name, brand, description, nutriscore, category_id, places, stores, barcode)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    query_get_categories = """SELECT * FROM Categories"""
    query_get_barcode = """SELECT barcode FROM Products """
    #query_test = """SELECT * FROM Categories WHERE name = 'Merguez'"""

    cursor = connx.cursor()
    print(Fore.GREEN + "Connection Established...")
    
    cursor.execute(query_get_categories)
    result = cursor.fetchall()

    cursor.execute(query_get_barcode)
    barcodes_in_db = cursor.fetchall()

    list_barcodes = []
    for code in barcodes_in_db:
        list_barcodes.append(code[0])
    
    cursor.close()

    nb = 1
    datas_to_insert = []
    for catg in result:
        print(Fore.BLUE + "Category " + str(nb) + " : " + catg[1] + " | " + catg[3])
        for i in range(const.PRODUCTS_PER_CATG):
            get_prod = Product(catg[3])
            product_viable = True
            
            # if not is_ascii(get_prod.products['product_name']):
            #     print(Fore.MAGENTA + "product_name contains 4 bytes character... passing iteration...")
            #     product_viable = False
            # else:
            #     product_viable = True

            test_pkey = test_product(not('product_name' in get_prod.products.keys()),
                                "Unable to find key product_name...", const.NB_TRY, product_viable)
            
            test_pcode = test_product(get_prod.products['code'] in list_barcodes,
                                get_prod.products['product_name'] + " already in database...",
                                const.NB_TRY, product_viable)

            test_pname =test_product(get_prod.products['product_name'] == "", "Product doesn't have a name...",
                                const.NB_TRY, product_viable)

            product_viable = (test_pkey == test_pcode == test_pname)
            
            if not product_viable:
                print(Fore.RED + "Unable to find another product... " + get_prod.products['code'])
                continue
            else:
                product_name = get_prod.products['product_name']
                print("Product " + str(i+1) + " : " + product_name + " | " + get_prod.products['code'])
                

                product_brand = get_product_datas(get_prod, 'brands')
                product_description = get_product_datas(get_prod, 'ingredients_text')
                product_nutriscore = get_product_datas(get_prod, 'nutriscore_grade')
                product_places = get_product_datas(get_prod, 'purchase_places')
                product_stores = get_product_datas(get_prod, 'stores')
                
                product_barcode = get_prod.products['code']
                barcodes_in_db.append(product_barcode)
                catg_id = catg[0]

                cursor = connx.cursor()
                data_require = (product_name, product_brand, product_description, product_nutriscore, catg[0], product_places, product_stores, product_barcode)
                datas_to_insert.append(data_require)
        
        nb += 1

    if len(datas_to_insert) > 0:
        cursor.executemany(query_insert_products, datas_to_insert)
        print(Fore.GREEN + str(cursor.rowcount) + " QUERY SUCCESSFULL...")
        connx.commit()
        print(Fore.GREEN + "Products injection successful !!!")
    else:
        print(Fore.GREEN + "No data to insert...")
    
    cursor.close()

except mysql.connector.Error as error:
    print(Fore.RED + "Failed to insert record into table {}".format(error))
    for data in datas_to_insert:
        print(data)

finally:
    if (connx.is_connected()):
        connx.close()
        print("Mysql connection closed...")

deinit()