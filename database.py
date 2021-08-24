#coding:utf-8

import sqlite3
from sqlite3 import Connection

import CreateTables

def createReader(c: Connection, readers: dict ) -> bool :
    f_name = readers["first_name"]
    l_name= readers["last_name"]
    birthday = readers["birthday"]
    mail = readers["mail"]
    pwd = readers["pwd"]
    readers["id"] = c.execute("INSERT INTO readers(first_name, last_name, birthday, mail, pwd) VALUES (?,?,?,?,?)",(f_name,
                        l_name, birthday, mail, pwd ))
    c.commit()
    return readers

def createBook(c: Connection, books: dict) -> bool:
    nameBook = books["name"]
    nameAuthor = books["author"]
    books["id"] = c.execute("INSERT INTO books(name, author) VALUES (?,?)", (nameBook, nameAuthor))

    c.commit()
    return books

def getReader(c, id):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT * FROM readers WHERE rowid=?", (id,)).fetchone()

def getBook(c, id):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM books WHERE rowid=?", (str(id),)).fetchone()

def read(c, rowid):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM readers WHERE rowid=?", (rowid,)).fetchone()

def readBook(c, rowid):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM books WHERE rowid=?",(rowid,)).fetchone()

def getAllReaders(c):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM readers").fetchall()

def getAllBooks(c):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM books").fetchall()

def getAllLoaned(c):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM loan").fetchall()

def getLoaned(c, userID):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM loan WHERE user == ?", (userID,)).fetchall()

def getLoanedBook(c, userID, bookID):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM loan WHERE user == ? AND book == ?", (userID, bookID)).fetchone()

def loan(c, userID, bookID):
    c.execute("INSERT INTO loan VALUES (?, ?)", (userID, bookID))
    c.commit()

def bringBack(c, loanID):
    c.execute(f"DELETE FROM loan WHERE rowid == ?", (int(loanID),))
    c.commit()

def createTable(c):
    if c.execute("SELECT count() FROM sqlite_master WHERE type=\"table\" AND name=\"books\"").fetchone()[0] == 0:
        print("Table n'existe pas")
        CreateTables.db(c)
        c.commit()

def searchBook(c, name):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM books WHERE name LIKE ?", ("%" + name + "%",)).fetchall()
    

def load(path: str):
    c = sqlite3.connect(path)
    createTable(c)
    return c

def deleteBook(c: Connection, rowid: int):
    c.execute("DELETE FROM books WHERE rowid=?",(rowid,))
    c.commit()
