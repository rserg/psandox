import ctypes, subprocess
import heapq
import tempfile
import random
import string
import collections
import logging
import os
import shutil
import threading
import ctypes
import sys
import __builtin__
import io
import subprocess
import traceback
import StringIO #in 3.2 to io.StringIO
from sanderror import SandError
from itertools import izip
from protoconfig import *
from StringIO import StringIO
try:
	import simplejson as json
except Exception, e:
	import json


#TODO Thread support

#Check time of run
class CheckTime(threading.Thread):
	def __init__(self,**config):
		threading.Thread.__init__(self)
		self.config = config
		self.timout = config.get('timout',2)
		self.out = config.get('stdout', subprocess.PIPE)

	def run(self):
		 self.process = subprocess.Popen(["python", self.config.get('filename')],\
		 bufsize=1024,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
		 self.process.wait()

	def Pstart(self):
		self.start()
		self.join(self.timout)
		if self.is_alive:
			self.process.kill()



class FuncThread(threading.Thread):
	def __init__(self,func, **config):
		self.func = func
		threading.Thread.__init__(self)
		self.stop = threading.Event()
		self.timout = 2

	def run(self):
		print self.func
		exec self.func

	def fstart(self):
		self.start()
		self.join(self.timout)
		if self.isAlive:
			try:
				self._Thread__stop()
			except Exception, e:
				print "Another thread has blocked"
			#self._Thread__stop()
			#raise SandError("Another thread has blocked")

class NotAllowdMethod(Exception):
	pass
class ISandbox:
	def __init__(self, regime,**kwargs):
		pass

	def allow(self):pass
	def disallow(self):pass
	def start(self, command):
		pass


from sets import Set

#Main class for set settings
class Settings:
	def __init__(self, **kwargs):
		self.configs = kwargs

	def get_stack_size(self):
		return self.configs.get('stack_size',1000)

	def get_argcount(self):
		return self.configs.get('argcount',100)

'''Custum ssetings of allow method on librarys'''
class ConfigAllowFunctions:
	def __init__(self, librs):
		self.librs = librs
		#json.dumps([librs, {'allow': {'json', 'becks'}}])

	def config(self,cfg):
		s = json.dumps(['a', {'allow': ('json', 'becks')}])
		return s


#exec code
class CodeSandbox(ISandbox):
	def __init__(self,name,**kwargs):
		ISandbox.__init__(self,name)
		self.kwargs = kwargs
		self.code = name
		self.config = ProtoConfig(kwargs)

	def start(self):
		try:
			i = __builtin__.__import__
			sys.stdout = self.stdout()
			__builtin__.__import__ = self.config.config_import
			exec self.code
			__builtin__.__import__ = i
			sys.stdout = sys.__stdout__
		except SandError, e:
			print 'Error in sandbox'
		except Exception, e:
			raise e

	def stdout(self):
		if self.kwargs.get('stdout', False) == False:
			return StringIO()
		else:
			return sys.__stdout__

#Main Sandbox function
class Sandbox(ISandbox):
	def __init__(self,code,name=None,**kwargs):
		ISandbox.__init__(self,name)
		self.code = code
		global_array.append(name)
		'''self.kwargs = kwargs
		self.timeout = kwargs.get('timeout')
		self.code_length = kwargs.get('code_length')
		self.block_output = kwargs.get('block_output')'''
		'''assert self.code_length > len(code) and self.code != None, \
		"Length of code is more then;.."'''

		# allow exceptions
		self.exception = kwargs.get('aexception')
		self.sandbox = None
		if name == None:
			self._name = ''.join(random.choice(string.letters) for i in range(5))

		if(hasattr(code, '__call__')):
			self.sandbox = FunctionSandbox(code, **kwargs)

		elif os.path.isfile(code):
			self.sandbox = FileSandbox(code,kwargs)
		else:
			self.sandbox = CodeSandbox(code,**kwargs)
		self._name = name

	def start(self):
		self.sandbox.start()
		#self.config.execc(self.code)

	def get_name(self):
		return self._name

	#for files and byte code
	def load(self):pass



    #Compare of results of processing
	def __cmp__(self):
		pass


#Function Sandbox config
class FunctionSandboxConfig:
	def __init__(self, kwargs):
		self.configs = kwargs


	def cmp(self, func):
		#print func.co_argcount < self.get_argcount()
		#print func.co_stacksize < self.get_stack_size()
		return (func.co_argcount < self.get_argcount()and \
		func.co_stacksize < self.get_stack_size())

	def get_stack_size(self):
		return self.configs.get('stack_size',1000)

    #Numbers of function arguments
	def get_argcount(self):
		return self.configs.get('argcount',100)

	def get_black_List(self):
		return self.configs.get('black_list')

	def stdout(self):
		if self.configs.get('stdout', False) == False:
			return StringIO()
		else:
			return sys.__stdout__

#Sandbox for function
class FunctionSandbox(ISandbox):
	def __init__(self,funcname,**kwargs):
		self.func = funcname
		ISandbox.__init__(self,funcname, **kwargs)
		self.config = FunctionSandboxConfig(kwargs)	


	def __call__(self,func):
		self.func = func
		def wrap(*args,**kwargs):
			self.start()
		return wrap

	def start(self):
		temp = __builtin__.__import__
		tempeval = __builtin__.eval
		try:
			__builtin__.eval = None
			__builtin__.open = None
			sys.stdout = self.config.stdout()
			if self.config.cmp(self.func.func_code):
				ff = FuncThread(self.func.func_code)
				ff.fstart() #Exception in thread Thread-1!
		except Exception, e:
			print 'Block'
		except NoneType, e:
			print "Eval has blocked"
		finally:
			pass

		__builtin__.__import__ = temp
		sys.stdout = sys.__stdout__
		__builtin__.eval = tempeval


'''FileSandbox Kingdom'''

class FileSandboxConfig(ProtoConfig):
	def __init__(self, func, kwargs):
		ProtoConfig.__init__(self,kwargs)
		self.kwargs = kwargs
		self.func = func

	def cmp(self):
		return len(self.func) < self.get_file_size()
	def get_file_size(self):
		return self.kwargs.get('file_size', 10000)
	def timeout(self):
		return self.kwargs.get('timeout',2)

	def get_default_config(self,filename):
		return ('["python", %s],  shell=False \
				close_fds=False, bufsize=1024, stdin=subprocess.PIPE, stdout=subprocess.PIPE')\
		%filename


#Load code from file
class FileSandbox(ISandbox):
	def __init__(self,name,**kwargs):
		self.data = None
		self.filename = name
		self.kwargs = kwargs
		#log event
		self.savemap = sdt.SafeMap()
		ISandbox.__init__(self,name, **kwargs)
		try:
			self.data = open(name).readlines()
			#Size
		except Exception, e:
			print 'File not found'

		self.config = FileSandboxConfig(self.data, kwargs)

	def data(self):
		return ''.join(self.data)

	def allow(self):
		return self.config.allow()

	def output(self):
		return self.kwargs.get('output',True)

	def start(self):
		#block import
		if self.config.cmp():
			i = __builtin__.__import__
			__builtin__.__import__ =self.config.config_import
			print self.config.get_default_config(self.filename)
			sys.stdout = self.output()
			CheckTime(bufsize=1024, stdout=subprocess.PIPE, filename=self.filename).Pstart()
			self.savemap.add({self.filename:True},"P")
			sys.stdout = sys.__stdout__
			__builtin__.__import__ = i
		else:
			print "Can't load this file"
			self.savemap.add({self.filename:False},"I")

	def __str__(self):
		return self.config.status()



'''Safty open file'''
class FileWork:
	def __init__(self, filename, new_dir=None, black=[]):
		self.filename = filename
		if new_dir != None:   #Copy to safe folder unit test
			shutil.copy2(filename, new_dir)

		file = open(new_dir,'r')
		file.readlines().split('\n')

#Stack with read-only interface
class SaveStack:
	def __init__(self, elems):
		self.elems = elems
		self._stack = list()

	def push(self, obj):
		self.append(obj)

	def pop(self):
		ErrorWithSave("Save Struct does not profive pop() ")

	def __len__(self):
		return len(self._stack)