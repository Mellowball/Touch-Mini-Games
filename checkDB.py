import sqlite3
import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

con = sqlite3.connect('./score_record.db')
cur = con.cursor()

print("Reaction Game Table")
cur.execute('Select * From ReactRecord')
for row in cur:
    print(row)

print("Remember Game Table")
cur.execute('Select * From RememRecord')
for row in cur:
    print(row)

print("Avoid Wall Game Table")
cur.execute('Select * From AvoidRecord')
for row in cur:
    print(row)