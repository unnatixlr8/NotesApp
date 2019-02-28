from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import add
import view

class FrontView():
	def __init__(self,master):
		self.master = master
		master.geometry("800x600") #Width x Height
		master.title("Note-Py")
		self.header = Label(master, text="Note-Py", font=("Verdana", 24))
		self.header.pack()
		self.addButton = ttk.Button(master, text="Add Note", command=self.openAddNote())
		self.addButton.pack()
		self.viewButton = ttk.Button(master, text="View Note")
		self.viewButton.pack()

	def openAddNote(self):
		add.main()


def main():
	root = Tk()
	rootObj = FrontView(root)
	root.mainloop()

if __name__ == "__main__":
	main()