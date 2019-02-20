from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


class ViewWindow():
	def __init__(self,master):
		self.master = master
		master.geometry("800x600")
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
		canvas.create_window(0,0,window=windowFrame, anchor='nw')

		try:
			conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
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
				insideFrame = Frame(windowFrame,highlightbackground="green", highlightcolor="green", highlightthickness=1) #for individual frame
				idLabel = Label(insideFrame, textvariable=idStrVar,font=("Verdana",18))
				idLabel.pack()
				timeStampLabel = Label(insideFrame, textvariable=timeStampStrVar, font=("Verdana",18))
				timeStampLabel.pack()
				noteLabel = Label(insideFrame, wraplength=600, textvariable=noteStrVar, font=("Verdana",18))
				noteLabel.pack()
				Label(insideFrame,text="\n").pack()
				deleteButton = ttk.Button(insideFrame,text="Delete", command = lambda idParameter = idParameter, insideFrame = insideFrame : self.deleteNote(idParameter,insideFrame))
				deleteButton.pack()
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
			conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
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





root = Tk()
rootObj = ViewWindow(root)
root.mainloop()
	