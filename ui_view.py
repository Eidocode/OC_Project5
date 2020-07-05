import tkinter as tk

from colorama import init, deinit

import utils.constants as const

from controler import Controler
from state import State_Machine, State


init(autoreset=True)


class UI_Manager(State_Machine):
    def __init__(self):
        # inherits from class State_Machine
        super().__init__()

        # Main and popup windows
        self.window = tk.Tk()
        self.popup = None

        # Controller instance
        self.controler = Controler()

        # List box uses for Categories and products
        self.list_box = []

        # Lists for products in categories and favorites
        self.lst_prod_in_cat = []
        self.lst_prod_in_fav = []

        # Return True if products button is active, else return False
        self.btn_prod_is_active = False

        # Left frame that contains buttons menu
        self.frame_menu = None
        self.frame_lstbox = None

        # Right bottom frame contains description
        self.frame_description = None

        # Selected category, product...
        self.selected_category = None
        self.selected_product = None
        self.selected_favorite = None
        self.selected_substitute = None

        self.init_application(self.window)

    def init_application(self, window):
        """Init. application"""

        # Main window configuration
        window.title('Pur Beurre Application')  # Title
        window.geometry('1024x768')  # Resolution
        window.resizable(width=0, height=0)  # Not resizable

        # Main Window MenuBar
        menubar = tk.Menu(window)
        window.config(menu=menubar)

        menu_edit = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=menu_edit)
        menu_edit.add_command(label="Add Products", command=lambda:
                                    self.controler.set_products(5))
        menu_edit.add_separator()
        menu_edit.add_command(label="Exit", command=quit)

        # Class methods
        self.display_state()  # Show current state
        self.draw_frame_menu(window)  # Left Frame Menu
        self.draw_content_frame(window)  # Right Frame Menu

    def clear_frame(self, frame):
        """Clear all widgets in specified frame

        Parameters
        ----------
        frame = Tkinter frame
            Frame where the widgets are located
        """
        for widget in frame.winfo_children():
            widget.destroy()

    def create_button(self, frm, txt, cmd, btn_state=tk.NORMAL):
        """Create a Tkinter button in a specified frame

        Parameters
        ----------
        frm = Tkinter frame
            Frame where the button will be
        txt = string
            Text to display in the button
        cmd = command
            Command to execute when clicked
        btn_state = Tkinter button state
            Button state, Normal by default
        """
        return tk.Button(frm, text=txt, command=cmd,
                         height=const.BUTTONS_HEIGHT,
                         width=const.BUTTONS_WIDTH, state=btn_state)

    def draw_frame_menu(self, window):
        """Draw left menu frame"""

        # Init elements
        self.frame_menu = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.update_menu_widgets(self.frame_menu)

    def update_menu_widgets(self, frame):
        """Update left menu widgets"""

        self.clear_frame(frame)
        if self.btn_prod_is_active:
            btn_state = tk.NORMAL
        else:
            btn_state = tk.DISABLED
        btn_categories = self.create_button(frame, 'Categories', lambda:
                                            self.show_elements('Categories'))
        btn_products = self.create_button(frame, 'Products', lambda:
                                          self.show_elements('Products'),
                                          btn_state)
        btn_favorites = self.create_button(frame, 'Favorites', lambda:
                                           self.show_elements('Favorites'))
        btn_exit = self.create_button(frame, 'Exit', quit)
        # Placements
        btn_categories.pack(padx=10, pady=5)
        btn_products.pack(padx=10)
        btn_favorites.pack(padx=10, pady=5)
        btn_exit.pack(padx=10, pady=5, side='bottom')
        frame.pack(side='left', fill='y')

    def draw_content_frame(self, window):
        """Update left menu widgets"""

        self.frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.frame_description = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.update_lstbox_widgets(self.window, self.frame_lstbox,
                                   self.frame_description)

    def update_lstbox_widgets(self, window, frame_up, frame_bot):
        """Update listbox widgets"""

        self.clear_frame(frame_up)
        # Init elements
        self.list_box = tk.Listbox(frame_up, height=15, width=110,
                                   selectbackground="#d0d0d0",
                                   selectforeground="#d00000",
                                   selectmode="single", cursor="hand2")
        btn_add_cats = self.create_button(frame_up, 'Add 5 Cat', lambda:
                                          self.add_5_items())
        btn_add_prods = self.create_button(frame_up, 'Add 5 Prod.', lambda:
                                           self.add_5_items())
        btn_select = self.create_button(frame_up, 'Select', lambda:
                                        self.show_selected_item(self.list_box))
        # Placements
        frame_up.pack(padx=5, pady=5, fill='x')
        self.list_box.pack(padx=10, pady=5)
        btn_select.pack(padx=10, pady=5, side='right')
        if self.get_state() == State.SHOW_CATEGORIES:
            btn_add_cats.pack(padx=10, pady=5, side='left')
        elif self.get_state() == State.SHOW_PRODUCTS:
            btn_add_prods.pack(padx=10, pady=5, side='left')

    def draw_description_frame(self):
        """Draw bottom right frame"""

        self.clear_frame(self.frame_description)
        if self.get_state() == State.SHOW_CATEGORIES:
            self.display_category_info()
        elif self.get_state() == State.SHOW_PRODUCTS:
            self.display_products_info()
        elif self.get_state() == State.SHOW_FAVORITES:
            self.display_products_info()

    def display_category_info(self):
        """Display information about categories"""

        category = self.selected_category

        text_name = str(category['name'])
        text_id = 'ID : ' + str(category['id'])
        text_jsonid = 'JSON ID : ' + str(category['json_id'])
        text_url = 'URL : ' + str(category['url'])
        # Init elements
        label_name = tk.Label(self.frame_description, text=text_name,
                              relief='raised', width=100, height=2,
                              font=(None, 18, 'bold'))
        label_id = tk.Label(self.frame_description, text=text_id,
                            relief='groove', width=100, height=2,
                            font=(None, 9))
        label_json_id = tk.Label(self.frame_description, text=text_jsonid,
                                 relief='groove', width=100, height=2,
                                 font=(None, 9))
        label_url = tk.Label(self.frame_description, text=text_url,
                             relief='groove', width=100, height=2,
                             font=(None, 9))
        # Placements
        self.frame_description.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_id.pack(padx=20, pady=10)
        label_json_id.pack(padx=20, pady=10)
        label_url.pack(padx=20, pady=10)

    def display_products_info(self, substitute=False):
        """Display information about products"""

        product = None
        frame = self.frame_description
        if self.get_state() == State.SHOW_PRODUCTS:
            if substitute:
                product = self.selected_substitute
                frame = self.popup
            else:
                product = self.selected_product
        elif self.get_state() == State.SHOW_FAVORITES:
            product = self.selected_favorite

        text_name = "{} de la marque {}".format(product['name'],
                                                product['brand'])
        text_score = 'Nutriscore : ' + str(product['nutriscore']).upper()
        text_places = 'Ville(s) : ' + str(product['places'])
        text_stores = 'Magasin(s) : ' + str(product['stores'])
        text_barcode = 'Code barre : ' + str(product['barcode'])
        text_description = 'Description : ' + str(product['description'])
        # Init elements
        label_name = tk.Label(frame, text=text_name, relief='raised',
                              width=100, height=2, font=(None, 18, 'bold'))
        label_score = tk.Label(frame, text=text_score, relief='groove',
                               width=100, height=2, font=(None, 9))
        label_places = tk.Label(frame, text=text_places, relief='groove',
                                width=100, height=2, font=(None, 9))
        label_stores = tk.Label(frame, text=text_stores, relief='groove',
                                width=100, height=2, font=(None, 9))
        label_barcode = tk.Label(frame, text=text_barcode, relief='groove',
                                 width=100, height=2, font=(None, 9))
        label_description = tk.Label(frame, text=text_description,
                                     relief='groove', width=100, height=2,
                                     font=(None, 9))
        # Placements
        if not substitute:
            frame.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_score.pack(padx=20, pady=10)
        label_places.pack(padx=20, pady=10)
        label_stores.pack(padx=20, pady=10)
        label_barcode.pack(padx=20, pady=10)
        label_description.pack(padx=20, pady=10)

        if self.get_state() == State.SHOW_PRODUCTS:
            if substitute:
                btn_add_fav = self.create_button(frame,
                                                 'Add to Fav.', lambda:
                                                 self.add_to_fav(
                                                    self.selected_substitute))
                btn_close = self.create_button(frame, 'Close', frame.destroy)
                btn_close.pack(side="bottom", padx=10, pady=5)
                btn_add_fav.pack(side="bottom", padx=10, pady=5)
            else:
                btn_add_fav = self.create_button(frame, 'Add to Fav.', lambda:
                                                 self.add_to_fav(
                                                    self.selected_product))
                btn_get_sub = self.create_button(frame, 'Get Sub.', lambda:
                                                 self.show_sub())
                btn_add_fav.pack(side="right", padx=10, pady=5)
                btn_get_sub.pack(side='left', padx=10, pady=5)
        elif self.get_state() == State.SHOW_FAVORITES:
            text_date = """Date d'ajout dans les favoris le : {}""".format(
                                                    str(product['added_date']))
            label_date = tk.Label(frame, text=text_date, relief='groove',
                                  width=100, height=2, font=(None, 9))
            label_date.pack(padx=20, pady=5)

    def show_elements(self, new_state):
        """Display elements in listbox defined by the state specified in
        parameter

        Parameters
        ----------
        new_state = String
            The state to target to show categories, products or favorites
            elements
        """

        self.clear_frame(self.frame_description)
        self.list_box.delete(0, tk.END)
        if new_state == 'Categories':
            self.set_state(State.SHOW_CATEGORIES)
            list_categories = self.controler.get_all_categories_info()
            self.update_lstbox_widgets(self.window, self.frame_lstbox,
                                       self.frame_description)
            for category in list_categories:
                self.list_box.insert(tk.END, category[1])
        elif new_state == 'Products':
            self.set_state(State.SHOW_PRODUCTS)
            self.lst_prod_in_cat = []
            list_products = self.controler.get_all_products_info(
                                            str(self.selected_category['id']))
            self.update_lstbox_widgets(self.window, self.frame_lstbox,
                                       self.frame_description)
            for product in list_products:
                self.lst_prod_in_cat.append(product)
                self.list_box.insert(tk.END, product[1])
        elif new_state == 'Favorites':
            self.set_state(State.SHOW_FAVORITES)
            self.lst_prod_in_fav = []
            list_favorites = self.controler.get_all_favorites_info()
            self.update_lstbox_widgets(self.window, self.frame_lstbox,
                                       self.frame_description)
            for product in list_favorites:
                self.lst_prod_in_fav.append(product)
                self.list_box.insert(tk.END, product['name'])
        self.display_state()

    def show_selected_item(self, list_box):
        """Show selected item (category, product, favorite) information"""

        select = list_box.curselection()
        indice = int(select[0])
        indice_db = indice + 1
        if self.get_state() == State.SHOW_CATEGORIES:
            self.selected_category = self.controler.get_category_info(
                                                                indice_db)
            print("Vous avez selectionné la catégorie " +
                  self.selected_category['name'])
            self.btn_prod_is_active = True
            self.update_menu_widgets(self.frame_menu)
        elif self.get_state() == State.SHOW_PRODUCTS:
            product = self.lst_prod_in_cat[indice]
            product_id = int(product[0])
            self.selected_product = self.controler.get_product_info(
                                product_id, str(self.selected_category['id']))
            print("Vous avez selectionné le produit " +
                  self.selected_product['name'])
        elif self.get_state() == State.SHOW_FAVORITES:
            self.selected_favorite = self.lst_prod_in_fav[indice]
            print("Vous avez selectionné le favoris " +
                  self.selected_favorite['name'])
        self.draw_description_frame()

    def display_state(self):
        """Display current state"""

        state = self.get_state()
        if state == State.IDLE:
            print('### IDLE STATE ###')
        elif state == State.SHOW_CATEGORIES:
            print('### CATEGORIES STATE ###')
        elif state == State.SHOW_PRODUCTS:
            print('### PRODUCTS STATE ###')
        elif state == State.SHOW_FAVORITES:
            print('### FAVORITES STATE ###')

    def add_5_items(self):
        """Add 5 items (categories or products) to database, depending of the
        current state"""

        if self.get_state() == State.SHOW_CATEGORIES:
            self.controler.set_categories(5)
            self.show_elements('Categories')
        elif self.get_state() == State.SHOW_PRODUCTS:
            self.controler.set_products_in_category(
                                                5,
                                                self.selected_category['id'])
            self.show_elements('Products')

    def add_to_fav(self, product):
        """Add product specified in parameters to favorites"""
        self.controler.set_product_to_fav(product)

    def show_sub(self):
        """Show substitute product"""

        self.popup = tk.Tk()  # Substitute popup window
        self.popup.wm_title("Product Substitute")
        self.popup.geometry('640x480')
        self.popup.resizable(width=0, height=0)

        product = self.controler.get_sub_product(self.selected_product,
                                                 self.lst_prod_in_cat)
        self.selected_substitute = product

        label = tk.Label(self.popup, text=self.display_products_info(True))
        label.pack(side="top", fill="x", pady=10)
        self.popup.mainloop()


# GUI instance
new_app = UI_Manager()
new_app.window.mainloop()

deinit()
