#coding:utf-8

import sqlite3

def db(c):
    #Create a table in db
    #--------------------
    c.execute("CREATE TABLE readers (first_name TEXT, last_name TEXT, birthday TEXT, mail TEXT, pwd TEXT)")
    print("\nReaders database created!")
    all_users = [("Nicolas", "Ferbeck", "23/11/1993", "nicolas@ferbeck.net", "123"), 
                 ("Lucky", "Smile", "14/09/1992", "lucky@smile.net", "123"), 
                 ("Anne", "Onyme", "01/01/1991", "anne@onyme.net", "123")]
    c.executemany("INSERT INTO readers VALUES (?, ?, ?, ?, ?)", all_users)
    print("\n3 users added!")
    c.execute("SELECT * FROM readers")
    tmp = c.fetchall()
    for i in tmp:
        print(f"{i[0]}\t {i[1]}\t {i[2]}\t {i[3]}\t {i[4]})")
    c.execute("CREATE TABLE books (name TEXT, author TEXT)")
    print("\nBooks database created!")

    #Insert multiple lines at once in db
    #-----------------------------------
    all_books = [("Iliade", "Homère"), 
                        ("Odyssée", "Homère"), 
                        ("À la recherche du temps perdu", "Marcel Proust"),
                        ("Hamlet", "William Shakespeare"), 
                        ("Le petit Prince", "Antoine de Saint-Exupéry"),
                        ("Le Seigneur des anneaux", "J. R. R. Tolkien"), 
                        ("Le choix de Sophie", "William Styron"),
                        ("Gaston Lagaffe", "André Franquin"), 
                        ("Les fourmis", "Bernard Werber"),
                        ("Les Thanatonautes", "Bernard Werber"), 
                        ("L'empire des anges", "Bernard Werber"),
                        ("Nous les dieux", "Bernard Werber"), 
                        ("L'arbre des possibles", "Bernard Werber"), 
                        ("Comment l'hypnose a changé ma vie", "Éric Normandin"),
                        ("Jeux vidéos et rage", "Nicolas Ferbeck"),
                        ("SQL pour les nuls", "Allen G. Taylor"),
                        ("Python pour les nuls", "John Paul Mueller"),
                        ("Harry Potter à l'école des sorciers", "J. K. Rowling"),
                        ("Harry Potter et la chambre des secrets", "J. K. Rowling"),
                        ("Harry Potter et le prisonnier d'Azkaban", "J. K. Rowling"),
                        ("Harry Potter et la coupe de feu", "J. K. Rowling"),
                        ("Harry Potter et l'ordre du phénix", "J. K. Rowling"),
                        ("Harry Potter et le prince de sang-mêlé", "J. K. Rowling"),
                        ("Harry Potter et les reliques de la mort", "J. K. Rowling")]
    c.executemany("INSERT INTO books VALUES (?, ?)", all_books)
    print("\n24 books added!")
    c.execute("SELECT * FROM books")
    tmp = c.fetchall()
    for i in tmp:
        print(f"{i[0]}\t ({i[1]})")
        
if __name__ == "__main__":
    #Connects to database (creates it if it doesn't exists)
    con = sqlite3.connect("data.db")

    #Create cursor
    c = con.cursor()
    
    db(c)