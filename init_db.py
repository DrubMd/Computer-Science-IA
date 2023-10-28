import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('DrubMD', '12345678')
            )
cur.execute("DELETE FROM users WHERE username = 'DrubMD'")

connection.commit()
connection.close()