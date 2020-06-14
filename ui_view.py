import tkinter as tk

from colorama import init, deinit, Fore, Back, Style

import utils.constants as const

from controler import Controler
from state import State_Machine, State


init(autoreset=True)

class UI_Manager(State_Machine):
    def __init__(self):
        super().__init__()  # inherits from class State_Machine
        self.window = tk.Tk()  # Main Window
        self.controler = Controler()  # Controller instance

        self.list_box = []  # List box uses for Categories and products
        self.lst_prod_in_cat = []
        self.lst_prod_in_fav = []

        self.btn_prod_is_active = False  # Return True if products button is active, else return False

        self.frame_menu = None  # Left frame that contains buttons menu
        self.frame_lstbox = None
        self.frame_description = None  # Right bottom frame contains description

        self.current_state = None

        self.selected_category = None  # The selected category in app
        self.selected_product = None  # The selected product in app
        self.selected_favorite = None

        self.init_application(self.window)

    def init_application(self, window):
        window.title('Pur Beurre Application')
        window.geometry('1024x768')
        window.resizable(width=0, height=0)
        
        self.display_state()
        self.draw_frame_menu(window)
        self.draw_content_frame(window)
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def create_button(self, frm, txt, cmd, btn_state=tk.NORMAL):
        return tk.Button(frm, text=txt, command=cmd, height=const.BUTTONS_HEIGHT, 
                            width=const.BUTTONS_WIDTH, state=btn_state)

    def draw_frame_menu(self, window):
        # Init elements
        self.frame_menu = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.update_menu_widgets(self.frame_menu)
    
    def update_menu_widgets(self, frame):
        self.clear_frame(frame)
        
        if self.btn_prod_is_active:
            btn_state = tk.NORMAL
        else:
            btn_state = tk.DISABLED
        
        btn_categories = self.create_button(frame, 'Categories', lambda:self.show_elements('Categories'))
        btn_products = self.create_button(frame, 'Products', lambda:self.show_elements('Products'), btn_state)
        btn_favorites = self.create_button(frame, 'Favorites', lambda:self.show_elements('Favorites'))
        btn_exit = self.create_button(frame, 'Exit', quit)
        
        # Placements
        btn_categories.pack(padx=10, pady=5)
        btn_products.pack(padx=10)
        btn_favorites.pack(padx=10, pady=5)
        btn_exit.pack(padx=10, pady=5, side='bottom')
        frame.pack(side='left', fill='y')
    
    def draw_content_frame(self, window):
        frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.frame_lstbox = frame_lstbox
        frame_description = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.frame_description = frame_description
        self.update_lstbox_widgets(self.window, self.frame_lstbox, self.frame_description)

    def update_lstbox_widgets(self, window, frame_up, frame_bot):
        self.clear_frame(frame_up)
        # Init elements
        self.list_box = tk.Listbox(frame_up, height=15, width=110, selectbackground="#d0d0d0", selectforeground="#d00000", 
                                    selectmode="single", cursor="hand2")
        btn_add_cats = tk.Button(frame_up, text='Add 5 Cat.', command = lambda : self.add_5_items(),
                                height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_add_prods = tk.Button(frame_up, text='Add 5 Prod.', command = lambda : self.add_5_items(),
                                height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_select = self.create_button(frame_up, 'Select', lambda:self.show_selected_item(self.list_box))
        # Placements
        frame_up.pack(padx=5, pady=5, fill='x')
        self.list_box.pack(padx=10, pady=5)
        btn_select.pack(padx=10, pady=5, side='right')
        print("HEEYYY " + str(self.get_state()))
        if self.get_state() == State.SHOW_CATEGORIES:
            btn_add_cats.pack(padx=10, pady=5, side='left')
        elif self.get_state() == State.SHOW_PRODUCTS:
            btn_add_prods.pack(padx=10, pady=5, side='left')
            
    def draw_description_frame(self):
        self.clear_frame(self.frame_description)

        if self.get_state() == State.SHOW_CATEGORIES:
            category = self.selected_category
            print("DRAW CONTENT CAT")
            self.display_category_info()

        elif self.get_state() == State.SHOW_PRODUCTS:
            product = self.selected_product
            print("DRAW CONTENT PROD")
            self.display_product_info()

        elif self.get_state() == State.SHOW_FAVORITES:
            favorite = self.selected_favorite
            print("DRAW CONTENT FAV")
            self.display_favorite_info()
    
    def display_category_info(self):
        category = self.selected_category

        text_name = str(category['name'])
        text_id = 'ID : ' + str(category['id'])
        text_jsonid = 'JSON ID : ' + str(category['json_id'])
        text_url = 'URL : ' + str(category['url'])
        # Init elements
        label_name = tk.Label(self.frame_description, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
        label_id = tk.Label(self.frame_description, text=text_id, relief='groove', width=100, height=2, font=(None, 9))
        label_json_id = tk.Label(self.frame_description, text=text_jsonid, relief='groove', width=100, height=2, font=(None, 9))
        label_url = tk.Label(self.frame_description, text=text_url, relief='groove', width=100, height=2, font=(None, 9))
        # Placements
        self.frame_description.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_id.pack(padx=20, pady=10)
        label_json_id.pack(padx=20, pady=10)
        label_url.pack(padx=20, pady=10)
    
    def display_product_info(self):
        product = self.selected_product

        text_name = str(product['name']) + ' de la marque ' + str(product['brand'])
        text_score = 'Nutriscore : ' + str(product['nutriscore']).upper()
        text_places = 'Ville(s) : ' + str(product['places'])
        text_stores = 'Magasin(s) : ' + str(product['stores'])
        text_barcode = 'Code barre : ' + str(product['barcode'])
        text_description = 'Description : ' + str(product['description'])
        # Init elements
        label_name = tk.Label(self.frame_description, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
        label_score = tk.Label(self.frame_description, text=text_score, relief='groove', width=100, height=2, font=(None, 9))
        label_places = tk.Label(self.frame_description, text=text_places, relief='groove', width=100, height=2, font=(None, 9))
        label_stores = tk.Label(self.frame_description, text=text_stores, relief='groove', width=100, height=2, font=(None, 9))
        label_barcode = tk.Label(self.frame_description, text=text_barcode, relief='groove', width=100, height=2, font=(None, 9))
        label_desciption = tk.Label(self.frame_description, text=text_description, relief='groove', width=100, height=2, font=(None, 9))

        btn_add_fav = tk.Button(self.frame_description, text='Add to Fav.', command = lambda : self.add_to_fav(),
                                height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        # Placements
        self.frame_description.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_score.pack(padx=20, pady=10)
        label_places.pack(padx=20, pady=10)
        label_stores.pack(padx=20, pady=10)
        label_barcode.pack(padx=20, pady=10)
        label_desciption.pack(padx=20, pady=10)
        btn_add_fav.pack(side="right", padx=10, pady=5)
    
    def display_favorite_info(self):
        favorite = self.selected_favorite

        text_name = str(favorite['name']) + ' de la marque ' + str(favorite['brand'])
        text_score = 'Nutriscore : ' + str(favorite['nutriscore']).upper()
        text_places = 'Ville(s) : ' + str(favorite['places'])
        text_stores = 'Magasin(s) : ' + str(favorite['stores'])
        text_barcode = 'Code barre : ' + str(favorite['barcode'])
        text_description = 'Description : ' + str(favorite['description'])
        text_date = "Date d'ajout dans les favoris le : " + str(favorite['added_date'])
        # Init elements
        label_name = tk.Label(self.frame_description, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
        label_score = tk.Label(self.frame_description, text=text_score, relief='groove', width=100, height=2, font=(None, 9))
        label_places = tk.Label(self.frame_description, text=text_places, relief='groove', width=100, height=2, font=(None, 9))
        label_stores = tk.Label(self.frame_description, text=text_stores, relief='groove', width=100, height=2, font=(None, 9))
        label_barcode = tk.Label(self.frame_description, text=text_barcode, relief='groove', width=100, height=2, font=(None, 9))
        label_desciption = tk.Label(self.frame_description, text=text_description, relief='groove', width=100, height=2, font=(None, 9))
        label_date = tk.Label(self.frame_description, text=text_date, relief='groove', width=100, height=2, font=(None, 9))
        # Placements
        self.frame_description.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_score.pack(padx=20, pady=5)
        label_places.pack(padx=20, pady=5)
        label_stores.pack(padx=20, pady=5)
        label_barcode.pack(padx=20, pady=5)
        label_desciption.pack(padx=20, pady=5)
        label_date.pack(padx=20, pady=5)

    def show_elements(self, new_state):
        print("CLIQUE CATEGORY")
        self.clear_frame(self.frame_description)
        
        self.list_box.delete(0, tk.END)

        if new_state == 'Categories':
            self.set_state(State.SHOW_CATEGORIES)
            list_categories = self.controler.get_all_categories_info()
            self.update_lstbox_widgets(self.window, self.frame_lstbox, self.frame_description)
            for category in list_categories:
                self.list_box.insert(tk.END, category[1])

        elif new_state == 'Products':
            self.set_state(State.SHOW_PRODUCTS)
            self.lst_prod_in_cat = []
            list_products = self.controler.get_all_products_info(str(self.selected_category['id']))
            self.update_lstbox_widgets(self.window, self.frame_lstbox, self.frame_description)
            for product in list_products:
                self.lst_prod_in_cat.append(product)
                self.list_box.insert(tk.END, product[1])

        elif new_state == 'Favorites':
            self.set_state(State.SHOW_FAVORITES)
            list_favorites = self.controler.get_all_favorites_info()

            for product in list_favorites:
                self.lst_prod_in_fav.append(product)
                self.list_box.insert(tk.END, product['name'])

        self.display_state()
        
    def show_selected_item(self, list_box):
        select = list_box.curselection()
        indice = int(select[0])
        indice_db = indice + 1

        if self.get_state() == State.SHOW_CATEGORIES:
            self.selected_category = self.controler.get_category_info(indice_db)
            print("Vous avez selectionné la catégorie " + self.selected_category['name'])
            self.btn_prod_is_active = True
            self.update_menu_widgets(self.frame_menu)
            
        elif self.get_state() == State.SHOW_PRODUCTS:
            product = self.lst_prod_in_cat[indice]
            product_id = int(product[0])
            self.selected_product = self.controler.get_product_info(product_id, str(self.selected_category['id']))
            print("Vous avez selectionné le produit " + self.selected_product['name'])
        
        elif self.get_state() == State.SHOW_FAVORITES:
            self.selected_favorite = self.lst_prod_in_fav[indice]
            print("Vous avez selectionné le favoris " + self.selected_favorite['name'])

        self.draw_description_frame()

    def display_state(self):
        state = self.get_state()

        if state != self.current_state:
            if state == State.IDLE:
                print('### IDLE STATE ###')
            elif state == State.SHOW_CATEGORIES:
                print('### CATEGORIES STATE ###')
            elif state == State.SHOW_PRODUCTS:
                print('### PRODUCTS STATE ###')
            elif state == State.SHOW_FAVORITES:
                print('### FAVORITES STATE ###')

            self.current_state = state
    
    def add_5_items(self):
        if self.get_state() == State.SHOW_CATEGORIES:
            self.controler.set_categories(5)
            self.show_elements('Categories')
        elif self.get_state() == State.SHOW_PRODUCTS:
            self.controler.set_products_in_category(5, self.selected_category['id'])
            self.show_elements('Products')
    
    def add_to_fav(self):
        print(self.selected_product)
        self.controler.set_product_to_fav(self.selected_product)


new_app = UI_Manager()

new_app.window.mainloop()
new_app.update_lstbox_widgets(new_app.window, new_app.frame_lstbox, new_app.frame_description)

deinit()