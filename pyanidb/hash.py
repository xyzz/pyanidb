import multihash, threading, time, os
try:
	import xattr
except ImportError:
	xattr = None

class File:
	def __init__(self, name, algorithms, cache):
		self.name = name
		self.size = os.path.getsize(name)
		self.mtime = os.path.getmtime(name)
		self.cached = False
		if cache:
			self.read_cache()
		if sum([not hasattr(self, a) for a in algorithms]):
			self.cached = False
			h = multihash.hash_file(name, algorithms)
			for a in algorithms:
				setattr(self, a, getattr(h, a)())
			self.write_cache()
	
	def read_cache(self):
		cache = dict([(n[13:], xattr.getxattr(self.name, n)) for n in xattr.listxattr(self.name) if n.startswith('user.pyanidb.')])
		if 'mtime' not in cache or str(int(self.mtime)) != cache.pop('mtime'):
			return
		for n, v in cache.iteritems():
			setattr(self, n, v)
		self.cached = True
	
	def write_cache(self):
		try:
			xattr.setxattr(self.name, 'user.pyanidb.mtime', str(int(self.mtime)))
			for n in ('ed2k', 'md5', 'sha1', 'crc32'):
				if hasattr(self, n):
					xattr.setxattr(self.name, 'user.pyanidb.' + n, getattr(self, n))
		except IOError:
			pass

class Hashthread(threading.Thread):
	def __init__(self, filelist, hashlist, algorithms, cache, *args, **kwargs):
		self.filelist = filelist
		self.hashlist = hashlist
		self.algorithms = algorithms
		self.cache = cache
		threading.Thread.__init__(self, *args, **kwargs)
	def run(self):
		try:
			while 1:
				f = self.filelist.pop(0)
				self.hashlist.append(File(f, self.algorithms, self.cache))
		except IndexError:
			return

def hash_files(files, cache = False, num_threads = 1, algorithms = ('ed2k',)):
	hashlist = []
	threads = []
	for x in xrange(num_threads):
		thread = Hashthread(files, hashlist, algorithms, cache)
		thread.start()
		threads.append(thread)
	while hashlist or sum([thread.isAlive() for thread in threads]):
		try:
			yield hashlist.pop(0)
		except IndexError:
			time.sleep(0.1)
	raise StopIteration
