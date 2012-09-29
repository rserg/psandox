import ctypes, subprocess
import urllib
import heapq
import tempfile
import random
import string
import collections
import sys
import __builtin__
import StringIO
import pdb #tom look at debugging
from sanderror import SandError

#block_import - blocking all imported modules

#Configuration of white and black list
class ProtoConfig:
	def __init__(self, kwargs):
		#Configure black list
		self.black = ['urllib', 'urllib2', 'ssl', 'ctypes', 'os', 'eval', 'virtualenv',
		'thread', 'threading', 'multiprocessing'
			]
		self.kwargs = kwargs
		self.block_import = kwargs.get('block_import')
		self.cur_white = kwargs.get('white')
		print lambda x:x * cur_white
		self.black_list = kwargs.get('black')
		if self.black_list != None:
			self.add_black_all(self.black_list)

		'''assert self.cur_white == list and self.cur_black == list, \
		"Error in lists"'''

	#Show current config
	def __str__(self):
		return self.kwargs

	def config_import(self, a, s, d, f=[], g=-1):
		if "block_import" in self.kwargs:
			raise SandError("All modules are blocked")

		print self.black
		if a in self.black:
			raise SandError("module %s in the stop list" %a)

		return (a,s,d,f,g)

    #good module
	def allow(self, conf):
		if conf in self.black:
			self.black.remove(conf)
	def add_black(self, conf):
		self.black.append(conf)

	def add_black_all(self, black_list):
		if black_list != None:
			self.black += [lis for lis in black_list]
	def contains(self,lib):
		return lib in self.black

	def blocked(self):
		return self.black

	def check_module(modname):
		try:
			__builtin__.__import__(modname)
			return True
		except Exception, e:
			return False
    #Internet connection
	def net(self):
		pass

