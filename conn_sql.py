import mysql.connector

from category import Category

tests = Category(30)

try:
    connx = mysql.connector.connect(
        host = "192.168.1.77",
        user = "student",
        password = "student",
        database = "pur_beurre"
    )

    insert_query_categories = """INSERT INTO Categories (name, json_id, url)
                            VALUES
                            (%s, %s, %s)"""

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