from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import sys
import os
import mysql.connector
from mysql.connector import Error


class ViewWindow():
	def __init__(self,master):
		self.master = master
		master.geometry("1366x768")
		master.title("View Notes")
		self.noteBox(master)


	def noteBox(self,master):
		self.master = master
		scrollBar = Scrollbar(master)
		canvas = Canvas(master,background = "#D2D2D2",yscrollcommand=scrollBar.set)
		scrollBar.config(command=canvas.yview)
		scrollBar.pack(side=RIGHT, fill=Y)
		windowFrame = Frame(canvas)
		canvas.pack(side="left", fill="both", expand=True)
		rightFrame = Frame(canvas)
		
		canvas.create_window(0,0,window=windowFrame, anchor='nw')
		rightFrame.pack(side="right")
		self.addWindow(rightFrame)

		try:
			conn = mysql.connector.connect(user='root', password='nirmmaalyam',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("Database connected")
			cursor.execute("SELECT * from notes")
			results = cursor.fetchall()
			print("Data fetched")
			for row in results:
				print(str(row[0])+"	"+str(row[1])+"	"+str(row[2]))
				idStrVar = StringVar(value=str(row[0]))
				idParameter = row[0]
				timeStampStrVar = StringVar(value=str(row[1]))
				noteStrVar = StringVar(value=str(row[2]))
				noteParameter = row[2]
				insideFrame = Frame(windowFrame,highlightbackground="green", highlightcolor="green", highlightthickness=1) #for individual frame
				idLabel = Label(insideFrame, textvariable=idStrVar,font=("Verdana",18))
				idLabel.pack()
				timeStampLabel = Label(insideFrame, textvariable=timeStampStrVar, font=("Verdana",18))
				timeStampLabel.pack()
				noteLabel = Label(insideFrame, wraplength=600, textvariable=noteStrVar, font=("Verdana",18))
				noteLabel.pack()
				Label(insideFrame,text="\n").pack()
				deleteButton = ttk.Button(insideFrame,text="Delete", command = lambda idParameter = idParameter, insideFrame = insideFrame : self.deleteNote(idParameter,insideFrame))
				deleteButton.pack(side=LEFT, padx=3)
				updateButton = ttk.Button(insideFrame,text="Update", command = lambda idParameter = idParameter, noteParameter = noteParameter : self.updateNote(idParameter, noteParameter, self.master))
				updateButton.pack(side=LEFT, padx=3)
				Label(insideFrame,text="\n").pack()
				insideFrame.pack(fill=X)

			master.update()
			canvas.config(scrollregion=canvas.bbox("all"))



		except mysql.connector.Error as error:
			print("Error")
			messagebox.showerror("Error", "Could not connect to database")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")


	def deleteNote(self,idNote,insideFrame):
		self.insideFrame = insideFrame
		try:
			conn = mysql.connector.connect(user='root', password='nirmmaalyam',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("Going to delete %s" %(idNote))
			cursor.execute("DELETE FROM notes WHERE (id=%s)" %(idNote))
			conn.commit()
			print("Note Deleted")
			insideFrame.destroy()

		except mysql.connector.Error as error:
			conn.rollback()
			print("Error, cannot delete")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")


	def updateNote(self,idNote, noteParameter, master):
		updateWindow = Toplevel(master,height=500, width=500)
		updateWindow.title("Update Note")
		self.updateBox = Text(updateWindow,highlightbackground="Black",font=("Verdana",14))
		self.updateBox.insert('1.0', noteParameter)
		self.updateBox.pack(padx=3,pady=3)
		submitButton = ttk.Button(updateWindow,text="Update Note", command=lambda : self.saveUpdateNote(idNote))
		submitButton.pack(pady=3)


	def saveUpdateNote(self,idNote):
		updateNotePost = self.updateBox.get(1.0,"end-1c")
		try:
			conn = mysql.connector.connect(user='root', password='nirmmaalyam',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("database connected")
			cursor.execute("UPDATE notes SET note = '%s' WHERE id = '%s'" %(updateNotePost,idNote))
			conn.commit()
			messagebox.showinfo("Success", "Your note has been updated")
			python = sys.executable
			os.execl(python,python, * sys.argv)

		except mysql.connector.Error as error:
			conn.rollback()
			print("Error")
			messagebox.showerror("Error", "Your note has NOT been updated")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")


	def restart_program(self):
		python = sys.executable
		os.execl(python,python, * sys.argv)


	def addWindow(self,master):
		self.master = master
		titleLabel = Label(master, text="Add New Note", font=("Verdana", 24))
		titleLabel.pack(pady=3)
		global textBox
		textBox = Text(master,highlightbackground="Black",font=("Verdana",14))
		textBox.pack(padx=3)
		addButton = ttk.Button(master, text="Save Note", command=self.uploadNote)
		addButton.pack(pady=5,ipadx=10,ipady=5)

	def uploadNote(self):
		noteToPost = textBox.get(1.0, "end-1c")
		try:
			conn = mysql.connector.connect(user='root', password='nirmmaalyam',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("database connected")
			cursor.execute("INSERT INTO notes(note) VALUES('%s')" %(noteToPost))
			conn.commit()
			print("Note Added")
			messagebox.showinfo("Success", "Your note has been posted")
			python = sys.executable
			os.execl(python,python, * sys.argv)


		except mysql.connector.Error as error:
			conn.rollback()
			print("Error")
			messagebox.showerror("Error", "Your note has NOT been posted")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")

def main():
	root = Tk()
	root.resizable(False, False)
	rootObj = ViewWindow(root)
	root.mainloop()

if __name__ == "__main__":
	main()
	