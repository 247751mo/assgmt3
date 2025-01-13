import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO datapoints (hours_studied, sleep_hours, performance_level) VALUES (?, ?, ?)",
            ('3', '7', '2')
            )

cur.execute("INSERT INTO datapoints (hours_studied, sleep_hours, performance_level) VALUES (?, ?, ?)",
            ('4', '8', '3')
            )

connection.commit()
connection.close()