from tkinter import *

window = Tk()

label = Label(window, text="Hello World", bg="yellow")
label.pack()

button = Button(window, text="close", command=window.quit)
button.pack()

value = StringVar()
value.set("Texte par défaut")
entree = Entry(window, textvariable=value, width=30)
entree.pack()

value = StringVar()
button1 = Radiobutton(window, text='Oui', variable=value, value=1)
button2 = Radiobutton(window, text='Non', variable=value, value=2)
button3 = Radiobutton(window, text='Peut-être', variable=value, value=3)
button1.pack()
button2.pack()
button3.pack()

liste = Listbox(window)
liste.insert(1, "Python")
liste.insert(2, "PHP")
liste.insert(3, "JQuery")
liste.insert(4, "CSS")
liste.insert(5, "JavaScript")
liste.pack()

canvas = Canvas(window, width=150, height=120, background='yellow')
ligne1 = canvas.create_line(75, 0, 75, 120)
ligne2 = canvas.create_line(0, 60, 150, 60)
txt = canvas.create_text(75, 60, text='Cible', font="Arial 16 italic", fill='blue')
canvas.pack()

value = DoubleVar()
scale = Scale(window, variable=value)
scale.pack()

window['bg']='white'

# frame 1
Frame1 = Frame(window, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=30, pady=30)

# frame 2
Frame2 = Frame(window, borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=10, pady=10)

# frame 3 dans frame 2
Frame3 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
Frame3.pack(side=RIGHT, padx=5, pady=5)

# Ajout de labels
Label(Frame1, text="Frame 1").pack(padx=10, pady=10)
Label(Frame2, text="Frame 2").pack(padx=10, pady=10)
Label(Frame3, text="Frame 3", bg="white").pack(padx=10, pady=10)


p = PanedWindow(window, orient=VERTICAL)
p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
p.add(Label(p, text='Volet 1', background='blue', anchor=CENTER))
p.add(Label(p, text='Volet 2', background='white', anchor=CENTER) )
p.add(Label(p, text='Volet 3', background='red', anchor=CENTER) )
p.pack()

l = LabelFrame(window, text="Titre de la frame", padx=20, pady=20)
l.pack(fill="both", expand="yes")
 
Label(l, text="A l'intérieure de la frame").pack()

window.mainloop()