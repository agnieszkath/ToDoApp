__author__ = 'Agnieszka'

import sqlite3

con = sqlite3.connect("mojabaza.db")

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS mbaza")
    cur.execute("CREATE TABLE mbaza(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER NOT NULL)")
    cur.execute('INSERT INTO mbaza (name, due_date, priority, status) VALUES("Prepare for exam", "10/06/2016", 10, 1)')
    cur.execute('INSERT INTO mbaza (name, due_date, priority, status) VALUES("Go to the cinema", "03/06/2016", 4, 1)')

con.close()