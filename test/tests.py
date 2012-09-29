from psandox import Sandbox

#http://tav.espians.com/a-challenge-to-break-python-security.html
def bind(f,v):return f(v) if f else None
def test():
	lis = ["one", "two", [i for i in range(10)]]
	return lambda x:x*5


def planeFileTest():
	f = FileSandbox('tests.py')
	f.start()

'''Another module testing'''

def testsdt():
	sv = SaveMap();
 	sv.add(4,5)
	sv.add("SS", 78)
	print sv.__contains__("SS")

def testFile(filename):
	#test default config
	f = FileSandbox(filename)
	f.start()

	#test block size
	f = FileSandbox(filename, file_size=10)
	f.start()

	#test block import

	f = FileSandbox(filename, black=["__builtin__", "io"])
	f.start()

	#test allow output
	f = FileSandbox(filename, output=False)
	f.start()

	f = FileSandbox(filename, black=["urllib", "logging"], output=False)
	f.start()

#test Sandbox for all
def sandbox_for_all(self):
	#as function
	f = Sandbox(test,"name")
	f.start("S")

from thread import start_new_thread
def absd(a):
	return a ** a

def test():
	import urllib
	start_new_thread(absd,(4,))
	ss = ["SSS", "next", "func"]

#test open file for write
def testopen(filename):
	with open(filename,'w') as f:
		f.write('testmessage')

def funcmessage():
	f = FunctionSandbox(testopen)
	f.start()


f = psandox.Sandbox(test)
f.start()
#info about 
'''s = sandbox.FunctionSandbox(test)
s.start()

s = sandbox.FunctionSandbox(test, stack_size=10)
s.start()

s = sandbox.FunctionSandbox(test, stack_size=1)
s.start()'''

