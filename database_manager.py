import mysql.connector

from colorama import init, deinit, Fore, Back, Style

import constants as const

from api_handler_categories import ApiHandlerCategories


init(autoreset=True)

class DatabaseManager:
    
    def __init__(self):
        self.sql_connx = mysql.connector.connect(
                host = const.SRV_IP,
                user = const.USER_ID,
                password = const.USER_PWD,
                database = const.DB_NAME
            )

    def get_query(self, query):
        result = None
        try:
            self.sql_connx
        
            cursor = self.sql_connx.cursor()
            print(Fore.GREEN + "Connection Established...")

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as error:
            print(Fore.RED + "Failed to get record from table {}".format(error))

        finally:
            if (self.sql_connx.is_connected()):
                self.sql_connx.close()
                print(Fore.GREEN + "Mysql connection closed...")
        
        return result

    def set_query(self, query, datas):
        try:
            self.sql_connx
        
            cursor = self.sql_connx.cursor()
            print(Fore.GREEN + "Connection Established...")

            cursor.executemany(query, datas)
            print(Fore.GREEN + str(cursor.rowcount) + " QUERY SUCCESSFULL...")
            self.sql_connx.commit()
            cursor.close()

        except mysql.connector.Error as error:
            print(Fore.RED + "Failed to insert record into table {}".format(error))

        finally:
            if (self.sql_connx.is_connected()):
                self.sql_connx.close()
                print(Fore.GREEN + "Mysql connection closed...")
    
    def _reset(self):
        self.__init__()
    
    def _destroy(self):
        del self


deinit()