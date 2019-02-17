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
				timeStampStrVar = StringVar(value=str(row[1]))
				noteStrVar = StringVar(value=str(row[2]))
				idLabel = Label(windowFrame, textvariable=idStrVar,font=("Verdana",18))
				idLabel.pack()
				timeStampLabel = Label(windowFrame, textvariable=timeStampStrVar, font=("Verdana",18))
				timeStampLabel.pack()
				noteLabel = Label(windowFrame, wraplength=600, textvariable=noteStrVar, font=("Verdana",18))
				noteLabel.pack()
				Label(windowFrame,text="\n").pack()

			master.update()
			canvas.config(scrollregion=canvas.bbox("all"))



		except mysql.connector.Error as error:
			print("Error")
			messagebox.showerror("Error", "Could not connect to database")

		finally:
			cursor.close()
			conn.close()
			print("connection closed")


root = Tk()
rootObj = ViewWindow(root)
root.mainloop()
	