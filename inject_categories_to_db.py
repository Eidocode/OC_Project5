from colorama import init, deinit, Fore, Back, Style

import constants as const

from database_manager import DatabaseManager
from api_handler_categories import ApiHandlerCategories


init(autoreset=True)


class Category:
    def __init__(self, nb_cat):
        self.nb_cat = nb_cat
        self.categories_in_db = self.get_all_from_db()
        
        self.list_json_id = []
        for cat in self.categories_in_db:
            self.list_json_id.append(cat[2])

    def get_from_api(self):
        list_categories = []
        api_datas = ApiHandlerCategories(self.nb_cat)

        for category in api_datas.categories:
            if not self.exist_in_db(category['id']):
                datas = (category['name'], category['id'], category['url'])
                list_categories.append(datas)
            else :
                print(Fore.YELLOW + category['name'] + " already in database...")
        
        return list_categories
    
    def set_to_db(self):
        db_manager = DatabaseManager()
        datas_to_insert = self.get_from_api()

        insert_query = """INSERT INTO Categories (name, json_id, url)
                            VALUES
                            (%s, %s, %s)"""
        
        db_manager.set_query(insert_query, datas_to_insert)
        db_manager._destroy()
    
    def get_all_from_db(self):
        db_manager = DatabaseManager()
        list_categories = []

        query_get_categories = """SELECT * FROM Categories"""
        
        list_categories = db_manager.get_query(query_get_categories)
        return list_categories

    def exist_in_db(self, json_id):
        if json_id in self.list_json_id:
            return True
        else:
            self.list_json_id.append(json_id)

        return False

    def _destroy(self):
        print(Fore.LIGHTYELLOW_EX + "InjectCategories instance has been deleted")
        del self


test = Category(const.NB_CATEGORIES_TO_GET)
test.set_to_db()
test._destroy()


deinit()




