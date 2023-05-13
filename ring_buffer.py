# From: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s19.html
class RingBuffer:
	"""
	A class that implements a ring buffer. This outer class handles the case when the buffer is not yet full!
	"""

	def __init__(self, size_max):
		"""
		Initialize the RingBuffer with a maximum size.

		Args:
			size_max (int): Maximum size of the buffer.
		"""
		self.max = size_max
		self.data = []

	class __Full:
		"""
		A class that implements a full buffer.
		"""

		def append(self, x):
			"""
			Append an element overwriting the oldest one.

			Args:
				x (Any): The element to be appended.
			"""
			self.data[self.cur] = x
			self.cur = (self.cur + 1) % self.max

		def get(self):
			"""
			Return a list of elements in correct order.
			"""
			return self.data[self.cur:] + self.data[:self.cur]

		def __iter__(self):
			"""
			Iterate over the elements in the buffer.
			"""
			yield from self.get()

		def __len__(self):
			"""
			Return the number of elements in the buffer.
			"""
			return self.max

		def __getitem__(self, key):
			"""
			Return the element at the given index.

			Args:
				key (int): Index of the element to be returned.

			Returns:
				Any: The element at the given index.
			"""
			return self.get()[key]

		def __setitem__(self, key, value):
			"""
			Set the value of the element at the given index.

			Args:
				key (int): Index of the element to be set.
				value (Any): The new value to be set.
			"""
			self.get()[key] = value

		def __reversed__(self):
			"""
			Return a new RingBuffer with the elements in reversed order.
			"""
			new = RingBuffer(self.max)
			for item in reversed(self.get()):
				new.append(item)
			return new

		def __contains__(self, item):
			"""
			Check if the buffer contains the given item.

			Args:
				item (Any): The item to be checked.

			Returns:
				bool: True if the item is in the buffer, False otherwise.
			"""
			return item in self.get()

	def append(self, x):
		"""
		Append an element at the end of the buffer.

		Args:
			x (Any): The element to be appended.
		"""
		self.data.append(x)
		if len(self.data) == self.max:
			self.cur = 0
			self.__class__ = self.__Full

	def get(self):
		"""
		Return a list of elements from the oldest to the newest.
		"""
		return self.data

	def __iter__(self):
		"""
		Iterate over the elements in the buffer.
		"""
		yield from self.get()

	def __len__(self):
		"""
		Return the number of elements in the buffer.
		"""
		return len(self.get())

	def __getitem__(self, key):
		"""
		Return the element at the given index.

		Args:
			key (int): Index of the element to be returned.

		Returns:
			Any: The element at the given index.
		"""
		return self.get()[key]

	def __setitem__(self, key, value):
			"""
			Set the value of the element at the given index.

			Args:
				key (int): Index of the element to be set.
				value (Any): The new value to be set.
			"""
			self.get()[key] = value

	def __reversed__(self):
		"""
		Return a new RingBuffer with the elements in reversed order.
		"""
		new = RingBuffer(self.max)
		for item in reversed(self.get()):
			new.append(item)
		return new

	def __contains__(self, item):
		"""
		Check if the buffer contains the given item.

		Args:
			item (Any): The item to be checked.

		Returns:
			bool: True if the item is in the buffer, False otherwise.
		"""
		return item in self.get()
