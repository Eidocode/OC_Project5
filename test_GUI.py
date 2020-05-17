from tkinter import *

window = Tk()

label = Label(window, text="Hello World", bg="yellow")
label.pack()

button = Button(window, text="close", command=window.quit)
button.pack()

value = StringVar()
value.set("Texte par défaut")
entree = Entry(window, value=string, width=30)
entree.pack()

window.mainloop()