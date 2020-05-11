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
                            (name, category_id, barcode)
                            VALUES (%s, %s, %s)"""

    query_get_categories = """SELECT * FROM Categories"""

    cursor = connx.cursor()
    print("Connection Established...")
    cursor.execute(query_get_categories)
    result = cursor.fetchall()
    cursor.close()

    for catg in result:
        print("Catégorie : " + catg[1] + " | " + catg[3])
        get_prod = Product(catg[3], 10)

        for product in get_prod.products:
            cursor = connx.cursor()
            insert_data = (product['product_name'], catg[0], product['code'])
            cursor.execute(query_insert_products, insert_data)
            print(product['product_name'], catg[0], product['code'])
            print('<--| Add ' + product["product_name"] + ' to list...')
            connx.commit()
            print(cursor.rowcount, "QUERY SUCCESSFULL...")

    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

finally:
    if (connx.is_connected()):
        connx.close()
        print("Mysql connection closed...")