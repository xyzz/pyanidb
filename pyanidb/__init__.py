import socket, time

protover = 3
client = 'pyanidb'
clientver = 0

states = {
	'unknown': 0,
	'hdd': 1,
	'cd': 2,
	'deleted': 3,
	'shared': 4,
	'release': 5}

fcode = (
	'', 'aid', 'eid', 'gid', 'lid', '', '', '',
	'state', 'size', 'ed2k', 'md5', 'sha1', 'crc32', '', '',
	'dublang', 'sublang', 'quality', 'source', 'acodec', 'abitrate', 'vcodec', 'vbitrate',
	'vres', 'filetype', 'length', 'description', '', '', '', '')

acode = (
	'gname', 'gtag', '', '', '', '', '', '',
	'epno', 'epname', 'epromaji', 'epkanji', '', '', '', '',
	'eptotal', 'eplast', 'year', 'type', 'romaji', 'kanji', 'english', 'other',
	'short', 'synonym', 'category', '', '', '', '', '')

info = fcode + acode
info = dict([(info[i], 1 << i) for i in xrange(len(info)) if info[i]])

class AniDBError(Exception):
	pass

class AniDBTimeout(AniDBError):
	pass

class AniDBLoginError(AniDBError):
	pass

class AniDBUserError(AniDBLoginError):
	pass

class AniDBReplyError(AniDBError):
	pass

class AniDBUnknownFile(AniDBError):
	pass

class AniDB:
	def __init__(self, username, password, localport = 1234, server = ('api.anidb.info', 9000)):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('0.0.0.0', localport))
		self.sock.settimeout(10)
		self.username = username.lower()
		self.password = password
		self.server = server
		self.session = ''
		self.lasttime = 0
	
	def __del__(self):
		self.logout()
		self.sock.close()
	
	def newver_msg(self):
		print 'New version available.'
	
	def retry_msg(self):
		print 'Connection timed out, retrying.'
	
	def execute(self, data, retry = False):
		while 1:
			t = time.time()
			if t < self.lasttime + 2:
				time.sleep(self.lasttime + 2 - t)
			self.lasttime = time.time()
			self.sock.sendto(data + '\n', self.server)
			try:
				data = self.sock.recv(8192).split('\n')
			except socket.timeout:
				if retry:
					self.retry_msg()
				else:
					raise AniDBTimeout()
			else:
				break
		code, text = data[0].split(' ', 1)
		data = [line.split('|') for line in data[1:-1]]
		code = int(code)
		return code, text, data
	
	def ping(self):
		t = time.time()
		try:
			return self.execute('PING')[0] == 300 and time.time() - t or None
		except AniDBTimeout:
			return None
	
	def auth(self):
		code, text, data = self.execute('AUTH user=%s&pass=%s&protover=%d&client=%s&clientver=%d' % (self.username, self.password, protover, client, clientver))
		if code in [200, 201]:
			self.session = text.split(' ', 1)[0]
			if code == 201 and clientver:
				self.newver_msg()
		elif code == 500:
			raise AniDBUserError()
		else:
			raise AniDBReplyError(code, text)
	
	def logout(self):
		if self.session:
			try:
				self.execute('LOGOUT s=%s' % (self.session))
				self.session = ''
			except AniDBError:
				pass
	
	def get_file(self, fid, info_codes, retry = False):
		try:
			fid = 'size=%d&ed2k=%s' % fid
		except TypeError:
			fid = 'fid=%d' % (fid)
		info_codes = list(info_codes)
		info_codes.sort(lambda x, y: cmp(info[x], info[y]))
		info_code = sum([info[code] for code in info_codes])
		code, text, data = self.execute('FILE s=%s&%s&fcode=%d&acode=%d' % (self.session, fid, info_code & 0xffffffff, info_code >> 32), retry)
		if code == 220:
			return dict([(name, data[0].pop(0)) for name in ['fid'] + info_codes])
		elif code == 320:
			raise AniDBUnknownFile()
		elif code in [501, 506]:
			self.auth()
		else:
			raise AniDBReplyError(code, text)
		return code, text, data
	
	def add_file(self, fid, state = 'hdd', viewed = False, source = '', storage = '', other = '', retry = False):
		try:
			fid = 'size=%d&ed2k=%s' % fid
		except TypeError:
			fid = 'fid=%d' % (fid)
		while 1:
			code, text, data = self.execute('MYLISTADD s=%s&%s&state=%d&viewed=%d&source=%s&storage=%s&other=%s' % (self.session, fid, states[state], viewed and 1 or 0, source, storage, other), retry)
			if code in [210, 310]:
				return
			elif code == 320:
				raise AniDBUnknownFile()
			elif code in [501, 506]:
				self.auth()
			else:
				raise AniDBReplyError(code, text)
