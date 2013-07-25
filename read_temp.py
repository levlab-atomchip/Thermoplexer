from spi import SPI

test = SPI(1,1)
test.msh = 1000000


def read_temp():
	out = test.readbytes(2)
	byte1 = '{0:08b}'.format(out[0])
	byte2 = '{0:08b}'.format(out[1])
	tempbits = byte1[1:] + byte2[:-3]
	return int(tempbits, 2)*0.25