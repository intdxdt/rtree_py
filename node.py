__author__ = 'titus'
from _mbr import empty


class Node(dict):
	"""
	BST - Node
	"""

	def __init__(self, **kw):
		dict.__init__(self, kw)
		self.__dict__ = self

		if not self.has_key('leaf'):
			self.leaf = False

		if not self.has_key('children'):
			self.children = []

		if not self.has_key('height'):
			self.height = 1

		if not self.has_key('bbox'):
			self.bbox = empty()

	def __getstate__(self):
		return self

	def __setstate__(self, state):
		self.update(state)
		self.__dict__ = self

	def __getattr__(self, item):
		# only gets called if key is missing
		if not self.__dict__.has_key(item):
			raise Exception("invalid attribute")
			# return getattr(self, item)

	def hasattr(self, attr):
		return self.__dict__.has_key(attr)

	@property
	def size(self):
		return len(self.children)
