import psycopg2
import datetime

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
cur = conn.cursor()

annotations = [
(12,
'Switched from MOT gauge to test chamber gauge',
datetime.datetime(2013, 10, 21, 18, 15),
2e-10),
(12,
'Switched from test gauge to MOT chamber gauge',
datetime.datetime(2013, 10, 22, 16, 40),
2e-10)
]

for annotation in annotations:
    cur.execute("INSERT INTO annotations VALUES (%s, %s, %s, %s);",(annotation[0],annotation[1],annotation[2], annotation[3]))

conn.commit()
cur.close()
conn.close()