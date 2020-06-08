import mysql.connector

from colorama import init, deinit, Fore, Back, Style

import utils.constants as const


init(autoreset=True)

class DatabaseManager:
    """ 
    Class used to communicate (/w credentials) with SQL server.
    Send "get"/"set" queries to database and return results...
    
    ...

    Attributes
    ----------
    sql_connx : tuple
        Contains SQL server informations like credentials, @IP, database name...
    
    Methods
    -------
    get_query(query)
        Returns results of a "get" query
        example : 'SELECT id, name, json_id FROM Categories WHERE id > 5'
    
    set_query(query, datas)
        Set datas to SQL database with a "set" query
        example : 'INSERT INTO Categories (name, json_id, url) VALUES (%s, %s, %s)'
    """

    def __init__(self):
        self.sql_connx = mysql.connector.connect(
                host = const.SRV_IP,
                user = const.USER_ID,
                password = const.USER_PWD,
                database = const.DB_NAME
            )

    def get_query(self, query):
        """Returns results of a "get" query
        
        Parameters
        ----------
        query : str
            query sent to database
        """

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

    def set_query(self, query, datas, many=True):
        """Returns results of a "get" query
        
        Parameters
        ----------
        query : str
            query sent to database
        
        datas : list or tuple
            datas to be injected in database
        """
        try:
            self.sql_connx
            cursor = self.sql_connx.cursor()
            print(Fore.GREEN + "Connection Established...")
            print(type(datas))
            print(datas)
            if many:
                cursor.executemany(query, datas)
            else:
                cursor.execute(query, datas)
                
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