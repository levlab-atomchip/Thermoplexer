import psycopg2
import math
import numpy as np
import datetime
import scipy.optimize as optimize
import matplotlib.dates as pltdates
import matplotlib.pylab as plt

STARTDATETIME = datetime.datetime(2014,7,25,6,00)
P_FINAL = 7e-8
tau_guess = 2*24*60*60 # 2 days in seconds

THERMOCOUPLE_TABLE = 'thermocouples_8x'
DATA_TABLE = 'data_8x_july2014'
ANNOTATIONS_TABLE = 'annotations_8x_july2014'
GAUGE_TABLE = 'sensors_july2014'
PRESSURES_TABLE = 'pressures_july2014'


def exp_func(t, Af, A, tau):
    return Af + A*np.exp(-1*t/tau)


def fit_pressures(target_sensor):
    conn = psycopg2.connect("dbname=will user=levlab host=levlabserver.stanford.edu")
    cur = conn.cursor()
    sensor_query = '''SELECT {0}.name FROM {0} WHERE {0}.fault=FALSE and {0}.unit='Torr';'''.format(GAUGE_TABLE)
    cur.execute(sensor_query)
    sensors = cur.fetchall()
    databysensors = dict()
    notesbysensors = dict()
    for sensor in sensors:
        sensorname = sensor[0]
        data_query = '''SELECT {0}.time, {0}.value FROM {0}, {1} WHERE {0}.value > 0 and {0}.id = {1}.id and {1}.name = %s and {1}.unit='Torr' and {0}.time > %s;'''.format(PRESSURES_TABLE, GAUGE_TABLE)
        annotate_query = '''SELECT {0}.note, {0}.time, {0}.pressure FROM {0}, {1} WHERE {1}.name = %s and {0}.sensorid={1}.id'''.format(ANNOTATIONS_TABLE, GAUGE_TABLE)
        cur.execute(data_query, (sensorname, STARTDATETIME,))
        databysensors[sensorname]=cur.fetchall()
        cur.execute(annotate_query, (sensorname,))
        notesbysensors[sensorname]=cur.fetchall()
    cur.close()
    conn.close()

    time =  [data[0] for data in databysensors[target_sensor]]
    time_secs = np.array([(t - STARTDATETIME).total_seconds() for t in time])
    value = np.array([float(data[1]) for data in databysensors[target_sensor]])
    
    p0 = np.array([P_FINAL, value[0] - P_FINAL, tau_guess])
    
    popt, _ = optimize.curve_fit(exp_func, time_secs, value, p0)
    print popt
    
    fit_result = [exp_func(t, *popt) for t in time_secs]
    if P_FINAL > popt[0]:
        est_pumpdown = STARTDATETIME + datetime.timedelta(seconds = popt[2] * np.log(popt[1] / (P_FINAL - popt[0])))
        print est_pumpdown
    else:
        print 'Desired pressure is unreachable.'
        one_wk_from_now_secs = ((datetime.datetime.now() - STARTDATETIME) + datetime.timedelta(weeks=1)).total_seconds()
        print 'Pressure in one week is: %e'%(exp_func(one_wk_from_now_secs, *popt))
    

    
    fig = plt.figure(figsize=(12,6))		
    ax1 = fig.add_subplot(111)
    # ax1.set_yscale('log')
    ax1.plot_date(time, value,'-', label = sensor[0])
    ax1.plot_date(time, fit_result, '-', label='Fit Result')
    ax1.fmt_xdate = pltdates.DateFormatter('%H%M')
    ax1.legend(loc = 'lower left')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Pressure / Torr')
    fig.autofmt_xdate()
    wm = plt.get_current_fig_manager()
    wm.window.wm_geometry("1920x1080+50+50")
    plt.show()
    
if __name__ == '__main__':
    fit_pressures('Magellan')