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
		strVar = StringVar()

		try:
			conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
			cursor = conn.cursor()
			print("Database connected")
			cursor.execute("SELECT * from notes")
			results = cursor.fetchall()
			print("Data fetched")
			for row in results:
				#print(row[0]+"	"+row[1]+"	"+row[2])
				print(row)

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
	