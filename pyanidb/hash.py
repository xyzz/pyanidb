import multihash, threading, time

class Hashthread(threading.Thread):
	def __init__(self, filelist, hashlist, algorithms, *args, **kwargs):
		self.filelist = filelist
		self.hashlist = hashlist
		self.algorithms = algorithms
		threading.Thread.__init__(self, *args, **kwargs)
	def run(self):
		try:
			while 1:
				f = self.filelist.pop(0)
				h = multihash.hash_file(f, self.algorithms)
				self.hashlist.append((f, h))
		except IndexError:
			return

def hash_files(files, num_threads = 1, algorithms = ('ed2k',)):
	hashlist = []
	threads = []
	for x in xrange(num_threads):
		thread = Hashthread(files, hashlist, algorithms)
		thread.start()
		threads.append(thread)
	while hashlist or sum([thread.isAlive() for thread in threads]):
		try:
			yield hashlist.pop(0)
		except IndexError:
			time.sleep(0.1)
	raise StopIteration
