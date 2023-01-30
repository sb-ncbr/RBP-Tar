import sqlite3
import time

connection = sqlite3.connect('../genes.db')
dest = sqlite3.connect(':memory:')

s = time.time()
# connection.backup(dest)
e = time.time()
print('backup, ', e - s)

s = time.time()
cur = connection.cursor()
cur.execute('SELECT * FROM genes WHERE start > 152011 limit 10000 offset 50')
print(len(cur.fetchall()))
e = time.time()
print('file, ', e - s)


# s = time.time()
# cur = dest.cursor()
# cur.execute('SELECT * FROM genes WHERE start > 152011 limit 10000 offset  50')
# cur.fetchall()
# e = time.time()
# print('mem, ', e - s)


