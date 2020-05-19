import tkinter as tk
import mysql.connector

from colorama import init, deinit, Fore, Back, Style

import constants as const
from tkinter import ttk

window = tk.Tk()

window.geometry('800x800')
window.resizable(width=0, height=0)

label = tk.Label(window, text="Application Pur Beurre", font="Arial 22 bold")
label.pack()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
    def create_widgets(self):
        






def get_categories(self):
    try:
        connx = mysql.connector.connect(
            host = const.SRV_IP,
            user = const.USER_ID,
            password = const.USER_PWD,
            database = const.DB_NAME
        )

        cursor = connx.cursor()
        print(Fore.GREEN + "Connection Established...")
        
        cursor.execute(const.QUERY_GET_CATEGORIES)
        result = cursor.fetchall()
        cursor.close()

    except mysql.connector.Error as error:
        print(Fore.RED + "Failed to insert record into table {}".format(error))

    finally:
        if (connx.is_connected()):
            connx.close()
            print("Mysql connection closed...")

    return result



list_categories = get_categories()

list_cat_name = []
for cat in list_categories:
    list_cat_name.append(cat[1])


labelChoix = tk.Label(window, text = "Veuillez choisir une catégorie !", font="Arial 14")
labelChoix.pack()

listeCombo = ttk.Combobox(window, values=list_cat_name)
listeCombo.current(0)
listeCombo.config(width=30)
print(listeCombo.get())
listeCombo.pack()



button = tk.Button(window, text=" Valider ", command=window.quit)
button.pack()

window.mainloop()