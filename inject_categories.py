import mysql.connector

from colorama import init, deinit, Fore, Back, Style

from category import Category

import constants as const


categories = Category(const.NB_CATEGORIES_TO_GET)

try:
    connx = mysql.connector.connect(
        host = const.SRV_IP,
        user = const.USER_ID,
        password = const.USER_PWD,
        database = const.DB_NAME
    )

    insert_query_categories = """INSERT INTO Categories (name, json_id, url)
                            VALUES
                            (%s, %s, %s)"""

    cursor = connx.cursor()
    print(Fore.GREEN + "Connection Established...")

    insert_data = []
    for category in categories.categories:
        data = (category['name'], category['id'], category['url'])
        insert_data.append(data)

    cursor.executemany(insert_query_categories, insert_data)
    print(Fore.GREEN + str(cursor.rowcount) + " QUERY SUCCESSFULL...")
    connx.commit()
    print(Fore.GREEN + "Categories injection successful !!!")
    cursor.close()

except mysql.connector.Error as error:
    print(Fore.RED + "Failed to insert record into table {}".format(error))

finally:
    if (connx.is_connected()):
        connx.close()
        print("Mysql connection closed...")

deinit()