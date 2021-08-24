#coding:utf-8

import sqlite3
from sqlite3 import Connection

import CreateTables

def getReader(c, id):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT * FROM readers WHERE rowid=?", (id,)).fetchone()

def read(c, rowid):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM readers WHERE rowid=?", (rowid,)).fetchone()

def getAllReaders(c):
    c.row_factory = sqlite3.Row
    return c.execute("SELECT rowid, * FROM readers").fetchall()

def createTable(c):
    if c.execute("SELECT count() FROM sqlite_master WHERE type=\"table\" AND name=\"books\"").fetchone()[0] == 0:
        print("Table n'existe pas")
        CreateTables.db(c)
        c.commit()

def load(path: str):
    c = sqlite3.connect(path)
    createTable(c)
    return c
