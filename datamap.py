''''class DataMap:
	def __init__(self):
		self.m = Map()
	def __add__(self, num):
		pass'''

num_int = ['1','3']

new_int = [int(i) for i in num_int]

badd = [1,4,8,5,9,6,2]
print filter(lambda x: x % 2 == 0, badd)


def func1(param):
	def func2():
		print param()
	return func2


def rabona(func):
	return lambda:func()+1

@func1
@rabona
def testo():
	print 4

testo()