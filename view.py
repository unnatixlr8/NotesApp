from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import sys
import os
import mysql.connector
from mysql.connector import Error
import json, urllib.request, urllib.parse, ssl

global na
class Main():
    def __init__(self,parent):
        self.parent = parent
        #self.parent.title("Loginn")

        self.page = StringVar()
        self.loginName = StringVar()
        self.loginPass = StringVar()
        self.signupName = StringVar()
        self.signupPass = StringVar()
        self.sts = StringVar()
        self.createWidgets()
       # self.showLogin()
        self.ViewWindow(parent)




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
        global na
        na=name
        #Code for linking to view window
        try:
            conn = mysql.connector.connect(user='root',password='pythondb',host='127.0.0.1',database='python')
            cursor = conn.cursor()
            print("database connected")
            cursor.execute("SELECT * FROM users WHERE uname='%s' and upass='%s'" % (name,password) )
            row = cursor.fetchone()
            print("Login Attempt")
            if(row == None):
                messagebox.showinfo("Error", "User Log in Failed !!!")
                self.parent.destroy()
            else:
                messagebox.showinfo("Success", "User Logged in Sucessfully !")

                self.loginFrame.destroy()
                self.page.set("")

                self.noteBox(self.parent,name)
                

        except mysql.connector.Error as error:
            conn.rollback()
            print("Error")
            messagebox.showerror("Error", "Connection to database Failed !!!")
            self.parent.destroy() 
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
        global name
        name = self.signupName.get()
        password = self.signupPass.get()
        try:
            conn = mysql.connector.connect(user='root',password='pythondb',host='127.0.0.1',database='python')
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

    def ViewWindow(self,master):
        self.master = master
        self.page.set("Login")
        self.loginFrame.pack()
        master.geometry("1366x768")
        master.title("Notes")
        

    def noteBox(self,master,name):
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
            conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
            cursor = conn.cursor()
            print("Database connected")
            cursor.execute("SELECT * from notes WHERE uname='%s'" % (name) )
            results = cursor.fetchall()
            print("Data fetched")
            for row in results:
                print(str(row[0])+" "+str(row[3])+" "+str(row[2]))
                idStrVar = StringVar(value=str(row[0]))
                idParameter = row[0]
                timeStampStrVar = StringVar(value=str(row[3]))
                noteStrVar = StringVar(value=str(row[2]))
                noteParameter = row[3]
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
                smsButton = ttk.Button(insideFrame,text="SMS", command = lambda noteParameter = noteParameter : self.smsNote(noteParameter,self.master))
                smsButton.pack(side=LEFT, padx=3)
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
            conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
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
            conn = mysql.connector.connect(user='root', password='pythondb',host='127.0.0.1',database='python')
            cursor = conn.cursor()
            print("database connected")
            cursor.execute("INSERT INTO notes(uname,note) VALUES('%s','%s')" %(na,noteToPost))
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

    def smsNote(self, noteParameter, master):
        self.mobileWindow = Toplevel(master,height=300, width=200)
        self.mobileWindow.title("Send as SMS")
        self.numVar = StringVar()
        self.mobileEntry = Entry(self.mobileWindow, textvariable=self.numVar)
        self.mobileEntry.grid(row=1, column=0)
        noteSent = str(noteParameter)
        sendButton = ttk.Button(self.mobileWindow, text="Send", command = lambda noteSent = noteSent : self.getNumber(noteSent))
        sendButton.grid(row=1, column=1)

    def getNumber(self,noteSent):
        number = self.numVar.get()
        TEXTLOCAL_API = '2AQn1u6DJg4-e4Mju1PjtT3ApXsXXOJ3P0g20n2WpE'
        resp = self.sendSMS(TEXTLOCAL_API,number,noteSent,'TXTLCL')
        print(resp)
        self.mobileWindow.destroy()


    def sendSMS(self, apikey, numbers, message, sender):
        data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender})
        data = data.encode('utf-8')
        context = ssl._create_unverified_context()
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data, context=context)
        fr = f.read()
        return(fr)


def main():
    root = Tk()
    root.resizable(False, False)
    Main(root)

    root.mainloop()

if __name__ == "__main__":
    main()
    