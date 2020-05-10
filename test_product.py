import mysql.connector

import constants as const

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
print(result)

print("Total rows are:  ", len(result))
print("Printing each row")
for row in result:
    print("Id: ", row[0])
    print("Name: ", row[1])
    print("Json_id: ", row[2])
    print("URL: ", row[3])
    print("\n")

cursor.close()
print("...Disconnected from database")