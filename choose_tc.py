def choose_tc(num):
	if num > 8 or num < 1:
		print "invalid choice"
		return
	bits = "{0:03b}".format(num - 1)
	GPIO.output("P8_12", int(bit[0]))
	GPIO.output("P8_14", int(bit[1]))
	GPIO.output("P8_16", int(bit[2]))
	return