import gpio_setup, time
import BBIO.GPIO as GPIO
from spi import SPI
import logging
#import cpickle
import datetime
#import matplotlib.pyplot as plt
import smtplib

logging.basicConfig(format='%(levelname)s:%(message)s', level = 
logging.WARNING)

CONNECTSTR = "dbname=will user=levlab host=levlabserver2.stanford.edu"

class Thermoplexer():
    def __init__(self, dbname, maxtemp = 200):
        # self.logfilename = logfilename
        self.tempreader = SPI(1,0)
        self.tempreader.msh = 1000000
        self.dbname = dbname
        self.maxtemp = maxtemp
        # self.init_log()
        
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
            print("TC # %d:"%num)
            temp = self.read_temp(num)
            if temp > 1000: #presumably thermocouple is railing
               logging.warning('TC %d Failure'%num)
            else:
                print("%2.0f C"%temp)
            time.sleep(0.5)
            
    def save_temps(self):
        conn = psycopg2.connect("dbname=will user=levlab host=levlabserver2.stanford.edu")
        cur = conn.cursor()
        for TCnum in self.TCnums:
            now = datetime.datetime.now()
            temp = self.read_temp(TCnum)
            self.check_overheat(temp)
            cur.execute("INSERT INTO data VALUES (%s, %s, %s);",(TCnum, timestamp, temp))
            time.sleep(0.5)
        conn.commit()
        cur.close()
        conn.close()
        
    def check_overheat(self, temp):
        if temp > self.maxtemp and temp <= 1000: #overheat condition
            conn = psycopg2.connect(CONNECTSTR)
            cur = conn.cursor()
            cur.execute("SELECT sensor.fault FROM sensors WHERE sensor.id = %s;",tcnum)
            faultbit = cur.fetchall()
            if faultbit == 0:
                cur.execute("UPDATE sensors SET fault = 1 WHERE sensor.id = %s;",tcnum)
                logging.warning('TC %d OVERHEATED!'%num)
                conn.commit()
                # self.email_warning()
            cur.close()
            conn.close()
        elif temp > 1000: #presumably thermocouple is railing
            conn = psycopg2.connect(CONNECTSTR)
            cur = conn.cursor()
            cur.execute("SELECT sensor.fault FROM sensors WHERE sensor.id = %s;",tcnum)
            faultbit = cur.fetchall()
            if faultbit == 0:
                cur.execute("UPDATE sensors SET fault = 1 WHERE sensor.id = %s;",tcnum)
                logging.warning('TC %d Failure'%num)
                conn.commit()
            cur.close()
            conn.close()
            
    def email_warning(self, tcname, temp):
        sender = 'thermoplexer@stanford.edu'
        receivers = ['rwturner@stanford.edu']
        
        message = '''From: From Thermoplexer <thermoplexer@stanford.edu>
        To: To Human <ACM>
        Subject: Overheating Warning!!
        
        The thermocouple labeled '%s' has reached a temperature of %d!
        
        The maximum acceptable temperature is %d.
        
        Love,
        Thermoplexer
        '''%(tcname, temp, self.maxtemp)
        
        try:
           smtpObj = smtplib.SMTP('smtp.stanford.edu', 25)
           smtpObj.starttls()
           smtpObj.sendmail(sender, receivers, message)         
           print("Successfully sent email")
        except SMTPException:
           print("Error: unable to send email")
        smtpObj.quit()
        
                
            
    
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

if __name__ == "__main__":
    dbname = 'data'
    # import thplxview
    thplx = Thermoplexer(dbname)
    # thplx.save_temps()
    thplx.email_warning('testtc', 230)
    # viewer = thplxview.ThermoplexerViewer(dbname)
    # viewer.plot_all_TCs()