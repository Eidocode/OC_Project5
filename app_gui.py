import tkinter as tk

window = tk.Tk()

window.geometry('1024x768')
window.resizable(width=0, height=0)

label = tk.Label(window, text="Application Pur Beurre", font="Arial 20 bold")
label.pack()

# frame = tk.LabelFrame(window, text="Titre de la frame", padx=1000, pady=1000)
# frame.pack(fill="both", expand="yes")
 
# tk.Label(frame, text="A l'intérieure de la frame").pack()

Frame1 = tk.Frame(window, borderwidth=5, relief=tk.GROOVE)
Frame1.pack(side=tk.LEFT, padx=10, pady=30)

Frame2 = tk.Frame(window, borderwidth=2, relief=tk.GROOVE)
Frame2.pack(side=tk.LEFT, padx=10, pady=30)

tk.Label(Frame1, text="Frame 1").pack()
tk.Label(Frame2, text="Frame 2").pack()



window.mainloop()