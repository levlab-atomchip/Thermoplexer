import gpio_setup, time
import BBIO.GPIO as GPIO
from spi import SPI
import logging
import cpickle
import datetime
import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s', level = 
logging.WARNING)

class Thermoplexer():
    def __init__(self, logfilename):
        self.logfilename = logfilename
        self.tempreader = SPI(1,0)
        self.tempreader.msh = 1000000
        self.init_log()
        
    def choose_tc(self, num):
        if num > 8 or num < 1:
            logging.warning("invalid choice")
            return
        bits = "{0:03b}".format(num - 1)
        logging.debug('bits: %s'%bits)
        GPIO.output("P8_12", int(bits[0]))
        GPIO.output("P8_14", int(bits[1]))
        GPIO.output("P8_16", int(bits[2]))

    def read_temp(self, num):
        self.choose_tc(num)
        out = self.tempreader.readbytes(2)
        byte1 = '{0:08b}'.format(out[0])
        byte2 = '{0:08b}'.format(out[1])
        tempbits = byte1[1:] + byte2[:-3]
        return int(tempbits, 2)*0.25
    
    def read_all_tcs(self):
        for num in range(1,9):
            print "TC # %d:"%num
            temp = self.read_temp(num)
            if temp > 1000: #presumably thermocouple is railing
               logging.warning('TC %d Failure'%num)
            else:
                print "%2.0f C"%temp
            time.sleep(0.5)
            
    def save_temps(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
        cur = conn.cursor()
        for TCnum in self.TCnums:
            now = datetime.datetime.now()
            temp = self.read_temp(TCnum)
            cur.execute("INSERT INTO data VALUES (%s, %s, %s);",(TCnum, timestamp, temp))
            time.sleep(0.5)
        cur.close()
        conn.close()
    
# cPickle implementation is deprecated
#    def save_temps(self):
#        f = open(self.logfilename, 'w')
#        data = cpickle.load(f)
#        for i in range(1,9):
#            temp = self.read_temp(i)
#            now = datetime.datetime.now()
#            data[now] = [i, temp]
#            time.sleep(0.5)
#        cpickle.dump(data, f)
#        f.close()
#        
#    def init_log(self):
#        f = open(self.logfilename, 'w')
#        data = {}
#        cpickle.dump(data, f)
#        f.close()
#        
#    def plot_temp_log(self):
#        f = open(self.logfilename, 'r')
#        data = cpickle.load(f)
#        plt.plot_date(data.keys(), data.values(), xdate = True, ydate = False)