import mysql.connector

from colorama import init, deinit, Fore, Back, Style

from product import Product

import constants as const


connx = mysql.connector.connect(
        host = const.SRV_IP,
        user = const.USER_ID,
        password = const.USER_PWD,
        database = const.DB_NAME
    )


query_get_barcode = """SELECT barcode FROM Products """

query_test = """SELECT * FROM Categories WHERE name = 'Merguez'"""


cursor = connx.cursor()
print(Fore.GREEN + "Connection Established...")
    
cursor.execute(query_test)
result = cursor.fetchall()

cursor.execute(query_get_barcode)
barcodes_in_db = cursor.fetchall()

list_barcodes = []
for code in barcodes_in_db:
    list_barcodes.append(code[0])
    
cursor.close()


print (list_barcodes)
if '2420669020207' in list_barcodes:
    print("Code existant ")
else:
    print("Code inexistant ")

# nb = 1
# for catg in result:
#     print(Fore.BLUE + "Catégorie " + str(nb) + " : " + catg[1] + " | " + catg[3])
#     for i in range(const.PRODUCTS_PER_CATG):
#         get_prod = Product(catg[3])
    
#         for nb_try_code in range(3):
#             print(nb_try_code)
#             if (get_prod.products['code'] in barcodes_in_db) and nb_try_code < 2:
#                 print(Fore.YELLOW + get_prod.products['product_name'] + " already in database...")
#                 print(Fore.YELLOW + "Attempt to find another product... " + str(nb_try_code + 1) + "/3...")
#                 get_prod = Product(catg[3])
#             elif get_prod.products['code'] not in barcodes_in_db:
#                 print("ce produit n'est pas dans la base")
#                 break
#             else:
#                 print(Fore.YELLOW + "Attempt to find another product... " + str(nb_try_code + 1) + "/3...")
        
#         product_name = get_prod.products['product_name']
#         print("Produit " + str(i+1) + " : " + product_name + " | " + get_prod.products['code'])


deinit()


