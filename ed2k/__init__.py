from _ed2k import *

def file_hash(name):
	e = Ed2k()
	f = open(name)
	data = f.read(32768)	
	while data:
		e.update(data)
		data = f.read(32768)
	f.close()
	return e.digest()
