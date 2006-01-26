from _hash import *

def file_hash(name):
	h = Hash()
	f = open(name)
	data = f.read(32768)	
	while data:
		h.update(data)
		data = f.read(32768)
	f.close()
	return h
