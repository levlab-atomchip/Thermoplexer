import scipy
import pylab
import datetime
import psycopg2
import time

import thplxview
dbname = 'data'
viewer = thplxview.ThermoplexerView(dbname)
fig, ax = viewer.make_obj()

def update_title(JackAndXander):
    viewer.plot_all_TCs()
    fig.canvas.draw()
    fig.savefig('//levlabserver2.stanford.edu/levlabgroup/Experiments/Atomic Chip Microscopy/Logging/Temperature.png')
    
update_title(None)

# Create a new timer object. Set the interval 500 milliseconds (1000 is default)
# and tell the timer what function should be called.
timer = fig.canvas.new_timer(interval=60000)
timer.add_callback(update_title,ax)
timer.start()
pylab.show()