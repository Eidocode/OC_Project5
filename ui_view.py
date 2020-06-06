import tkinter as tk

from colorama import init, deinit, Fore, Back, Style

import utils.constants as const

from controler import Controler

init(autoreset=True)

class Application:
    def __init__(self):
        self.window = tk.Tk()  # Main Window
        self.controler = Controler()  # Controller instance
        self.list_box = []  # List box uses for Categories and products
        self.selected_category = None  # The selected category in app
        self.selected_product = None  # The selected product in app
        self.btn_prod_is_active = False  # Return True if products button is active, else return False
        self.frame_left= None  # Left Frame that contains buttons menu
        # self.frame_right_upper = None
        # self.frame_right_bottom = None
        self.init_application(self.window)


    def init_application(self, window):
        window.title("Pur Beurre Application")
        window.geometry('800x600')
        window.resizable(width=0, height=0)

        self.build_frame_left(window)
        self.build_main_frame(window)

    def update_left_frame_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
        if self.btn_prod_is_active:
            btn_state = tk.NORMAL
        else:
            btn_state = tk.DISABLED
        
        btn_categories = tk.Button(frame, text='Categories', command=lambda : self.get_categories(self.list_box),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_products = tk.Button(frame, text='Products', state=btn_state, command = lambda : self.get_products(self.list_box),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        btn_exit = tk.Button(frame, text='Exit', command=quit,
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
        
        # Placements
        btn_categories.pack(padx=10, pady=5)
        btn_products.pack(padx=10)
        btn_exit.pack(padx=10, pady=5, side='bottom')
        frame.pack(side='left', fill='y')

    def build_frame_left(self, window):
        # Init elements
        self.frame_left = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.update_left_frame_widgets(self.frame_left)
    
    def build_main_frame(self, window):
        frame = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.build_upper_frame(window, frame)
        
    def build_upper_frame(self, window, frame):
        # Init elements
        frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.list_box = tk.Listbox(frame_lstbox, height=15, width=110, selectbackground="#d0d0d0", selectforeground="#d00000", 
                                    selectmode="single", cursor="hand2")
        btn_select = tk.Button(frame_lstbox, text='Select', command = lambda : self.get_selected_category(self.list_box, window, frame),
                                    height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)

        # Placements
        frame_lstbox.pack(padx=5, pady=5, fill='x')
        self.list_box.pack(padx=10, pady=5)
        btn_select.pack(padx=10, pady=5, side='right')
    
    def build_bottom_frame(self, window, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        text_name = str(self.selected_category['name'])
        text_id = 'ID : ' + str(self.selected_category['id'])
        text_jsonid = 'JSON ID : ' + str(self.selected_category['json_id'])
        text_url = 'URL : ' + str(self.selected_category['url'])

        # Init elements
        frame_details = frame
        label_name = tk.Label(frame_details, text=text_name, relief='raised', width=100, height=2, font=(None, 18, 'bold'))
        label_id = tk.Label(frame_details, text=text_id, relief='groove', width=100, height=2, font=(None, 9))
        label_json_id = tk.Label(frame_details, text=text_jsonid, relief='groove', width=100, height=2, font=(None, 9))
        label_url = tk.Label(frame_details, text=text_url, relief='groove', width=100, height=2, font=(None, 9))

        # Placements
        frame_details.pack(padx=5, pady=5, expand=1, fill='both')
        label_name.pack(padx=20, pady=20)
        label_id.pack(padx=20, pady=10)
        label_json_id.pack(padx=20, pady=10)
        label_url.pack(padx=20, pady=10)
    
    def get_categories(self, list_box):
        list_box.delete(0, tk.END)
        list_categories = self.controler.get_all_categories_info()

        for category in list_categories:
            list_box.insert(tk.END, category[1])
    
    def get_selected_category(self, list_box, window, frame_right_bottom):
        select = list_box.curselection()
        indice = int(select[0]+1)

        self.selected_category = self.controler.get_category_info(indice)
        print("Vous avez selectionné la catégorie " + self.selected_category['name'])
        
        self.build_bottom_frame(window, frame_right_bottom)
        self.btn_prod_is_active = True
        self.update_left_frame_widgets(self.frame_left)

    def get_products(self, list_box):
        list_box.delete(0, tk.END)
        list_products = self.controler.get_all_products_info(str(self.selected_category['id']))

        for product in list_products:
            list_box.insert(tk.END, product[1])
    
    def get_selected_product(self, list_box, window, frame_right_bottom):
        select = list_box.curselection()
        indice = int(select[0]+1)

        self.selected_product = self.controler.get_product_info(indice, str(self.selected_category['id']))
        print("Vous avez selectionné le produit " + self.selected_product['name'])

        self.build_bottom_frame(window, frame_right_bottom)
    




new_app = Application()
new_app.window.mainloop()

deinit()