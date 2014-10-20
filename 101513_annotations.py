import psycopg2
import datetime

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
cur = conn.cursor()

annotations = [
(12,
'Switched from test chamber to MOT gauge',
datetime.datetime(2013, 10, 15, 14, 30),
6e-11)
]

for annotation in annotations:
    cur.execute("INSERT INTO annotations VALUES (%s, %s, %s, %s);",(annotation[0],annotation[1],annotation[2], annotation[3]))

conn.commit()
cur.close()
conn.close()