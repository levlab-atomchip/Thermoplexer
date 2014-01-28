import psycopg2
import datetime

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
cur = conn.cursor()

annotations = [
(9,
'Start Bake',
datetime.datetime(2013, 8, 3, 12),
8e-6),
(9,
'Hot',
datetime.datetime(2013, 8, 3, 20,30),
9e-6),
(9,
'Flash Ion Pump',
datetime.datetime(2013, 8, 5, 9, 15),
1e-5),
(9,
'Degas Filament 1',
datetime.datetime(2013,8,5,9,30),
1e-6),
(9,
'Degas Filament 2',
datetime.datetime(2013,8,5,9,45),
5e-7),
(9,
'Condition NEG',
datetime.datetime(2013, 8, 5, 10),
4e-5),
# (9,
# 'End Conditioning',
# datetime.datetime(2013,8,5,11),
# 2e-7),
(9,
'Cool Down',
datetime.datetime(2013,8,5,13),
2e-7),
(9,
'Degas Ti Sub',
datetime.datetime(2013,8,5,14),
7e-6),
(9,
'Activate NEG, VAT closed',
datetime.datetime(2013,8,6,0),
4e-6),
# (9,
# 'NEG on, VAT closed, Ion Off',
# datetime.datetime(2013,8,6,5),
# 2.5e-8),
(9,
'Ion On',
datetime.datetime(2013,8,6,9,45),
2.5e-8),
(9,
'VAT Opened',
datetime.datetime(2013,8,6,10,15),
7.6e-10),
(9,
'Ion Off, VAT Open, Activate NEG',
datetime.datetime(2013,8,6,12,50),
2.4e-6),
(9,
'Ion On',
datetime.datetime(2013,8,6,13,45),
3.6e-9),
(9,
'Activate Ti Sub',
datetime.datetime(2013,8,6,17,5),
1e-6)
]

for annotation in annotations:
    cur.execute("INSERT INTO annotations VALUES (%s, %s, %s, %s);",(annotation[0],annotation[1],annotation[2], annotation[3]))

conn.commit()
cur.close()
conn.close()