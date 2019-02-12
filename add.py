from tkinter import *
from tkinter import ttk 

class NotesWindow():
	def __init__(self,master):
		self.master = master
		master.geometry("800x600") #Width x Height
		master.title("Add Note")
		self.addWindow(master)

	def addWindow(self,master):
		self.master = master
		titleLabel = Label(master, text="Add New Note", font=("Verdana", 24))
		titleLabel.pack(pady=3)
		textBox = Text(master,highlightbackground="Black",font=("Verdana",14))
		textBox.pack()
		addButton = ttk.Button(master, text="Save Note")
		addButton.pack(pady=5,ipadx=10,ipady=5)


root = Tk()
rootObj = NotesWindow(root)
root.mainloop()