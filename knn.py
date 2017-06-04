from collections import namedtuple
from _heap import Heap
from node import Node
from shapely.geometry import Polygon

QObj = namedtuple('QObj', ('dist', 'node', 'leaf'))


def poly_box(obj):
	"""
	(x1,y2)              (x2,y2)
		   __|_________|__
			 |         |
			 |         |
		   __|_________|__
			 |         |
	 (x1,y1)             (x2,y1)
	"""
	o = bbox(obj)
	x1, y1, x2, y2 = o[0], o[1], o[2], o[3]
	pgeom = Polygon(((x1, y1), (x1, y2), (x2, y2), (x2, y1)))
	return pgeom


def bbox(o):
	if isinstance(o, (tuple, list)):
		return o
	try:
		bx = o.bounds
	except:
		bx = tuple(o.bbox)
	return bx


def KNN(tree, query, limit, scoreFn, predicate):
	node = tree.data
	result = []
	queue = Heap()
	stop = False

	while node and (not stop):
		for child in node.children:
			if not isinstance(child, Node):
				dist = scoreFn(query, child)
			else:
				dist = scoreFn(query, poly_box(child))
			# print gbox
			o = QObj(dist, child, node.leaf)
			queue.push(o)

		while (not queue.is_empty()) and queue.peek().leaf:
			candidate = queue.pop()
			pred, stop = predicate(candidate)
			if pred:
				result.append(candidate.node)

			if stop:
				break

			if limit != 0 and len(result) == limit:
				return result

		if not stop:
			if queue.is_empty():
				node = None
			else:
				node = queue.pop().node
	return result
