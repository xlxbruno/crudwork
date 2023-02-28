import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())
    cur = connection.cursor()

cur.execute("INSERT INTO posts (id, title, price, image) VALUES (?, ?, ?, ?)", (1, 'Sneakers', 'Kes 2500', 'sneakers.jpg'))
cur.execute("INSERT INTO posts (id, title, price, image) VALUES (?, ?, ?, ?)", (2, 'Sandals', 'Kes 1900', 'sandals.png'))
cur.execute("INSERT INTO posts (id, title, price, image) VALUES (?, ?, ?, ?)", (3,'Boots', 'Kes 3500', 'boots.png'))

connection.commit()
connection.close()
