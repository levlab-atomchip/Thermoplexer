import BBIO.GPIO as GPIO
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_16", GPIO.OUT)

GPIO.output("P8_12", GPIO.HIGH)
GPIO.output("P8_14", GPIO.HIGH)
GPIO.output("P8_16", GPIO.HIGH)
