#started by RWT

#TODO: refactor the plot_all_* methods, too much duplicated code

import psycopg2
import pylab
import matplotlib
import math
import numpy as np
import datetime

# maxtemp = 150
# chamberindex = 0 #0= Oven, 3 = MOT Chamber, 2 = Magellan]
STARTDATETIME = datetime.datetime(2014,8,20,16,15)

THERMOCOUPLE_TABLE = 'sensors_ovenbake_august2014'
DATA_TABLE = 'data_ovenbake_august2014'
ANNOTATIONS_TABLE = 'annotations_8x_july2014'
GAUGE_TABLE = 'sensors_july2014'
PRESSURES_TABLE = 'pressures_july2014'
ADC_SENSOR_TABLE = 'sensors_ovenbake_august2014'

matplotlib.rcParams['axes.color_cycle'] = ['b', 'g', 'r', 'c', 'm', 'y', 'k','(1,1,0)','(1,0,.8)','(0,0.5,0.5)','(0.5,0,0)','(0.7,0.7,0.7)','(0.1,0.9,0.1)']

class ThermoplexerView():

    def __init__(self,bakedbname, showplot = False):
        self.bakedbname = bakedbname
        self.showplot = showplot
		       			
    def plot_all_TCs(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        sensor_query = '''SELECT {0}.name FROM {0} WHERE {0}.fault=FALSE and {0}.unit='C';'''.format(THERMOCOUPLE_TABLE)
        cur.execute(sensor_query)
        sensors = cur.fetchall()
        print sensors

        databysensors = dict()
        notesbysensors=dict()
        for sensor in sensors:
            sensorname = sensor[0]
            data_query = '''SELECT {0}.time, {0}.value FROM {0}, {1} WHERE {0}.sensorid = {1}.id and {1}.name = %s and {0}.value < 1000 and {1}.unit='C' and {0}.time > %s;'''.format(DATA_TABLE, THERMOCOUPLE_TABLE)
            cur.execute(data_query, (sensorname, STARTDATETIME))
            databysensors[sensorname]=cur.fetchall()
            notesbysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()

        fig = pylab.figure(1,figsize = (12,6))
        ax1 = fig.add_subplot(111)
        
        
        for sensor in sensors:
            x = [data[0] for data in databysensors[sensor[0]]]
            y = [data[1] for data in databysensors[sensor[0]]]
            ax1.plot_date(x, y, '-', label = sensor[0])
        ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        ax1.legend(loc = 'upper left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature / C')
        ax1.set_title('Oven Section Temperature Data, August 2014')
        fig.autofmt_xdate()
        wm = pylab.get_current_fig_manager()
        wm.window.state('zoomed')
        # pylab.show()
        
    def plot_all_pressures(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        sensor_query = '''SELECT {0}.name FROM {0} WHERE {0}.fault=FALSE and {0}.unit='Torr';'''.format(GAUGE_TABLE)
        cur.execute(sensor_query)
        sensors = cur.fetchall()
        databysensors = dict()
        notesbysensors = dict()
        for sensor in sensors:
            sensorname = sensor[0]
            data_query = '''SELECT {0}.time, {0}.value FROM {0}, {1} WHERE {0}.value > 0 and {0}.id = {1}.id and {1}.name = %s and {1}.unit='Torr' and {0}.time > %s;'''.format(PRESSURES_TABLE, GAUGE_TABLE)
            cur.execute(data_query, (sensorname, STARTDATETIME,))
            databysensors[sensorname]=cur.fetchall()
            notesbysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()        
      
        fig = pylab.figure(2,figsize=(12,6))		
        ax1 = fig.add_subplot(111)
        ax1.set_yscale('log')
        for sensor in sensors:
            x = [data[0] for data in databysensors[sensor[0]]]
            y = [data[1] for data in databysensors[sensor[0]]]
            ax1.plot_date(x, y,'-', label = sensor[0])
        ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        ax1.legend(loc = 'lower left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Pressure / Torr')
        
        fig.autofmt_xdate()
        
        wm = pylab.get_current_fig_manager()
        wm.window.state('zoomed')
        #pylab.show()

    
    def plot_all_other(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        sensor_query = '''SELECT {0}.name FROM {0} WHERE {0}.fault=FALSE and {0}.unit!='C';'''.format(ADC_SENSOR_TABLE)
        cur.execute(sensor_query)
        sensors = cur.fetchall()
        databysensors = dict()
        notesbysensors = dict()
        for sensor in sensors:
            sensorname = sensor[0]
            data_query = '''SELECT {0}.time, {0}.value FROM {0}, {1} WHERE {0}.value > 0 and {0}.sensorid = {1}.id and {1}.name = %s and {0}.time > %s;'''.format(DATA_TABLE, ADC_SENSOR_TABLE)
            cur.execute(data_query, (sensorname, STARTDATETIME,))
            databysensors[sensorname]=cur.fetchall()
            notesbysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()
        
        fig = pylab.figure(3,figsize=(6,3))		
        ax1 = fig.add_subplot(111)
        for sensor in sensors:
            x = [data[0] for data in databysensors[sensor[0]]]
            y = [data[1] for data in databysensors[sensor[0]]]
            ax1.plot_date(x, y,'-', label = sensor[0])
            for annotation in notesbysensors[sensor[0]]:
                print(annotation)
                ax1.annotate(annotation[0], (annotation[1], annotation[2]), xytext=(-50, 30), textcoords='offset points',arrowprops=dict(arrowstyle="->"), bbox=dict(boxstyle="round", fc="0.8"))
        ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        ax1.legend(loc = 'lower left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Field / G')
        

        fig.autofmt_xdate()
        wm = pylab.get_current_fig_manager()
        wm.window.state('zoomed')
        pylab.show()
            
if __name__ == "__main__":
    test = ThermoplexerView('data_july2014')
    test.plot_all_TCs()
    test.plot_all_pressures()
    test.plot_all_other()
    