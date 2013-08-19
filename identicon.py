def transform(p, h, v, r):
	if v: p = reversed(p)
	if h: p = map(reversed, p)
	return tuple(zip(*p) if r else p)

def combine(mode, a, b):
	x = mode % 6
	return tuple(tuple(l)+tuple(m) for l,m in zip(a +
		transform(b, x > 1, x == 5, x > 3),
		transform(b, x == 4, x & 5, x > 3) +
		transform(a, x > 1, x & 5, False)))

SHAPES = (
	list(map(lambda z: lambda x,y,s: x+y>z*s, (4,7,8,10))) +
	list(map(lambda z: lambda x,y,s: x*y>z*s*s, (2,3,4,5,7,9,10,12,16))) +
	[lambda x,y,s: (x^y)%3==0, lambda x,y,s: (x^y)%3==1, lambda x,y,s: x+2*y>13*s])

def segment(n, shape, sz):
	f = SHAPES[shape % len(SHAPES)]
	return tuple(tuple(n+f(x,y,sz/8) for x in range(sz)) for y in range(sz))

def make_indexed(rnd, blocksz, iters):
	p = combine(rnd[2], *(segment(2*i, rnd[i], blocksz) for i in range(2)))
	for i in range(iters): p = combine(rnd[3+i], p, p)
	return p

def make_rgb(rnd, blocksz, iters):
	p = make_indexed(rnd[12:], blocksz, iters)
	colors = [rnd[3*i:3*i+3] for i in range(4)]
	return len(p), b''.join(colors[c] for l in p for c in l)

import struct, zlib
i32 = struct.Struct('>L').pack
def png_chunk(name, *data):
	yield i32(sum(map(len, data)))
	yield name
	yield from data
	crc = zlib.crc32(name)
	for d in data: crc = zlib.crc32(d, crc)
	yield i32(crc & 0xffffffff)
def make_png(rnd, blocksz, iters):
	p = make_indexed(rnd[12:], blocksz, iters)
	l = [b'\x89PNG\r\n\x1a\n']
	l.extend(png_chunk(b'IHDR', i32(len(p))*2, b'\x08\3\0\0\0'))
	l.extend(png_chunk(b'PLTE', rnd[:12]))
	l.extend(png_chunk(b'IDAT', zlib.compress(bytes(i for l in p for i in (0,)+l), 9)))
	l.extend(png_chunk(b'IEND'))
	return b''.join(l)

