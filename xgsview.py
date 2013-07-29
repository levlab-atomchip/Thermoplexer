import thplxview
dbname = 'pressures'
viewer = thplxview.ThermoplexerView(dbname)
viewer.plot_all_pressures()