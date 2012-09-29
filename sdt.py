#Save data types

#Stack with read-only interface
#Or maybe i implement Set?
#Add atributes for settings stack
class SaveStack:
	def __init__(self, elems, **kwargs):
		self.elems = elems
		self._stack = list()
		self._allowpop = kwargs.get('pop')
		self._maxstack(kwargs.get('size'))

	def push(self, obj):
		self.append(obj)

    #Custum settings
	def pop(self):
		self._pop()

	def _pop(self):
		if self._allowpop:
			sel._stack.pop()
		else:
			ErrorWithSave("Save Struct does not profive pop() ")


	def __len__(self):
		return len(self._stack)


#List with read-only interface

#TODO some settings
class SafeMap:
	def __init__(self):
		self._map = list()

	def __contains__(self, key):
		return self._exists(key)

 	def __len__(self):
 		return len(self._map)
	def __iter__(self):
		BlockError("__iter__ not allowed in this case")
	def add(self,key,value):
		self._map.append(KeyValue(key, value))

	def remove(self, key):
		BlockError("Remove is bad")

	def __copy__(self, newMap):
		BlockError("__copy__ not exists")

    #exists key in map
	def _exists(self, key):
		return filter(lambda x: x.key == key, self._map) != []



#Class (or something calld this 'struct' for store key, value pair)

class KeyValue:
	def __init__(self, key, value):
		self.key = key
		self.value = value


#More complex about building Exceptions
def BlockError(message):
	raise NotAllowedException(message)
class NotAllowedException(Exception):
	def __init__(self,message):
		Exception.__init__(self, message)
