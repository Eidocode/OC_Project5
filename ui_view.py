import tkinter as tk

from enum import Enum, auto
from colorama import init, deinit, Fore, Back, Style

import utils.constants as const

from controler import Controler

init(autoreset=True)


class State(Enum):
    IDLE = auto()
    SHOW_CATEGORIES = auto()
    SHOW_PRODUCTS = auto()
    SHOW_FAVORITES = auto()


class State_Machine:
    def __init__(self):
        self.__state = State.IDLE
    
    def set_state(self, state):
        self.__state = state
    
    def get_state(self):
        return self.__state


class Application(State_Machine):
    def __init__(self):
        super().__init__()  # inherits from class State_Machine
        self.window = tk.Tk()  # Main Window
        self.controler = Controler()  # Controller instance
        self.list_box = []  # List box uses for Categories and products
        self.selected_category = None  # The selected category in app
        self.lst_prod_in_cat = []
        self.selected_product = None  # The selected product in app
        self.lst_prod_in_fav = []
        self.selected_favorite = None
        self.btn_prod_is_active = False  # Return True if products button is active, else return False
        self.current_state = None  # Application current state
        
        self.frame_left = None  # Left frame that contains buttons menu
        self.frame_right_bottom = None  # Right bottom frame contains description
        self.init_application(self.window)


    def init_application(self, window):
        window.title('Pur Beurre Application')
        window.geometry('1024x768')
        window.resizable(width=0, height=0)
        
        self.update_state()
        self.build_left_frame(window)
        self.build_right_frame(window)

    def update_state(self):
        state = self.get_state()

        if state != self.current_state:
            if state == State.IDLE:
                print('### IDLE STATE ###')
            elif state == State.SHOW_CATEGORIES:
                print('### CATEGORIES STATE ###')
            elif state == State.SHOW_PRODUCTS:
                print('### PRODUCTS STATE ###')
                self.lst_prod_in_cat = []
            elif state == State.SHOW_FAVORITES:
                print('### FAVORITES STATE ###')
            
            self.current_state = state

    def build_left_frame(self, window):
        # Init elements
        self.frame_left = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.update_left_frame_widgets(self.frame_left)

    def update_left_frame_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
        if self.btn_prod_is_active:
            btn_state = tk.NORMAL
        else:
            btn_state = tk.DISABLED
        
        btn_categories = tk.Button(frame, text='Categories', command=lambda : self.show_categories(self.list_box),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_products = tk.Button(frame, text='Products', state=btn_state, command = lambda : self.show_products(self.list_box),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_favorites = tk.Button(frame, text='Favorites', command = lambda : self.show_favorites(self.list_box),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_exit = tk.Button(frame, text='Exit', command=quit,
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        
        # Placements
        btn_categories.pack(padx=10, pady=5)
        btn_products.pack(padx=10)
        btn_favorites.pack(padx=10, pady=5)
        btn_exit.pack(padx=10, pady=5, side='bottom')
        frame.pack(side='left', fill='y')
        
    def build_right_frame(self, window):
        frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=2)
        frame_description = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.frame_right_bottom = frame_description
        self.build_upper_frame(window, frame_lstbox, frame_description)
        
    def build_upper_frame(self, window, frame_up, frame_bot):
        for widget in frame_up.winfo_children():
            widget.destroy()
        # Init elements
        self.list_box = tk.Listbox(frame_up, height=15, width=110, selectbackground="#d0d0d0", selectforeground="#d00000", 
                                    selectmode="single", cursor="hand2")
        btn_select = tk.Button(frame_up, text='Select', command = lambda : self.show_selected_item(self.list_box, window, frame_bot),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        # Placements
        frame_up.pack(padx=5, pady=5, fill='x')
        self.list_box.pack(padx=10, pady=5)
        btn_select.pack(padx=10, pady=5, side='right')

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def build_bottom_frame(self, window, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        frame_details = frame
        
        if self.current_state == State.SHOW_CATEGORIES:
            category = self.selected_category

            text_name = str(category['name'])
            text_id = 'ID : ' + str(category['id'])
            text_jsonid = 'JSON ID : ' + str(category['json_id'])
            text_url = 'URL : ' + str(category['url'])
            # Init elements
            label_name = tk.Label(frame_details, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
            label_id = tk.Label(frame_details, text=text_id, relief='groove', width=100, height=2, font=(None, 9))
            label_json_id = tk.Label(frame_details, text=text_jsonid, relief='groove', width=100, height=2, font=(None, 9))
            label_url = tk.Label(frame_details, text=text_url, relief='groove', width=100, height=2, font=(None, 9))

            btn_add_cats = tk.Button(frame_details, text='Add 5 Cat.', command = lambda : self.add_5_items,
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
            # Placements
            frame_details.pack(padx=5, pady=5, expand=1, fill='both')
            label_name.pack(padx=20, pady=20)
            label_id.pack(padx=20, pady=10)
            label_json_id.pack(padx=20, pady=10)
            label_url.pack(padx=20, pady=10)
            btn_add_cats.pack(side="bottom", padx=10, pady=5)

        elif self.current_state == State.SHOW_PRODUCTS:
            product = self.selected_product

            text_name = str(product['name']) + ' de la marque ' + str(product['brand'])
            text_score = 'Nutriscore : ' + str(product['nutriscore']).upper()
            text_places = 'Ville(s) : ' + str(product['places'])
            text_stores = 'Magasin(s) : ' + str(product['stores'])
            text_barcode = 'Code barre : ' + str(product['barcode'])
            text_description = 'Description : ' + str(product['description'])
            # Init elements
            label_name = tk.Label(frame_details, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
            label_score = tk.Label(frame_details, text=text_score, relief='groove', width=100, height=2, font=(None, 9))
            label_places = tk.Label(frame_details, text=text_places, relief='groove', width=100, height=2, font=(None, 9))
            label_stores = tk.Label(frame_details, text=text_stores, relief='groove', width=100, height=2, font=(None, 9))
            label_barcode = tk.Label(frame_details, text=text_barcode, relief='groove', width=100, height=2, font=(None, 9))
            label_desciption = tk.Label(frame_details, text=text_description, relief='groove', width=100, height=2, font=(None, 9))

            btn_add_prods = tk.Button(frame_details, text='Add 5 Prod.', command = lambda : self.add_5_items() ,
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
            # Placements
            frame_details.pack(padx=5, pady=5, expand=1, fill='both')
            label_name.pack(padx=20, pady=20)
            label_score.pack(padx=20, pady=10)
            label_places.pack(padx=20, pady=10)
            label_stores.pack(padx=20, pady=10)
            label_barcode.pack(padx=20, pady=10)
            label_desciption.pack(padx=20, pady=10)
            btn_add_prods.pack(side="bottom", padx=10, pady=5)
        
        elif self.current_state == State.SHOW_FAVORITES:
            favorite = self.selected_favorite

            text_name = str(favorite['name']) + ' de la marque ' + str(favorite['brand'])
            text_score = 'Nutriscore : ' + str(favorite['nutriscore']).upper()
            text_places = 'Ville(s) : ' + str(favorite['places'])
            text_stores = 'Magasin(s) : ' + str(favorite['stores'])
            text_barcode = 'Code barre : ' + str(favorite['barcode'])
            text_description = 'Description : ' + str(favorite['description'])
            text_date = "Date d'ajout dans les favoris le : " + str(favorite['added_date'])
            # Init elements
            label_name = tk.Label(frame_details, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
            label_score = tk.Label(frame_details, text=text_score, relief='groove', width=100, height=2, font=(None, 9))
            label_places = tk.Label(frame_details, text=text_places, relief='groove', width=100, height=2, font=(None, 9))
            label_stores = tk.Label(frame_details, text=text_stores, relief='groove', width=100, height=2, font=(None, 9))
            label_barcode = tk.Label(frame_details, text=text_barcode, relief='groove', width=100, height=2, font=(None, 9))
            label_desciption = tk.Label(frame_details, text=text_description, relief='groove', width=100, height=2, font=(None, 9))
            label_date = tk.Label(frame_details, text=text_date, relief='groove', width=100, height=2, font=(None, 9))
            # Placements
            frame_details.pack(padx=5, pady=5, expand=1, fill='both')
            label_name.pack(padx=20, pady=20)
            label_score.pack(padx=20, pady=5)
            label_places.pack(padx=20, pady=5)
            label_stores.pack(padx=20, pady=5)
            label_barcode.pack(padx=20, pady=5)
            label_desciption.pack(padx=20, pady=5)
            label_date.pack(padx=20, pady=5)
            btn_add_prods.pack(side="bottom", padx=10, pady=5)


    
    def add_5_items(self):
        if self.current_state == State.SHOW_CATEGORIES:
            self.controler.set_categories(5)
            self.show_categories(self.list_box)
        elif self.current_state == State.SHOW_PRODUCTS:
            self.controler.set_products_in_category(5, self.selected_category['id'])
            self.show_products(self.list_box)

    def show_categories(self, list_box):
        self.clear_frame(self.frame_right_bottom)
        self.set_state(State.SHOW_CATEGORIES)
        self.update_state()
        list_box.delete(0, tk.END)
        list_categories = self.controler.get_all_categories_info()

        for category in list_categories:
            list_box.insert(tk.END, category[1])

    def show_products(self, list_box):
        self.clear_frame(self.frame_right_bottom)
        self.set_state(State.SHOW_PRODUCTS)
        self.update_state()
        list_box.delete(0, tk.END)
        list_products = self.controler.get_all_products_info(str(self.selected_category['id']))

        for product in list_products:
            self.lst_prod_in_cat.append(product)
            list_box.insert(tk.END, product[1])
    
    def show_favorites(self, list_box):
        self.clear_frame(self.frame_right_bottom)
        self.set_state(State.SHOW_FAVORITES)
        self.update_state()
        list_box.delete(0, tk.END)
        list_products = self.controler.get_all_favorites_info()

        for p in list_products:
            product = {}
            product['fav_id'] = p[0]
            product['prod_id'] = p[1]
            product['name'] = p[2]
            product['brand'] = p[3]
            product['description'] = p[4]
            product['nutriscore'] = p[5]
            product['places'] = p[6]
            product['stores'] = p[7]
            product['barcode'] = p[8]
            product['added_date'] = p[9]
            self.lst_prod_in_fav.append(product)
            list_box.insert(tk.END, p[2])


    def show_selected_item(self, list_box, window, frame_right_bottom):
        select = list_box.curselection()
        indice = int(select[0]+1)

        if self.current_state == State.SHOW_CATEGORIES:
            self.selected_category = self.controler.get_category_info(indice)
            print("Vous avez selectionné la catégorie " + self.selected_category['name'])
            self.btn_prod_is_active = True
            self.update_left_frame_widgets(self.frame_left)

        elif self.current_state == State.SHOW_PRODUCTS:
            product = self.lst_prod_in_cat[int(select[0])]
            product_id = int(product[0])
            self.selected_product = self.controler.get_product_info(product_id, str(self.selected_category['id']))
            print("Vous avez selectionné le produit " + self.selected_product['name'])
        
        elif self.current_state == State.SHOW_FAVORITES:
            self.selected_favorite = self.lst_prod_in_fav[0]
            print("#########")

            print(self.selected_favorite)
            print("Vous avez selectionné le favoris " + self.selected_favorite['name'])

        self.build_bottom_frame(window, frame_right_bottom)
    




new_app = Application()
new_app.window.mainloop()

deinit()