import psycopg2
import datetime

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
cur = conn.cursor()

time = datetime.datetime(2013, 7, 30)
text = 'test message'
cur.execute("INSERT INTO annotations VALUES (%s, %s, %s);",(3, text, time))

conn.commit()
cur.close()
conn.close()