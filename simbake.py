import psycopg2
import random
import datetime
import math

n = 1000
TCnums = range(1,9)
max_temp = [random.uniform(150,200) for i in TCnums]
tau = [random.uniform(300,600) for i in TCnums]

def sim_temp(num, timestamp):
    minutes_passed = timestamp.hour * 60 + timestamp.minute
    temp = max_temp[num - 1] * ( 1 - math.exp(-1*minutes_passed / tau[num-1])) + 20 + round(random.normalvariate(0, 3))
    return temp

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
cur = conn.cursor()
for i in range(0,n):
    for TCnum in TCnums:
        now = datetime.datetime.today()
        now = now.replace(hour = random.randint(0,23), minute = random.randint(0,59))
        print(now)
        temp = sim_temp(TCnum, now)
        cur.execute("INSERT INTO data VALUES (%s, %s, %s);",(TCnum, now, temp))
        # time.sleep(0.5)
conn.commit()
cur.close()
conn.close()