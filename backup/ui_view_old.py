import tkinter as tk

from tkinter.filedialog import askopenfilename, asksaveasfilename
from colorama import init, deinit, Fore, Back, Style

import utils.constants as const

from controler import Controler


init(autoreset=True)

controler = Controler()

def list_categories(list_box):
    list_box.delete(0, tk.END)
    categories = controler.get_all_categories_info()

    for category in categories:
        list_box.insert(tk.END, category[1])

def get_selected(list_box):
    select = list_box.curselection()
    indice = int(select[0]+1)

    category = controler.get_category_info(indice)

    print("Vous avez selectionné la catégorie " + category['name'])

    

# Main Window
window = tk.Tk()
window.title("Pur Beurre Application")
window.geometry('800x600')
window.resizable(width=0, height=0)
# window.rowconfigure(0, minsize=800, weight=1)
# window.columnconfigure(1, minsize=800, weight=1)

# Listboxes Frames
frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=1)
lst_box = tk.Listbox(frame_lstbox, height=15, width=110, selectbackground="#d0d0d0", selectforeground="#d00000", 
                        selectmode="single", cursor="hand2")
btn_select = tk.Button(frame_lstbox, text='Select', command=lambda : get_selected(lst_box), height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)

label_catg = tk.Label(text="Vous avez selectionné la catégorie : " )

# Button Frames
frame_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_categories = tk.Button(frame_buttons, text='Categories', command=lambda : list_categories(lst_box), height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
btn_save = tk.Button(frame_buttons, text='Products', height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)
btn_exit = tk.Button(frame_buttons, text='Exit', height=const.BUTTONS_HEIGHT, width=const.BUTTONS_WIDTH)


# Placements
    # Button column
btn_categories.pack(padx=10, pady=5)
btn_save.pack(padx=10)
btn_exit.pack(padx=10, pady=5, side='bottom')
frame_buttons.pack(side='left', fill='y')
    
    # Listbox frame
frame_lstbox.pack(padx=5, pady=5, fill='x')
lst_box.pack(padx=10, pady=5)
btn_select.pack(padx=10, pady=5, side='right')

deinit()
window.mainloop()
