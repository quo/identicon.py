#!/usr/bin/python3
import identicon

with open('/dev/urandom','rb') as rnd:
	for i in range(10):
		with open('test-%i.png' % i, 'wb') as f:
			f.write(identicon.make_png(rnd.read(17), 8, 2))

