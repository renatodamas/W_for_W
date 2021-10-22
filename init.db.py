import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    'INSERT INTO posts (title, content) values (?, ?)',
    ('First Post', 'Content for the first post')
)

cur.execute(
    'INSERT INTO posts (title, content) values (?,?) ',
    ('Second Post', 'Content for the second post')
)

connection.commit()
connection.close()
