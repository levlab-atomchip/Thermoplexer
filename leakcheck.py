import msvcrt
import pylab
import numpy
import matplotlib.pyplot as plt
import matplotlib
import xgs600
import thplxview
import time

#Enter the gauge number to watch
gauge=1

startTime=time.time()
#Initialize figure
plt.ion()
fig, = plt.plot([],[])
ax=plt.gca()

#Initialize pressure gauge
xgs=xgs600.XGS600Driver()

#Read pressures, then update plot dynamically, until ESC key is pressed.
while True:
    newdata=xgs.ReadPressure(gauge)
    #print newdata
    now=time.time()-startTime

    fig.set_xdata(numpy.append(fig.get_xdata(),now))
    fig.set_ydata(numpy.append(fig.get_ydata(),newdata))
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    # time.sleep(1)
    
    if msvcrt.kbhit():
	if ord(msvcrt.getch()) == 27:
	    break

xgs.f.close()