from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

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
		global textBox
		textBox = Text(master,highlightbackground="Black",font=("Verdana",14))
		textBox.pack()
		addButton = ttk.Button(master, text="Save Note", command=self.uploadNote)
		addButton.pack(pady=5,ipadx=10,ipady=5)

	def uploadNote(self):
		noteToPost = textBox.get(1.0, "end-1c")
		try:
			conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("database connected")
			cursor.execute("INSERT INTO notes(note) VALUES('%s')" %(noteToPost))
			conn.commit()
			print("Note Added")
			messagebox.showinfo("Success", "Your note has been posted")

		except mysql.connector.Error as error:
			conn.rollback()
			print("Error")
			messagebox.showerror("Error", "You note has NOT been posted")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")


root = Tk()
rootObj = NotesWindow(root)
root.mainloop()