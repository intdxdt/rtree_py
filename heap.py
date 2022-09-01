from heapq import heappush as hpush, heappop as  hpop


class Heap(object):
	def __init__(self, data=()):
		self.items = []
		for o in data:
			self.push(o)

	def push(self, o):
		hpush(self.items, o)

	def pop(self):
		return hpop(self.items)

	def peek(self):
		return self.items[0]

	def is_empty(self):
		return len(self.items) == 0

	def has_next(self):
		return not self.is_empty()


if __name__ == '__main__':
	hq = Heap([1, 2, 3, 4, 5, 6, 7])
	while not hq.is_empty():
		print (hq.pop())
