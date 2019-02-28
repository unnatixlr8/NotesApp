from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class Main():
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("Login")

        self.page = StringVar()
        self.loginName = StringVar()
        self.loginPass = StringVar()
        self.signupName = StringVar()
        self.signupPass = StringVar()
        self.sts = StringVar()
        self.createWidgets()
        self.showLogin()

    def createWidgets(self):
        Label(self.parent,textvariable = self.page,font = ("",20)).pack()
        frame1 = Frame(self.parent)
        Label(frame1,text = "Name").grid(sticky = W)
        Entry(frame1,textvariable = self.loginName).grid(row = 0,column = 1,pady = 10,padx = 10)
        Label(frame1,text = "Password").grid(sticky = W)
        Entry(frame1,textvariable = self.loginPass,show="*").grid(row = 1,column = 1)
        Button(frame1,text = "Login",command=self.login).grid(pady = 10)
        Button(frame1,text = "Sign Up",command=self.signup).grid(row = 2,column = 1,pady = 10)

        frame2 = Frame(self.parent)
        Label(frame2,text = "Name").grid(sticky = W)
        Entry(frame2,textvariable = self.signupName).grid(row = 0,column = 1,pady = 10,padx = 10)
        Label(frame2,text = "Password").grid(sticky = W)
        Entry(frame2,textvariable = self.signupPass,show="*").grid(row = 1,column = 1)
        Button(frame2,text = "Create",command=self.create).grid(pady = 10)
        Button(frame2,text = "Back",command=self.showLogin).grid(row = 2,column = 1,pady = 10)


        self.loginFrame  = frame1
        self.signupFrame  = frame2

        Label(self.parent, textvariable = self.sts).pack()

    def login(self):
        name = self.loginName.get()
        password = self.loginPass.get()
        
        try:
            conn = mysql.connector.connect(user='root',password='nirmmaalyam',host='127.0.0.1',database='python')
            cursor = conn.cursor()
            print("database connected")
            cursor.execute("SELECT * FROM users WHERE uname='%s' and upass='%s'" % (name,password) )
            row = cursor.fetchone()
            print("Login Attempt")
            if(row == None):
                messagebox.showinfo("Error", "User Log in Failed !!!")
            else:
                messagebox.showinfo("Success", "User Logged in Sucessfully !")
        except mysql.connector.Error as error:
            conn.rollback()
            print("Error")
            messagebox.showerror("Error", "Connection to database Failed !!!")
        finally:
            cursor.close()
            conn.close()
            print("connection closed")




    def signup(self):
        self.page.set("Sign Up")
        self.loginFrame.pack_forget()
        self.signupFrame.pack()

    def showLogin(self):
        self.page.set("Login")
        self.signupFrame.pack_forget()
        self.loginFrame.pack()

    
    def create(self):
        name = self.signupName.get()
        password = self.signupPass.get()
        try:
        	conn = mysql.connector.connect(user='root',password='nirmmaalyam',host='127.0.0.1',database='python')
        	cursor = conn.cursor()
        	print("database connected")
        	cursor.execute("INSERT INTO users(uname,upass) VALUES('%s','%s')" % (name,password))
        	conn.commit()
        	print("User Added")
        	messagebox.showinfo("Success", "User created Sucessfully !")
        except mysql.connector.Error as error:
        	conn.rollback()
        	print("Error")
        	messagebox.showerror("Error", "User Creation Failed !!!")
        finally:
        	cursor.close()
        	conn.close()
        	print("connection closed")
        self.showLogin()

if __name__ == "__main__":
    root = Tk()
    Main(root)
root.mainloop()