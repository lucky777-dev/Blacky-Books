#coding:utf-8

from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Connection

import database as db

def lbClick(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0] + 1
        reader = db.read(c, index)
        mail.set(reader["mail"])
        pwd.set("")

def connectUser():
    readerMail = mail.get()
    readerPwd = pwd.get()
    if readerMail != "" and readerPwd != "":
        id = getID(readerMail)
        if id >= 0:
            reader = db.getReader(c, id)
            if readerPwd == reader["pwd"]:
                winCon.destroy()
                entrySearch.config(state="normal")
                buttonSearch.config(state="normal")
                win.update()
            else:
                labelStatus.config(text="Mot de passe incorrect", fg="RED")
                winCon.update()
        else:
            labelStatus.config(text="L'utilisateur n'existe pas", fg="RED")
            winCon.update()


def getID(mail):
    tmp = db.getAllReaders(c)
    for reader in tmp:
        if mail == reader["mail"]:
            return reader["rowid"]
    return -1

db_path = "data.db"

# MAIN WINDOW ===============================================================

win = Tk()

search = StringVar()

frameBooks = LabelFrame(win, text="Livres", padx=25, pady=25)

entrySearch = Entry(frameBooks, width = 30, textvariable = search, state="disabled")
buttonSearch = Button(frameBooks, text="Chercher", state="disabled")

frameBooks.pack(padx=50, pady=15)

entrySearch.grid()
buttonSearch.grid(row=0, column=1)


# CONNECTION WINDOW =========================================================

winCon = Toplevel()

mail = StringVar()
pwd = StringVar()

xLeft = int(win.winfo_screenwidth()//2 - 1500)
yTop = int(win.winfo_screenheight()//2 - 400)
win.geometry(f"1000x800+{xLeft}+{yTop}")
win.resizable(False, False)
win.title("Blacky Books")

xLeft = int(winCon.winfo_screenwidth()//2 - 1300)
yTop = int(winCon.winfo_screenheight()//2 - 200)
winCon.geometry(f"+{xLeft}+{yTop}")
winCon.resizable(False, False)
winCon.title("Connexion")
frameCon = LabelFrame(winCon, text="Connectez-vous", padx=25, pady=25)

frameCon2 = Frame(winCon)

labelMail = Label(frameCon, text="Mail :")
entryMail = Entry(frameCon, width=30, textvariable = mail)
labelPwd = Label(frameCon, text="Mot de passe :")
entryPwd = Entry(frameCon, width=30, textvariable=pwd)
buttonConnect = Button(frameCon, text="Connecter", command=connectUser)
labelStatus = Label(frameCon, text="", fg="RED")

buttonNewUser = Button(frameCon2, text="Nouvel utilisateur")
buttonQuitCon = Button(frameCon2, text="Quitter", command=lambda: quitWin(win))

lbReaders = Listbox(frameCon)
"""
for i in readers:
    lbReaders.insert(END, f"{i[1]} {i[2]}")
"""
frameCon.pack(padx=50, pady=(25, 15))
frameCon2.pack(pady=(0, 15))

labelMail.grid(pady=10)
entryMail.grid(row=0, column=1, pady=10)
labelPwd.grid(row=1, pady=10)
entryPwd.grid(row=1, column=1, pady=10)
buttonConnect.grid(row=2, column=1, pady=10)
labelStatus.grid(row=3, column=0, columnspan=2)

lbReaders.grid(row=0, column=2, rowspan=3, padx=(25, 0))
lbReaders.bind("<<ListboxSelect>>", lbClick)

buttonNewUser.grid(pady=10, padx=(0, 40))
buttonQuitCon.grid(row=0, column=1, pady=10)

def populate():
    lbReaders.delete(0, END)

    for i in db.getAllReaders(c):
        lbReaders.insert(i["rowid"], f"{i['first_name']} {i['last_name']}")

def quitWin(window):
    window.destroy()


if __name__ == '__main__':
    c = db.load(db_path)
    populate()
    winCon.attributes("-topmost", True)
    win.mainloop()
    