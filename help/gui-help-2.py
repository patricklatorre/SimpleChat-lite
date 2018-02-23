import time
from tkinter import *
import tkinter.messagebox


''' ======= global ======= '''
def doNothing():
	tkinter.messagebox.showinfo("AirPort", "this doesn't do anything")
	answer = tkinter.messagebox.askquestion("Question", "Are you going to press yes?")
	tkinter.messagebox.showinfo("Your answer", answer)

''' ======= Setup ======= '''
root = Tk()

''' ======= Main Menu ======= '''
menu = Menu(root)
root.config(menu=menu)

fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New Project", command=doNothing)
fileMenu.add_command(label="New", command=doNothing)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)

''' ======= Toolbar ======= '''
toolbar = Frame(root, bg="gray")
refreshBtn = Button(toolbar, text="Refresh", command=doNothing)
refreshBtn.pack(side=LEFT, padx=5, pady=2)
printBtn = Button(toolbar, text="Print", command=doNothing)
printBtn.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)


''' ======= Status Bar ======= '''
status = Label(root, text="Preparing to do nothing..", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

''' ======= Content ======= '''
photo = PhotoImage(file="refresh.png", width=50, height=50)
photo_con = Label(root, image=photo)
photo_con.pack()

root.mainloop()


