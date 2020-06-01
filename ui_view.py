import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from controler import Controler


controler = Controler()

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

def list_categories(list_box):
    list_box.delete(0, tk.END)
    categories = controler.get_all_categories_info()

    for category in categories:
        list_box.insert(tk.END, category[1])
    
    

# Main Window
window = tk.Tk()
window.title("Pur Beurre Application")
window.geometry('800x800')
window.resizable(width=0, height=0)
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

# Listboxes Frames
frame_lstbox = tk.Frame(window, relief=tk.RAISED, bd=1)

# Listboxes
lst_box = tk.Listbox(frame_lstbox, selectbackground="#d0d0d0", selectforeground="#d00000", 
                        selectmode="single", cursor="hand2")


# Button Frames
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

# Buttons
btn_categories = tk.Button(fr_buttons, text="Categories", command=lambda : list_categories(lst_box))
btn_save = tk.Button(fr_buttons, text="Products", command=save_file)
btn_select = tk.Button(frame_lstbox, text='Select')

# Placements
btn_categories.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
fr_buttons.grid(row=0, column=0, sticky="ns")

frame_lstbox.grid(row=0, column=1, FILL='BOTH', sticky='nw')
lst_box.grid(row=0, column=1, sticky="nsew")

btn_select.grid(row=1, column = 1, sticky="nsew")

window.mainloop()