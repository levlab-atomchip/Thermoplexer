import psycopg2
import pylab
import matplotlib

maxtemp = 150

class ThermoplexerView():
    def __init__(self,bakedbname):
        self.bakedbname = bakedbname
		       			
    def plot_all_TCs(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
        cur = conn.cursor()
        cur.execute("SELECT sensors.name FROM sensors WHERE sensors.fault=FALSE;")
        sensors = cur.fetchall()
        databysensors = dict()
        for sensor in sensors:
            sensorname = sensor[0]
            query = "SELECT %s.time, %s.temperature FROM %s, sensors WHERE %s.sensorid = sensors.id and sensors.name = %%s and %s.temperature < 1000 ;"%(self.bakedbname, self.bakedbname, self.bakedbname, self.bakedbname, self.bakedbname)
            #print(query)
            cur.execute(query, (sensorname, ))
            databysensors[sensorname]=cur.fetchall()
        cur.close()
        conn.close()
        
        
        fig = pylab.figure(figsize = (8,6))
        ax1 = fig.add_subplot(111)
        for sensor in sensors:
            x = [data[0] for data in databysensors[sensor[0]]]
            y = [data[1] for data in databysensors[sensor[0]]]
            ax1.plot_date(x, y,'.', label = sensor[0])
        ax1.fmt_xdate = matplotlib.dates.DateFormatter('%H%M')
        ax1.legend(loc = 'upper left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature / C')
        ax1.set_title('Bake Data')
        ax1.axhline(y = maxtemp, linewidth = 4, color = 'r')
        fig.autofmt_xdate()
        # print(x)
        pylab.show()
        # pylab.savefig('C://Users//Levlab//thermoplexerview.png')
        
    # def upload_to_wiki(self):
        
            
if __name__ == "__main__":
    test = ThermoplexerView('data')
    test.plot_all_TCs()