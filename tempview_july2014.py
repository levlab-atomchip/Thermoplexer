import thplxview_8x_july2014 as thplxview
dbname = 'pressures_july2014'
viewer = thplxview.ThermoplexerView(dbname, showplot = True)
viewer.plot_all_TCs()