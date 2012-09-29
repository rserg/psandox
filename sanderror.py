class SandError(Exception):
	def __init__(self,message):
		Exception.__init__(self,"Error at the %s" % message)