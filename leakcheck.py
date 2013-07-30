import msvcrt
import pylab
import numpy
import matplotlib.pyplot as plt
import matplotlib
import xgs600
import thplxview
import time
import gtk

#gauge = raw_input("Enter gauge to watch: ")
gauge=1

startTime=time.time()

#Initialize figure
plt.ion()
fig, = plt.plot([],[])
#plt.draw()
ax=plt.gca()

#fig.set_xlabel('Time')
#fig.set_ylabel('Pressure / Torr')

#Initialize pressure gauge
xgs=xgs600.XGS600Driver()

#Read pressures constantly, then update plot dynamically, until ESC key is pressed.
olddata=[]
oldtime=[]
while True:
    newdata=xgs.ReadPressure(gauge)
    #print newdata
    now=time.time()-startTime
    #print fig.get_ydata()
    
    olddata.append(newdata)
    oldtime.append(now)
    fig.set_xdata(oldtime)
    fig.set_ydata(olddata)
    #print olddata
    fig.set_xdata(numpy.append(fig.get_xdata(),now))
    fig.set_ydata(numpy.append(fig.get_ydata(),newdata))
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    #time.sleep(1)
    
    #if msvcrt.kbhit():
	#if ord(msvcrt.getch()) == 27:
	#    break

xgs.f.close()