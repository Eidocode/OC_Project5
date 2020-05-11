import mysql.connector

import constants as const

from product import Product

connx = mysql.connector.connect(
    host = const.SRV_IP,
    user = const.USER_ID,
    password = const.USER_PWD,
    database = const.DB_NAME
)

#query_get_categories = """SELECT id, name, url FROM Categories"""

cursor = connx.cursor()
print("Connection Established...")
cursor.execute("SELECT * FROM Categories")
result = cursor.fetchall()

print("Total rows are:  ", len(result))
print("Printing each row")

list_prods = []
for row in result:
    # print("Id: ", row[0])
    # print("Name: ", row[1])
    # print("Json_id: ", row[2])
    # print("URL: ", row[3])
    # print("\n")

    print("Catégorie : " + row[1] + " | " + row[3])
    test_prod = Product(row[3], 10)
    for product in test_prod.products:
        list_prods.append(product)
        print('<--| Add ' + product["product_name"] + ' to list...')
    print ("LISTE : {} products".format(len(list_prods)))

cursor.close()
print("...Disconnected from database")