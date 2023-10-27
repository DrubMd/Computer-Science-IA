import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO flashcards (term, definition) VALUES (?, ?)",
            ('First term', 'First definition')
            )

cur.execute("INSERT INTO flashcards (term, definition) VALUES (?, ?)",
            ('Second term', 'Second definition')
            )

connection.commit()
connection.close()