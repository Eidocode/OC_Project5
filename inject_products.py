import mysql.connector

from product import Product

import constants as const

products = Category(30)

try:
    connx = mysql.connector.connect(
        host = const.SRV_IP,
        user = const.USER_ID,
        password = const.USER_PWD,
        database = const.DB_NAME
    )

    query_insert_products = """INSERT INTO Products
                            (name, brand, decription, nutriscore, category_id, location, barcode)
                            VALUES (%s, %s, %s)"""

    query_get_categories = """SELECT id, name """

    
    
    cursor = connx.cursor()
    print("Connection Established...")








    for test in tests.list_categories:
        insert_data = (test['name'], test['id'], test['url'])
        cursor.execute(insert_query_categories, insert_data)
    connx.commit()
    print(cursor.rowcount, "QUERY SUCCESSFULL...")
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

finally:
    if (connx.is_connected()):
        connx.close()
        print("Mysql connection closed...")