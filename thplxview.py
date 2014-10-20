import psycopg2
import pylab
import matplotlib
import math
import numpy as np
import datetime

maxtemp = 150
chamberindex = 0 #0= Oven, 3 = MOT Chamber, 0 = Magellan]
# STARTDATETIME = datetime.datetime(2014,7,16,15,5)
STARTDATETIME = datetime.datetime(2014,7,1,18)
# FINISHDATETIME = datetime.datetime(2013, 8, 10, 6)

matplotlib.rcParams['axes.color_cycle'] = ['b', 'g', 'r', 'c', 'm', 'y', 'k','(1,1,0)','(1,0,.8)','(0,0.5,0.5)','(0.5,0,0)','(0.7,0.7,0.7)','(0.1,0.9,0.1)']

class ThermoplexerView():

    def __init__(self,bakedbname):
        self.bakedbname = bakedbname
		       			
    def plot_all_TCs(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        cur.execute("SELECT sensors.name FROM sensors WHERE sensors.fault=FALSE and sensors.unit='C';")
        sensors = cur.fetchall()
        
       
        databysensors = dict()
        notesbysensors=dict()
        for sensor in sensors:
            sensorname = sensor[0]
            query = "SELECT %s.time, %s.value FROM %s, sensors WHERE %s.sensorid = sensors.id and sensors.name = %%s and %s.value < 1000 and sensors.unit='C' and %s.time > %%s;"%(self.bakedbname, self.bakedbname, self.bakedbname, self.bakedbname, self.bakedbname,self.bakedbname)
            #print(query)
            annotate_query = "SELECT annotations.note, annotations.time, annotations.pressure FROM annotations, sensors WHERE sensors.name = %s and annotations.sensorid=sensors.id"
            cur.execute(query, (sensorname, STARTDATETIME))
            databysensors[sensorname]=cur.fetchall()
            cur.execute(annotate_query, (sensorname,))
            notesbysensors[sensorname]=cur.fetchall()
        print notesbysensors
        cur.close()
        conn.close()
        
        

        fig = pylab.figure(figsize = (12,6))
        self.ax1 = fig.add_subplot(111)
        # self.ax1.clear()
        
        for sensor in sensors:
            x = [data[0] for data in databysensors[sensor[0]]]
            y = [data[1] for data in databysensors[sensor[0]]]
            self.ax1.plot_date(x, y, '-', label = sensor[0])
            for annotation in notesbysensors[sensor[0]]:
                print(annotation)
                self.ax1.annotate(annotation[0], (annotation[1], annotation[2]), xytext=(-50, 30), textcoords='offset points',arrowprops=dict(arrowstyle="->"), bbox=dict(boxstyle="round", fc="0.8"))
        self.ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        self.ax1.legend(loc = 'upper left')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Temperature / C')
        # ax1.set_title('Bake Data')
        self.ax1.axhline(y = maxtemp, linewidth = 4, color = 'r')
        #fig.autofmt_xdate()
        
        # print(x)
        # if show:
        
        #FJ
        pylab.show()
        #
        
        # pylab.savefig('C://Users//Levlab//thermoplexerview.png')
        # return fig
        
    # def upload_to_wiki(self):
    def plot_all_pressures(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        cur.execute("SELECT sensors.name FROM sensors WHERE sensors.fault=FALSE and sensors.unit='Torr';")
        sensors = cur.fetchall()
        databysensors = dict()
        notesbysensors = dict()
        for sensor in sensors:
            sensorname = sensor[0]
            query = "SELECT pressures.time, pressures.value FROM pressures, sensors WHERE pressures.value > 0 and pressures.id = sensors.id and sensors.name = %s and sensors.unit='Torr' and pressures.time > %s;"
            #print(query)
            annotate_query = "SELECT annotations.note, annotations.time, annotations.pressure FROM annotations, sensors WHERE sensors.name = %s and annotations.sensorid=sensors.id"
            cur.execute(query, (sensorname, STARTDATETIME,))
            databysensors[sensorname]=cur.fetchall()
            cur.execute(annotate_query, (sensorname,))
            notesbysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()        
      
        fig = pylab.figure(figsize=(12,6))		
        ax1 = fig.add_subplot(121)
        ax1.set_yscale('log')
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
        ax1.set_ylabel('Pressure / Torr')
        # ax1.set_title('Bake Data')
        
        ax2 = fig.add_subplot(122)
        chamber=sensors[chamberindex]
        chambername=chamber[chamberindex]
        x = [data[0] for data in databysensors[chambername]]
        y = [data[1] for data in databysensors[chambername]]
        ax2.plot_date(x, y,'-', label = chambername)
        ax2.ticklabel_format(style='sci',scilimits=(0,0),axis='y')
        ax2.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        ax2.legend(loc = 'upper left')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Pressure / Torr')
        ax2.set_title('Bake Data')
        fig.autofmt_xdate()
        # print(x)
        # if show:
        wm = pylab.get_current_fig_manager()
        wm.window.wm_geometry("1920x1080+50+50")
        pylab.show()
        # return fig
    
    def plot_all_fields(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        cur.execute("SELECT sensors.name FROM sensors WHERE sensors.fault=FALSE and sensors.unit='G';")
        sensors = cur.fetchall()
        databysensors = dict()
        notesbysensors = dict()
        for sensor in sensors:
            sensorname = sensor[0]
            query = "SELECT bfields.time, bfields.value FROM bfields, sensors WHERE bfields.sensorid = sensors.id and sensors.name = %s and sensors.unit='G' and bfields.time > %s;"
            #print(query)
            annotate_query = "SELECT annotations.note, annotations.time, annotations.pressure FROM annotations, sensors WHERE sensors.name = %s and annotations.sensorid=sensors.id"
            cur.execute(query, (sensorname, STARTDATETIME,))
            databysensors[sensorname]=cur.fetchall()
            cur.execute(annotate_query, (sensorname,))
            notesbysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()
        
        fig = pylab.figure(figsize=(6,3))		
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
        # print(x)
        # if show:
        wm = pylab.get_current_fig_manager()
        wm.window.wm_geometry("1920x1080+50+50")
        pylab.show()
        
    def make_obj(self):
		self.fig = pylab.figure(figsize=(12,6))		
		self.ax1 = self.fig.add_subplot(111)
		return self.fig,self.ax1
        
    # def plot_TP(self):
        # fig=pylab.figure()
        # axt = self.plot_all_TCs(show=False)
        # axp = self.plot_all_pressures(show=False)
        # fig.add_subplot(211)
        # fig.axes.append(axt)
        # fig.add_subplot(212)
        # fig.axes.append(axp)
        # pylab.show()
        
    # def plot_figures(self,figures, nrows = 1, ncols=1):
        # """Plot a dictionary of figures.

        # Parameters
        # ----------
        # figures : <title, figure> dictionary
        # ncols : number of columns of subplots wanted in the display
        # nrows : number of rows of subplots wanted in the figure
        # """

        # fig, axeslist = matplotlib.pyplot.subplots(nrows=nrows, ncols=ncols)
        # for ind,title in zip(range(len(figures)), figures):
            # axeslist.ravel()[ind].imshow(figures[title], cmap=matplotlib.pyplot.gray())
            # axeslist.ravel()[ind].set_title(title)
            # axeslist.ravel()[ind].set_axis_off()
        # matplotlib.pyplot.tight_layout() # optional
            
if __name__ == "__main__":
    test = ThermoplexerView('data')
    test.plot_all_TCs()
    # test.plot_all_pressures()
    # test.plot_TP()
    # test.plot_figures({'Temperatures':test.plot_all_TCs(), 'Pressures':test.plot_all_pressures()}, 2, 1)
