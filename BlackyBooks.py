#coding:utf-8

from os import name
from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Connection
import database as db

def bookAdd():
    winAdd = Toplevel()
    xLeft = int(winAdd.winfo_screenwidth()//2 - 300)
    yTop = int(winAdd.winfo_screenheight()//2 - 500)
    winAdd.geometry(f"+{xLeft}+{yTop}")
    winAdd.resizable(False, False)
    #winAdd.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
    winAdd.title("Add-Book")

    frameAdd = LabelFrame(winAdd)
    frameAdd2 = Frame(winAdd)

    labelName = Label(frameAdd, text = "Nom: ")
    entryName = Entry(frameAdd, width= 30, textvariable= nameBook)
    labelAuthor = Label(frameAdd, text="Auteur: ")
    entryAuthor = Entry(frameAdd, width=30, textvariable=authorBook)
    buttonAdd = Button(frameAdd2, text="Ajouter", command= lambda: createbook())
    buttonQuitAdd = Button(frameAdd2, text="Quitter", command= lambda: quitWin(winAdd))

    frameAdd.pack(padx=50, pady=(25,15))
    frameAdd2.pack(padx=50, pady=(25,15))

    labelName.grid(padx=25)
    entryName.grid(row=0, column=1)
    labelAuthor.grid(row=1)
    entryAuthor.grid(row=1, column=1)
    buttonAdd.grid(padx=25)
    buttonQuitAdd.grid(row=0, column=1)

    def createbook():
        books = {"id": -1, "name": entryName.get(), "author": entryAuthor.get()}
        db.createBook(c, books)
        populateBooks()
        win.update()
        winAdd.destroy()
        messagebox.showinfo("Succès","Votre livre à bien été ajouté. Merci pour votre participation")


def deleteBook():
    index = lbBooks.curselection() [0]
    id = booksList[index]["rowid"]
    if messagebox.askyesno("Sur?", f"Voulez-vous vraiment supprimer le livre '{db.getBook(c, id)['name']}'"):
        db.deleteBook(c, id)
        populateBooks()   

def searchBook():
    searchName = search.get()
    if searchName != "":
        booksFound = db.searchBook(c, searchName)
        if len(booksFound) >= 1:
            lbBooks.delete(0, END)
            booksList.clear()

            cpt = 0
            for i in booksFound:
                booksList.append(i)
                lbBooks.insert(cpt,f"{i['name']}")
                if bookFree(i):
                    lbBooks.itemconfig(cpt, foreground="GREEN")
                else:
                    lbBooks.itemconfig(cpt, foreground="RED")
                cpt += 1
        else:
            messagebox.showinfo("Oups","Nous n'avons pas trouver votre livre :(")
    else:
        populateBooks()

def lbClick(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        reader = db.read(c, readersList[index]["rowid"])
        mail.set(reader["mail"])
        pwd.set("")

def lbClickBook(event):
    global book
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        book = db.readBook(c, booksList[index]["rowid"])
        entryNameBook.config(text=book["name"])
        entryNameAuthor.config(text=book["author"])
        win.update()

def lbClickLoan(event):
    global selectedLoaned
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        selectedLoaned = db.getLoanedBook(c, connectedUserID, loanedList[index]["book"])["rowid"]
       
def connectUser():
    readerMail = mail.get()
    readerPwd = pwd.get()
    if readerMail != "" and readerPwd != "":
        id = getID(readerMail)
        if id >= 0:
            reader = db.getReader(c, id)
            if readerPwd == reader["pwd"]:
                global connectedUserID
                connectedUserID = id
                winCon.destroy()
                entrySearch.config(state="normal")
                buttonSearch.config(state="normal")
                win.update()
                populateBooks()
                populateLoan()
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

def getidBook(name):
    tmp = db.getAllBooks(c)
    for book in tmp:
        if name == book["name"]:
            return book["rowid"]
    return -1

def newuser():
    winNewUser = Toplevel()
    winNewUser.attributes("-topmost", True)

    firs_name = StringVar()
    last_name = StringVar()
    dateOfBirth = StringVar()
    mail = StringVar()
    pwd = StringVar()
    validPwd = StringVar()

    xLeft = int(win.winfo_screenwidth()//2 - 500)
    yTop = int(win.winfo_screenheight()//2 - 500)
    winNewUser.geometry(f"1000x800+{xLeft}+{yTop}")
    winNewUser.resizable(False, False)
    winNewUser.title("Nouvelle utilisateur")
    #winNewUser.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
    frameNewUser = LabelFrame(winNewUser,text="Remplissez les champs pour vous connecter",padx=25, pady=25)

    frameNewUser2=Frame(winNewUser)

    labelFirstName = Label(frameNewUser,text="Prénom: ")
    entryFirstName = Entry(frameNewUser,width=30, textvariable=firs_name)
    labelLastName= Label(frameNewUser,text="Nom: ")
    entryLastName= Entry(frameNewUser, width=30, textvariable=last_name)
    labelDateOfBirth=Label(frameNewUser,text="Date de naissance: ")
    entryDateOfBirth=Entry(frameNewUser, width=30, textvariable=dateOfBirth)
    labelMail = Label(frameNewUser,text="Mail: ")
    entryMail = Entry(frameNewUser, width=30, textvariable=mail)
    labelPwdUser = Label(frameNewUser, text="Mot de passe: ")
    entryPwdUSer = Entry(frameNewUser, width=30, textvariable=pwd, show='*')
    labelValidPwd = Label(frameNewUser,text="Confirmer le mot de passe: ")
    entryValidPwd = Entry(frameNewUser, width=30, textvariable=validPwd, show='*')
    labelStatuePwd = Label(frameNewUser, text="", fg="RED")

    buttonNewUser = Button(frameNewUser2, text="Créer", command= lambda: validUser())
    buttonQuit = Button(frameNewUser2, text="Quitter",command= lambda: quitWin(winNewUser))

    frameNewUser.pack(padx=50, pady=(25,15))
    frameNewUser2.pack(pady=(0, 15))

    labelFirstName.grid(padx=25)
    entryFirstName.grid(row=0, column=1, pady=10)
    labelLastName.grid(row=1, pady=10)
    entryLastName.grid(row=1, column=1, pady=10)
    labelDateOfBirth.grid(row=2, pady=10)
    entryDateOfBirth.grid(row=2, column=1 , pady=10)
    labelMail.grid(row=3, pady=10)
    entryMail.grid(row=3, column=1 ,pady=10)
    labelPwdUser.grid(row=4, pady=10)
    entryPwdUSer.grid(row=4, column=1, pady=10)
    labelValidPwd.grid(row=5, pady=10)
    entryValidPwd.grid(row=5, column=1, pady=10)
    labelStatuePwd.grid(row=6, column=0, columnspan = 2)

    buttonNewUser.grid(row=6, pady=10, padx=50)
    buttonQuit.grid(row=6, column=2, pady=10,padx=50)

    def validUser():
        """Création d'un contact dans la base de donnée"""
        if entryPwdUSer.get() == "" and entryValidPwd.get() == "":
            labelStatuePwd.config(text="Mot de passe obligatoire")
            winNewUser.update()
        else:
            if entryPwdUSer.get() == entryValidPwd.get():
                readers = {"id": -1, "first_name": entryFirstName.get(), "last_name": entryLastName.get(), "birthday": entryDateOfBirth.get(), "mail": entryMail.get(), 
                            "pwd": entryPwdUSer.get()}
                db.createReader(c, readers)
                populateReaders()
                winNewUser.destroy()
            else:
                labelStatuePwd.config(text="Mot de passe incorrect\nVérifier si ils sont identique",fg="RED")
                winNewUser.update()
               
db_path = "data.db"

def bookFree(book):
    tmp = db.getAllLoaned(c)
    for i in tmp:
        if str(book["rowid"]) == str(i["book"]):
            return False
    return True

def loan():
    try:
        bookTry = book["name"]
        bookIDTry = book["rowid"]
    except:
        messagebox.showerror("Erreur", "Aucun livre sélectionné")
    if bookFree(book):
        if messagebox.askyesno("Sur?", f"Voulez-vous emprunter {book['name']}"):
                db.loan(c, connectedUserID, book["rowid"])
                populateBooks()
                populateLoan()
    else:
        messagebox.showerror("Erreur", "Le livre a déja été emprunté")

def bringBack():
    try:
        db.bringBack(c, selectedLoaned)
        populateBooks()
        populateLoan()
    except:
        messagebox.showerror("Erreur", "Aucun livre sélectionné")

def populateReaders():
    lbReaders.delete(0, END)
    readersList.clear()

    for i in db.getAllReaders(c):
        readersList.append(i)
        lbReaders.insert(i["rowid"], f"{i['first_name']} {i['last_name']}")

def populateBooks():
    lbBooks.delete(0, END)
    booksList.clear()

    cpt = 0
    for i in db.getAllBooks(c):
        booksList.append(i)
        lbBooks.insert(cpt,f"{i['name']}")
        if bookFree(i):
            lbBooks.itemconfig(cpt, foreground="GREEN")
        else:
            lbBooks.itemconfig(cpt, foreground="RED")
        cpt += 1

def populateLoan():
    lbLoan.delete(0, END)
    loanedList.clear()

    for i in db.getLoaned(c, connectedUserID):
        loanedList.append(i)
        lbLoan.insert(i["rowid"], f"{db.getBook(c, i['book'])['name']}")

def quitWin(window):
    window.destroy()

# MAIN WINDOW ===============================================================

win = Tk()

xLeft = int(win.winfo_screenwidth()//2 - 500)
yTop = int(win.winfo_screenheight()//2 - 500)
win.geometry(f"720x480+{xLeft}+{yTop}")
win.resizable(False, False)
#win.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
win.title("Blacky Books")

nameBook = StringVar()
authorBook = StringVar()
search = StringVar()

frameBooks = LabelFrame(win, text="Recherche", padx=25, pady=25)
frameBooks2 = LabelFrame(win, text= "Livres", padx=15, pady=15)
frameBooks3 = Frame(win)

entrySearch = Entry(frameBooks, width = 30, textvariable = search, state="disabled")
buttonSearch = Button(frameBooks, text="Chercher", command=searchBook)
buttonAdd = Button(frameBooks, text="Ajouter", command=bookAdd)
buttonDelete = Button(frameBooks, text="Supprimer", command=deleteBook)

labelNameBook = Label(frameBooks2, text="Nom: ")
entryNameBook = Label(frameBooks2, text="", width=30)
labelNameAuthor = Label(frameBooks2, text="Auteur: ")
entryNameAuthor = Label(frameBooks2, text="", width=30)
lbBooks = Listbox(frameBooks2)
lbLoan = Listbox(frameBooks2)

labelNameBook.grid(row=0, column=1, pady=10)
entryNameBook.grid(row=0, column=2)
labelNameAuthor.grid(row=1, column=1, pady=10)
entryNameAuthor.grid(row=1, column=2)
lbBooks.grid(row=0, column=3, rowspan=3, padx=10)
lbBooks.bind("<<ListboxSelect>>", lbClickBook)
lbLoan.bind("<<ListboxSelect>>", lbClickLoan)
lbLoan.grid(row=0, column=4, rowspan=3)

frameBooks.pack(padx=50, pady=15)
frameBooks2.pack(pady=(25, 15))
frameBooks3.pack()

entrySearch.grid(padx=(0, 5))
buttonSearch.grid(row=0, column=1, padx=5)
buttonAdd.grid(row=0, column=2, padx=5)
buttonDelete.grid(row=0, column=3, padx=(5, 0))

buttonLoan = Button(frameBooks3, text= "Emprunter", command=loan)
buttonBringBack = Button(frameBooks3, text="Rendre", command=bringBack)
buttonQuitBooks = Button(frameBooks3, text="Quitter", command= lambda: quitWin(win))

buttonLoan.grid()
buttonBringBack.grid(row=0, column=1, padx=50)
buttonQuitBooks.grid(row=0, column=2)


# CONNECTION WINDOW =========================================================

winCon = Toplevel()

mail = StringVar()
pwd = StringVar()

xLeft = int(winCon.winfo_screenwidth()//2 - 300)
yTop = int(winCon.winfo_screenheight()//2 - 500)
winCon.geometry(f"+{xLeft}+{yTop}")
winCon.resizable(False, False)
winCon.title("Connexion")
#winCon.iconbitmap("D:\Etudes\Ecole\TFE\TFE_Biblio\Code\Blacky-Book2\Blacky-Book\BookSeel.ico")
frameCon = LabelFrame(winCon, text="Connectez-vous", padx=25, pady=25)

frameCon2 = Frame(winCon)

labelMail = Label(frameCon, text="Mail :")
entryMail = Entry(frameCon, width=30, textvariable = mail)
labelPwd = Label(frameCon, text="Mot de passe :")
entryPwd = Entry(frameCon, width=30, textvariable=pwd,show='*')
buttonConnect = Button(frameCon, text="Connecter", command=connectUser)
labelStatus = Label(frameCon, text="", fg="RED")

buttonNewUser = Button(frameCon2, text="Nouvel utilisateur",command=newuser)
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

if __name__ == '__main__':
    c = db.load(db_path)
    readersList = []
    booksList = []
    loanedList = []
    populateReaders()
    winCon.attributes("-topmost", True) 
    win.mainloop()
