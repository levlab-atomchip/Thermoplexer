import psycopg2
import datetime

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
cur = conn.cursor()

annotations = [
(9,
'Conditioning Ion Pump',
datetime.datetime(2013, 7, 29, 14),
5e-5),
(9,
'Cool Down',
datetime.datetime(2013, 7, 30, 14),
5e-7),
(9,
'Activated Getter',
datetime.datetime(2013, 7, 30, 19, 30),
1e-5),
(9,
'Getter and Ion Pump On',
datetime.datetime(2013,7,31,2),
1e-8),
(9,
'Degas Ion Gauge',
datetime.datetime(2013,7,31,10),
1e-6),
(11,
'Resets of Ion Gauge',
datetime.datetime(2013, 7, 30, 17),
5e-10),
(6,
'Ion Gauge On',
datetime.datetime(2013,7,27,22),
80),
(6,
'?',
datetime.datetime(2013,7,28,6),
100),
(6,
'Gauge Foil Disturbed',
datetime.datetime(2013,7,29,14),
130),
(8,
'Improved Cryostat Wrapping',
datetime.datetime(2013,7,28,18),
100),
(5,
'Conditioned NexTorr',
datetime.datetime(2013,7,29,15,30),
170),
(5,
'Activated Getter',
datetime.datetime(2013,7,30,20),
130),
(2,
'Main Warmup',
datetime.datetime(2013,7,28,14),
80),
(2,
'Cool Down',
datetime.datetime(2013,7,30,17),
100)
]

for annotation in annotations:
    cur.execute("INSERT INTO annotations VALUES (%s, %s, %s, %s);",(annotation[0],annotation[1],annotation[2], annotation[3]))

conn.commit()
cur.close()
conn.close()