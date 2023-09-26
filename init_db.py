import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO flashcards (term, defenition) VALUES (?, ?)",
            ('First term', 'First defenition')
            )

cur.execute("INSERT INTO flashcards (term, defenition) VALUES (?, ?)",
            ('Second term', 'Second defenition')
            )

connection.commit()
connection.close()