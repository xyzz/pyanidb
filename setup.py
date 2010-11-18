#!/usr/bin/env python

import os
from distutils.core import setup, Extension

setup(
	name = 'pyanidb',
	version = '0.2.1',
	author = 'Vegard Storheil Eriksen',
	author_email = 'zyp@jvnv.net',
	url = 'http://redmine.jvnv.net/projects/pyanidb/',
	packages = ['pyanidb'],
	scripts = ['anidb'])
