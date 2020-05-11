import mysql.connector

from product import Product

import constants as const

try:
    connx = mysql.connector.connect(
        host = const.SRV_IP,
        user = const.USER_ID,
        password = const.USER_PWD,
        database = const.DB_NAME
    )

    query_insert_products = """INSERT INTO Products
                            (name, brand, description, nutriscore, category_id, location, barcode)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    query_get_categories = """SELECT * FROM Categories"""

    cursor = connx.cursor()
    print("Connection Established...")
    cursor.execute(query_get_categories)
    result = cursor.fetchall()
    cursor.close()

    for catg in result:
        print("Catégorie : " + catg[1] + " | " + catg[3])
        get_prod = Product(catg[3], 20)
        
        for product in get_prod.products:
            print('**************')
            product_name = product['product_name']
            print("Name = " + product_name)
            
            if 'brands' in product.keys():
                product_brand = product['brands']
                print("Brand = " + product_brand)
            else:
                product_brand = None
                print("No Brand...")
            
            if 'ingredients_text' in product.keys():
                product_description = product['ingredients_text']
            else:
                product_description = None

            if 'nutriscore_grade' in product.keys():
                product_nutriscore = product['nutriscore_grade']
            else:
                product_nutriscore = None
            
            if 'purchase_places' in product.keys():
                product_location = product['stores']
            else:
                product_location = None

            product_barcode = product['code']
            catg_id = catg[0]

            cursor = connx.cursor()
            insert_data = (product_name, product_brand, product_description, product_nutriscore, catg[0], product_location, product_barcode)
            cursor.execute(query_insert_products, insert_data)

            print('<--| Add ' + product["product_name"] + ' to Database...')
            connx.commit()
            print('**************')
        print(cursor.rowcount, "QUERY SUCCESSFULL...")
    
    print("Products injection successful !!!")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

finally:
    if (connx.is_connected()):
        connx.close()
        
        print("Mysql connection closed...")