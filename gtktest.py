#!/usr/bin/python3
from gi.repository import Gtk, GdkPixbuf
import struct, identicon

def get_pixbuf(data, w, h):
	return GdkPixbuf.Pixbuf.new_from_inline(struct.pack('>4s5L',
		b'GdkP', 24 + len(data), 0x1010001, len(data)//h, w, h) + data, True)

win = Gtk.Window()
win.connect('destroy', Gtk.main_quit)
win.set_default_size(640, 480)

m = Gtk.ListStore(GdkPixbuf.Pixbuf)
with open('/dev/urandom','rb') as f:
	for i in range(256):
		sz, data = identicon.make_rgb(f.read(17), 8, 2)
		m.append((get_pixbuf(data, sz, sz),))

iv = Gtk.IconView()
iv.set_pixbuf_column(0)
iv.set_model(m)

scroll = Gtk.ScrolledWindow()
scroll.add(iv)
win.add(scroll)

win.show_all()
Gtk.main()

