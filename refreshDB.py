import sqlite3
import datetime
import pytz

con = sqlite3.connect('./score_record.db')
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS ReactRecord")
cur.execute("DROP TABLE IF EXISTS RememRecord")
cur.execute("DROP TABLE IF EXISTS AvoidRecord")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS ReactRecord(Name text, ReactionTime real, doDate text);")
cur.execute("CREATE TABLE IF NOT EXISTS RememRecord(Name text, CorrectPercent real, doDate text);")
cur.execute("CREATE TABLE IF NOT EXISTS AvoidRecord(Name text, Score integer, doDate text);")

kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")

cur.execute("INSERT INTO ReactRecord Values('Avg', 0.60724, ?)", (now_kst,))
cur.execute("INSERT INTO RememRecord Values('Avg', 90.457, ?)", (now_kst,))
cur.execute("INSERT INTO AvoidRecord Values('Avg', '3170', ?)", (now_kst,))
con.commit()

cur.execute('Select * From ReactRecord')
for row in cur:
    print(row)

cur.execute('Select * From RememRecord')
for row in cur:
    print(row)

cur.execute('Select * From AvoidRecord')
for row in cur:
    print(row)