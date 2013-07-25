import gpio_setup, time
import BBIO.GPIO as GPIO
from spi import SPI
import logging
import cpickle
import datetime

logging.basicConfig(format='%(levelname)s:%(message)s', level = 
logging.WARNING)

test = SPI(1,0)
test.msh = 1000000

def choose_tc(num):
	if num > 8 or num < 1:
		print "invalid choice"
		return
	bits = "{0:03b}".format(num - 1)
#        logging.debug('bits: %s'%bits)
	GPIO.output("P8_12", int(bits[0]))
	GPIO.output("P8_14", int(bits[1]))
	GPIO.output("P8_16", int(bits[2]))

def read_temp(num):
    choose_tc(num)
    out = test.readbytes(2)
    byte1 = '{0:08b}'.format(out[0])
    byte2 = '{0:08b}'.format(out[1])
    tempbits = byte1[1:] + byte2[:-3]
    return int(tempbits, 2)*0.25

def read_all_tcs():
    for num in range(1,9):
        print "TC # %d:"%num
        temp = read_temp(num)
        if temp > 1000: #presumably thermocouple is railing
            print 'Thermocouple Failure'
        else:
            print "%2.0f C"%temp
        time.sleep(0.5)

def save_temps(filename):
    f = open(filename, 'w')
    data = cpickle.load(f)
    for i in range(1,9):
        temp = read_temp(i)
        now = datetime.datetime.now()
        data[now] = [i, temp]
        time.sleep(0.5)
    cpickle.dump(data, f)
    f.close()
    
def init_log(filename):
    f = open(filename, 'w')
    data = {}
    cpickle.dump(data, f)
    f.close()