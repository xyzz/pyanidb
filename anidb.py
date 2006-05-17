#!/usr/bin/env python

import pyanidb, pyanidb.hash
import ConfigParser, optparse, os, sys, getpass, multihash

# Config.

config = {}
try:
	cp = ConfigParser.ConfigParser()
	cp.read(os.path.expanduser('~/.pyanidb.conf'))
	for option in cp.options('pyanidb'):
		config[option] = cp.get('pyanidb', option)
except:
	pass

# Options.

op = optparse.OptionParser()

op.add_option('-u', '--username', help = 'AniDB username.',
	action = 'store', dest = 'username', default = config.get('username'))
op.add_option('-p', '--password', help = 'AniDB password.',
	action = 'store', dest = 'password', default = config.get('password'))

op.add_option('-r', '--recursive', help = 'Recurse into directories.',
	action = 'store_true', dest = 'recursive', default = False)
op.add_option('-s', '--suffix', help = 'File suffix for recursive matching.',
	action = 'append', dest = 'suffix', default = config.get('suffix', '').split())

op.add_option('-i', '--identify', help = 'Identify files.',
	action = 'store_true', dest = 'identify', default = False)
op.add_option('-a', '--add', help = 'Add files to mylist.',
	action = 'store_true', dest = 'add', default = False)

options, args = op.parse_args(sys.argv[1:])

# Defaults.

options.login = options.add or options.identify

if options.login:
	if not options.username:
		options.username = raw_input('Username: ')
	if not options.password:
		options.passord = getpass.getpass()

# Input files.

files = []
for name in args:
	if not os.access(name, os.R_OK):
		print 'Invalid file: %s' % (name)
	elif os.path.isfile(name):
		files.append(name)
	elif os.path.isdir(name):
		if not options.recursive:
			print 'Is a directory: %s' % (name)
		else:
			for root, subdirs, subfiles in os.walk(name):
				subdirs.sort()
				subfiles.sort()
				files += [os.path.join(root, file) for file in subfiles if sum([file.endswith('.' + suffix) for suffix in options.suffix])]

if not files:
	print 'All operations finished.'
	sys.exit(0)

# Authorization.

if options.login:
	a = pyanidb.AniDB(options.username, options.password)
	try:
		a.auth()
		print 'Logged in as user %s.' % (options.username)
	except pyanidb.AniDBUserError:
		print 'Invalid username/password.'
		sys.exit(1)
	except pyanidb.AniDBTimeout:
		print 'Connection timed out.'
		sys.exit(1)
	except pyanidb.AniDBError, e:
		print 'Fatal error:', e
		sys.exit(1)

# Hashing.

for filename, hash in pyanidb.hash.hash_files(files):
	size = os.path.getsize(filename)
	print 'Hashed: ed2k://|file|%s|%d|%s|' % (filename, size, hash.ed2k())
	fid = (size, hash.ed2k())
	
	try:
		# Identify
		
		if options.identify:
			info = a.get_file(fid, ('gname', 'romaji', 'epno', 'epromaji'), True)
			fid = int(info['fid'])
			print '[%s] %s - %s - %s' % (info['gname'], info['romaji'], info['epno'], info['epromaji'])
		# Adding
		
		if options.add:
			a.add_file(fid, retry = True)
			print 'Added file: %s' % (filename)
		
	except pyanidb.AniDBUnknownFile:
		print 'Unknown file: %s' % (filename)

# Finished.

print 'All operations finished.'
