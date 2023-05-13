# From: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s19.html
class RingBuffer:

	""" class that implements a not-yet-full buffer """
	def __init__(self,size_max):
		self.max = size_max
		self.data = []

	class __Full:
		""" class that implements a full buffer """
		def append(self, x):
			""" Append an element overwriting the oldest one. """
			self.data[self.cur] = x
			self.cur = (self.cur+1) % self.max

		def get(self):
			""" return list of elements in correct order """
			return self.data[self.cur:]+self.data[:self.cur]

		# Extra magic functions to make it work like other containers!

		# Suport iteration
		def __iter__(self):
			yield from self.get()

		# Support len
		def __len__(self):
			return len(self.get())
		
		# Support subscript retrieval
		def __getitem__(self, key):
			return self.get()[key]

		# Support subscript storage
		def __setitem__(self, key, value):
			#TODO: Do I need to handle out of bounds?
			self.get()[key] = value #TODO: Does this even work !?!?!

		# Support reverse
		def __reversed__(self): #TODO: Does this even work!??!?!
			new = RingBuffer()
			for item in reversed(self.get()):
				new.append(item)
			return new
			
		# Support in
		def __contains__(self, item):
			return item in self.get()

	def append(self,x):
		"""append an element at the end of the buffer"""
		self.data.append(x)
		if len(self.data) == self.max:
			self.cur = 0
			# Permanently change self's class from non-full to full
			self.__class__ = self.__Full

	def get(self):
		""" Return a list of elements from the oldest to the newest. """
		return self.data


	# Extra magic functions to make it work like other containers!

	# Suport iteration
	def __iter__(self):
		yield from self.get()

	# Support len
	def __len__(self):
		return len(self.get())
	
	# Support subscript retrieval
	def __getitem__(self, key):
		return self.get()[key]

	# Support subscript storage
	def __setitem__(self, key, value):
		#TODO: Do I need to handle out of bounds?
		self.get()[key] = value #TODO: Does this even work !?!?!

	# Support reverse
	def __reversed__(self): #TODO: Does this even work!??!?!
		new = RingBuffer()
		for item in reversed(self.get()):
			new.append(item)
		return new
		
	# Support in
	def __contains__(self, item):
		return item in self.get()

	