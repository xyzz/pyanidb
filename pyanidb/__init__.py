import socket, time

protover = 3
client = 'pyanidb'
clientver = 2

states = {
	'unknown': 0,
	'hdd': 1,
	'cd': 2,
	'deleted': 3,
	'shared': 4,
	'release': 5
}

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
		self.new_version = False
	def __del__(self):
		self.logout()
		self.sock.close()
	def execute(self, data):
		t = time.time()
		if t < self.lasttime + 2:
			time.sleep(self.lasttime + 2 - t)
		self.lasttime = time.time()
		self.sock.sendto(data + '\n', self.server)
		try:
			data = self.sock.recv(8192).split('\n')
		except socket.timeout:
			raise AniDBTimeout()
		code, text = data[0].split(' ', 1)
		data = data[1:-1]
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
			if code == 201:
				self.new_version = True
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
	def add_hash(self, size, ed2k, state = states['hdd'], viewed = False, source = '', storage = '', other = ''):
		while 1:
			code, text, data = self.execute('MYLISTADD s=%s&size=%d&ed2k=%s&state=%d&viewed=%d&source=%s&storage=%s&other=%s' % (self.session, size, ed2k, state, viewed and 1 or 0, source, storage, other))
			if code in [210, 310]:
				return
			elif code in [501, 506]:
				self.auth()
			elif code == 320:
				raise AniDBUnknownFile()
			else:
				raise AniDBReplyError(code, text)
