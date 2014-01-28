import psycopg2
import pylab
import matplotlib
import math
import numpy as np
import datetime
import time
import csv

STARTDATETIME = datetime.datetime(2013,8,8,16,15)
ENDDATETIME = datetime.datetime.now()
STARTDATEPOSIX = time.mktime(STARTDATETIME.timetuple())

conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
cur = conn.cursor()
cur.execute("SELECT sensors.name FROM sensors WHERE sensors.fault=FALSE and sensors.unit='Torr';")
sensors = cur.fetchall()
databysensors = dict()
notesbysensors = dict()
for sensor in sensors:
    sensorname = sensor[0]
    query = "SELECT pressures.time, pressures.value FROM pressures, sensors WHERE pressures.id = sensors.id and sensors.name = %s and sensors.unit='Torr' and pressures.time > %s and pressures.time < %s;"
    #print(query)
    annotate_query = "SELECT annotations.note, annotations.time, annotations.pressure FROM annotations, sensors WHERE sensors.name = %s and annotations.sensorid=sensors.id"
    cur.execute(query, (sensorname, STARTDATETIME, ENDDATETIME,))
    databysensors[sensorname]=cur.fetchall()
    cur.execute(annotate_query, (sensorname,))
    notesbysensors[sensorname]=cur.fetchall()
cur.close()
conn.close()

fig = pylab.figure(figsize=(12,6))		
ax1 = fig.add_subplot(111)
# ax1.set_yscale('log')
# ax1.set_xscale('log')
for sensor in sensors:
    x = [time.mktime(data[0].timetuple()) - STARTDATEPOSIX for data in databysensors[sensor[0]]]
    y = [data[1] for data in databysensors[sensor[0]]]
    filename = 'C:\\Users\Levlab\\Documents\\GitHub\\Thermoplexer\%s.csv'%sensor[0]
    f = open(filename, 'w')
    writer = csv.writer(f)
    writer.writerow(x)
    writer.writerow(y)
    ax1.plot(x, y,'-', label = sensor[0])
    for annotation in notesbysensors[sensor[0]]:
        print(annotation)
        # ax1.annotate(annotation[0], (annotation[1], annotation[2]), xytext=(-50, 30), textcoords='offset points',arrowprops=dict(arrowstyle="->"), bbox=dict(boxstyle="round", fc="0.8"))
ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
ax1.legend(loc = 'lower left')
ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure / Torr')
# ax1.set_title('Bake Data')

pylab.show()