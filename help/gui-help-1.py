import time
from tkinter import *

''' ================================================== '''
def printName(event):
	print("Pressed!")

def leftClick(event):
	print("Left")

def middleClick(event):
	print("Middle")

def rightClick(event):
	print("Right")

''' ================================================== '''
class GuiPort:
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()

		self.printBtn = Button(frame, text="Submit")
		self.printBtn.bind("<Button-1>", self.printName)
		self.printBtn.pack(side=LEFT)

		self.closeBtn = Button(frame, text="Close window", command=frame.quit)
		self.closeBtn.pack(side=LEFT)

	def printName(self, event):
		print("Pressed!")

''' ================================================== '''
root = Tk()
app = GuiPort(root)
root.mainloop()


''' 
def start_gui():
	root = Tk()

	nameLabel = Label(root, text="Name")
	pwLabel = Label(root, text="Password")
	nameField = Entry(root)
	pwField = Entry(root)

	nameLabel.grid(row=0, sticky=E)
	nameField.grid(row=0, column=1)

	pwLabel.grid(row=1, sticky=E)
	pwField.grid(row=1, column=1)

	check = Checkbutton(root, text="Keep me logged in")
	check.grid(columnspan=2)

	submit = Button(root, text="Submit", bg="dodgerblue", fg="white")
	submit.bind("<Button-1>", leftClick)
	submit.bind("<Button-2>", middleClick)
	submit.bind("<Button-3>", rightClick)
	submit.grid(columnspan=2)

	root.mainloop()
'''

''' Responsive
    one = Label(root, text="One", bg="red", fg="white");
    one.pack()
    two = Label(root, text="Two", bg="blue", fg="white");
    two.pack(fill=X)
    three = Label(root, text="Three", bg="green", fg="white");
    three.pack(side=LEFT, fill=Y)
	'''


''' Positioning
	topFrame = Frame(root)
    topFrame.pack(side=TOP)
    bottomFrame = Frame(root)
    bottomFrame.pack(side=BOTTOM)

	button1 = Button(topFrame, text="a button", fg="white", bg="black")
    button1.pack(side=LEFT)
    button2 = Button(topFrame, text="2utton", fg="white", bg="black")
    button2.pack(side=RIGHT) 
	'''

''' Menus
def doNothing():
	print("this doesn't do anything")

root = Tk()

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

root.mainloop() 
'''