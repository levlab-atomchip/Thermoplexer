import serial
import time
import datetime
import psycopg2

HONEYWELL_SENSORIDS = [13,14,15]

DEBUG = 0

class HMR2300Driver():

    def __init__(self):
    #Opens serial port on COM4. Use Device Manager to refresh port on first initialization.
        self.f = serial.Serial('COM5')

    def hmr_comm(self,command):
        comm = "*00" + command + "\r"

        self.f.write(comm)
        time.sleep(0.25)
        bytes = self.f.inWaiting()
        complete_string = self.f.read(bytes)
        #complete_string = complete_string.replace('>','').replace('\r','')
        return(complete_string)

    def readxyz(self):
        xyzstring = self.hmr_comm("P")
        if DEBUG:
            print xyzstring
        xyzstring = xyzstring.replace(',','').replace('\r','')
        if DEBUG:
            print xyzstring
        xyzstring = xyzstring.split()
        if DEBUG:
            print xyzstring
        for index, entry in enumerate(xyzstring):
            # this fixes a problem where minus signs have a space after them
            if entry == '-':
                xyzstring[index + 1] = '-' + xyzstring[index + 1]
                del xyzstring[index]


        xyz = []
        for x in xyzstring:
            if DEBUG:
                print x
                print float(x)
            xyz.append(float(x)/15000.0) #units in gauss

        return(xyz)

    def ReadSoftwareVersion(self):
        return(self.hmr_comm("F"))

    def ReadHardwareVersion(self):
        return(self.hmr_comm("H"))

    def save_xyz(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
        cur = conn.cursor()
        compass = self.readxyz()
        for dirindex, _ in enumerate(compass):
            now = datetime.datetime.now()
            cur.execute("INSERT INTO bfields VALUES (%s, %s, %s);",(HONEYWELL_SENSORIDS[dirindex], now, compass[dirindex]))
            time.sleep(0.1)
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    honeywell = HMR2300Driver()
    honeywell.save_xyz()
    # print str(honeywell.readxyz())
    honeywell.f.close()#important to close the connection otherwise next run will barf