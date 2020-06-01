from colorama import init, deinit, Fore, Back, Style

from database.database_manager import DatabaseManager
from api.api_handler_categories import ApiHandlerCategories


init(autoreset=True)

class Category:
    """
    Class used to manipulate categories

    ...

    Attributes
    ----------
    categories_in_db : list
        List which contains all categories present in database
    
    list_json_id : list
        List which contains values of json_id field in database
    
    Methods
    -------
    _get_from_api(nb_cat)
        Analyze categories returns by ApiHandlerCategories Class.
    
    set_to_db(datas_to_insert)
        Set categories to database
    
    get_all_from_db
        Returns a list of all categories present in database
    
    exist_in_db
        Check if json_id exists in database and returns True or False
    """
    
    def __init__(self):
        self.categories_in_db = self.get_all_from_db()
        
        self.list_json_id = []
        for cat in self.categories_in_db:
            self.list_json_id.append(cat[2])

    def _get_from_api(self, nb_cat):
        """Analyze categories returns by ApiHandlerCategories Class. For each 
        category, check if it already exists in list or database. Returns a 
        list without any duplicate category.

        Parameters
        ----------
        nb_cat : int
            Number of categories for instantiation of ApiHandlerCategories
        """

        list_categories = []
        api_datas = ApiHandlerCategories(nb_cat)

        for category in api_datas.categories:
            if not self.exist_in_db(category['id']):
                datas = (category['name'], category['id'], category['url'])
                list_categories.append(datas)
                print(category['name'] + " added to database...")
            else :
                print(Fore.YELLOW + category['name'] + " already in list or database...")
        
        return list_categories
    
    def set_to_db(self, datas_to_insert):
        """Set categories to database with DatabaseManager Class

        Parameters
        ----------
        datas_to_insert : tuple
            tuple of data to insert in database
        """

        db_manager = DatabaseManager()

        insert_query = """INSERT INTO Categories (name, json_id, url)
                            VALUES
                            (%s, %s, %s)"""
        
        db_manager.set_query(insert_query, datas_to_insert)
        db_manager._destroy()
    
    def get_all_from_db(self):
        """Returns a list of all categories present in database"""
        
        db_manager = DatabaseManager()
        list_categories = []
        query_get_categories = """SELECT * FROM Categories"""
        
        list_categories = db_manager.get_query(query_get_categories)
        db_manager._destroy()

        return list_categories

    def exist_in_db(self, json_id):
        """Check if json_id exists in database and returns True or False
        If json_id not present in list_json_id, add it to prevent duplicate 
        category.

        Parameters
        ----------
        json_id = string
            Contains json_id category value
        """
        if json_id in self.list_json_id:
            return True
        else:
            self.list_json_id.append(json_id)

        return False
    
    def get_one_from_db(self, id_category):
        db_manager = DatabaseManager()
        category_info = []
        
        query_get_category = """SELECT * FROM Categories WHERE id = """ + id_category
        
        category_info = db_manager.get_query(query_get_category)
        db_manager._destroy()

        return category_info


    def _destroy(self):
        print(Fore.LIGHTYELLOW_EX + "Instance Category has been deleted")
        del self


deinit()
