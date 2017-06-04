import copy
import os
import sys
import unittest
import random
from _rtree import RTree

true = True
rtree_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(rtree_path)
rtree = RTree


def compare(x, y):
	if x < y:
		return -1
	elif x > y:
		return 1
	else:
		return 0


def sortedEqual(t, a, b, compare=compare):
	a = sorted(a[:], cmp=compare)
	b = sorted(b[:], cmp=compare)
	t.assertEqual(a, b)


def someData(n):
	data = []
	for i in xrange(0, n):
		data.append([i, i, i, i])
	return data


def RandBox(size):
	x = random.random() * (100.0 - size)
	y = random.random() * (100.0 - size)
	return [x, y, (x + size * random.random()), (y + size * random.random())]


def GenDataItems(N, size):
	data = []
	for i in xrange(N):
		data.append(RandBox(size))
	return data


data = [[0, 0, 0, 0], [10, 10, 10, 10], [20, 20, 20, 20], [25, 0, 25, 0], [35, 10, 35, 10], [45, 20, 45, 20],
        [0, 25, 0, 25], [10, 35, 10, 35],
        [20, 45, 20, 45], [25, 25, 25, 25], [35, 35, 35, 35], [45, 45, 45, 45], [50, 0, 50, 0], [60, 10, 60, 10],
        [70, 20, 70, 20], [75, 0, 75, 0],
        [85, 10, 85, 10], [95, 20, 95, 20], [50, 25, 50, 25], [60, 35, 60, 35], [70, 45, 70, 45], [75, 25, 75, 25],
        [85, 35, 85, 35], [95, 45, 95, 45],
        [0, 50, 0, 50], [10, 60, 10, 60], [20, 70, 20, 70], [25, 50, 25, 50], [35, 60, 35, 60], [45, 70, 45, 70],
        [0, 75, 0, 75], [10, 85, 10, 85],
        [20, 95, 20, 95], [25, 75, 25, 75], [35, 85, 35, 85], [45, 95, 45, 95], [50, 50, 50, 50], [60, 60, 60, 60],
        [70, 70, 70, 70], [75, 50, 75, 50],
        [85, 60, 85, 60], [95, 70, 95, 70], [50, 75, 50, 75], [60, 85, 60, 85], [70, 95, 70, 95], [75, 75, 75, 75],
        [85, 85, 85, 85], [95, 95, 95, 95]]

testTree = {
	"children": [
		{
			"children": [
				{"children": [[0, 0, 0, 0], [10, 10, 10, 10], [20, 20, 20, 20], [25, 0, 25, 0]], "height": 1,
				 "bbox"    : [0, 0, 25, 20], "leaf": true},
				{"children": [[0, 25, 0, 25], [10, 35, 10, 35], [25, 25, 25, 25], [20, 45, 20, 45]], "height": 1,
				 "bbox"    : [0, 25, 25, 45], "leaf": true},
				{"children": [[50, 0, 50, 0], [35, 10, 35, 10], [60, 10, 60, 10], [45, 20, 45, 20]], "height": 1,
				 "bbox"    : [35, 0, 60, 20], "leaf": true},
				{"children": [[50, 25, 50, 25], [35, 35, 35, 35], [60, 35, 60, 35], [45, 45, 45, 45]], "height": 1,
				 "bbox"    : [35, 25, 60, 45], "leaf": true}
			],
			"height"  : 2,
			"bbox"    : [0, 0, 60, 45]
		},
		{
			"children": [
				{"children": [[0, 50, 0, 50], [25, 50, 25, 50], [10, 60, 10, 60], [20, 70, 20, 70]], "height": 1,
				 "bbox"    : [0, 50, 25, 70], "leaf": true},
				{"children": [[0, 75, 0, 75], [25, 75, 25, 75], [10, 85, 10, 85], [20, 95, 20, 95]], "height": 1,
				 "bbox"    : [0, 75, 25, 95], "leaf": true},
				{"children": [[35, 60, 35, 60], [50, 50, 50, 50], [60, 60, 60, 60], [45, 70, 45, 70]], "height": 1,
				 "bbox"    : [35, 50, 60, 70], "leaf": true},
				{"children": [[50, 75, 50, 75], [60, 85, 60, 85], [45, 95, 45, 95], [35, 85, 35, 85]], "height": 1,
				 "bbox"    : [35, 75, 60, 95], "leaf": true}
			],
			"height"  : 2,
			"bbox"    : [0, 50, 60, 95]
		},
		{
			"children": [
				{"children": [[70, 20, 70, 20], [75, 0, 75, 0], [75, 25, 75, 25], [70, 45, 70, 45]], "height": 1,
				 "bbox"    : [70, 0, 75, 45], "leaf": true},
				{"children": [[75, 50, 75, 50], [70, 70, 70, 70], [75, 75, 75, 75], [70, 95, 70, 95]], "height": 1,
				 "bbox"    : [70, 50, 75, 95], "leaf": true},
				{"children": [[85, 10, 85, 10], [95, 20, 95, 20], [85, 35, 85, 35], [95, 45, 95, 45]], "height": 1,
				 "bbox"    : [85, 10, 95, 45], "leaf": true},
				{"children": [[85, 60, 85, 60], [95, 70, 95, 70], [85, 85, 85, 85], [95, 95, 95, 95]], "height": 1,
				 "bbox"    : [85, 60, 95, 95], "leaf": true}
			],
			"height"  : 2,
			"bbox"    : [70, 0, 95, 95]
		}],
	"height"  : 3,
	"bbox"    : [0, 0, 95, 95]
}


class TestRTree(unittest.TestCase):
	def test_format(self):
		"""
		constructor accepts a format argument to customize the data format'
		"""
		tree = rtree(4, ['.minLng', '.minLat', '.maxLng', '.maxLat'])
		self.assertEqual(tree.toBBox({'minLng': 1, 'minLat': 2, 'maxLng': 3, 'maxLat': 4}), [1, 2, 3, 4])

	def test_maxentries(self):
		"""
		constructor uses 9 max entries by default
		"""
		t = self
		tree = rtree()
		tree.load(someData(9))
		t.assertEqual(tree.json['height'], 1)

		tree2 = rtree()
		tree2.load(someData(10))
		t.assertEqual(tree2.json['height'], 2)

	def test_custom_access(self):
		"""toBBox, compareMinX, compareMinY can be overriden to allow custom data structures"""
		t = self
		tree = rtree(4)

		def toBBox(item):
			return [item['minLng'], item['minLat'], item['maxLng'], item['maxLat']]

		def compareMinX(a, b):
			return a['minLng'] - b['minLng']

		def compareMinY(a, b):
			return a.minLat - b.minLat

		tree.toBBox = toBBox
		tree.compareMinX = compareMinX
		tree.compareMinY = compareMinY

		data = [
			{'minLng': -115, 'minLat': 45, 'maxLng': -105, 'maxLat': 55},
			{'minLng': 105, 'minLat': 45, 'maxLng': 115, 'maxLat': 55},
			{'minLng': 105, 'minLat': -55, 'maxLng': 115, 'maxLat': -45},
			{'minLng': -115, 'minLat': -55, 'maxLng': -105, 'maxLat': -45}
		]

		tree.load(data)

		def byLngLat(a, b):
			return a['minLng'] - b['minLng'] or a['minLat'] - b['minLat']

		sortedEqual(t, tree.search([-180, -90, 180, 90]), [
			{'minLng': -115, 'minLat': 45, 'maxLng': -105, 'maxLat': 55},
			{'minLng': 105, 'minLat': 45, 'maxLng': 115, 'maxLat': 55},
			{'minLng': 105, 'minLat': -55, 'maxLng': 115, 'maxLat': -45},
			{'minLng': -115, 'minLat': -55, 'maxLng': -105, 'maxLat': -45}
		], byLngLat)

		sortedEqual(t, tree.search([-180, -90, 0, 90]), [
			{'minLng': -115, 'minLat': 45, 'maxLng': -105, 'maxLat': 55},
			{'minLng': -115, 'minLat': -55, 'maxLng': -105, 'maxLat': -45}
		], byLngLat)

		sortedEqual(t, tree.search([0, -90, 180, 90]), [
			{'minLng': 105, 'minLat': 45, 'maxLng': 115, 'maxLat': 55},
			{'minLng': 105, 'minLat': -55, 'maxLng': 115, 'maxLat': -45}
		], byLngLat)

		sortedEqual(t, tree.search([-180, 0, 180, 90]), [
			{'minLng': -115, 'minLat': 45, 'maxLng': -105, 'maxLat': 55},
			{'minLng': 105, 'minLat': 45, 'maxLng': 115, 'maxLat': 55}
		], byLngLat)

		sortedEqual(t, tree.search([-180, -90, 180, 0]), [
			{'minLng': 105, 'minLat': -55, 'maxLng': 115, 'maxLat': -45},
			{'minLng': -115, 'minLat': -55, 'maxLng': -105, 'maxLat': -45}
		], byLngLat)

	def test_bulkload_search(self):
		"""load bulk-loads the given data given max node entries and forms a proper search tree"""
		tree = rtree(4).load(data)
		tree_all = tree.all()
		from_json_all = rtree(4).from_json(testTree).all()
		sortedEqual(self, tree_all, from_json_all, compare)

	def test_usestandard_size(self):
		"""load uses standard insertion when given a low number of items"""
		tree = rtree(8).load(data).load(data[0: 3])
		tree2 = rtree(8).load(data)
		tree2.insert(data[0])
		tree2.insert(data[1])
		tree2.insert(data[2])
		self.assertEqual(tree.json, tree2.json)

	def test_load_nothing(self):
		"""load does nothing if loading empty data"""
		tree = rtree().load([])
		self.assertEqual(tree.json, rtree().json)

	def test_merge_split(self):
		"""load properly splits tree root when merging trees of the same height"""
		tree = rtree(4).load(data)
		tree.load(data)
		self.assertEqual(tree.json['height'], 4)
		sortedEqual(self, tree.all(), data + data, compare)

	def test_load_merge_small_big(self):
		"""load properly merges data of smaller or bigger tree heights"""
		smaller = someData(10)

		tree1 = rtree(4).load(data)
		tree1.load(smaller)

		tree2 = rtree(4).load(smaller)
		tree2.load(data)

		self.assertEqual(tree1.json['height'], tree2.json['height'])
		sortedEqual(self, tree1.all(), data + smaller)
		sortedEqual(self, tree2.all(), data + smaller)

	def test_serch_box(self):
		"""search finds matching points in the tree given a bbox"""
		tree = rtree(4).load(data)
		result = tree.search([40, 20, 80, 70])

		sortedEqual(self, result, [
			[70, 20, 70, 20], [75, 25, 75, 25], [45, 45, 45, 45], [50, 50, 50, 50], [60, 60, 60, 60], [70, 70, 70, 70],
			[45, 20, 45, 20], [45, 70, 45, 70], [75, 50, 75, 50], [50, 25, 50, 25], [60, 35, 60, 35], [70, 45, 70, 45]
		])

	def test_search_empty(self):
		"""search returns an empty array if nothing found"""
		result = rtree(4).load(data).search([200, 200, 210, 210])
		self.assertEqual(result, [])

	def test_all_tree(self):
		"""all returns all points in the tree"""
		tree = rtree(4).load(data)
		result = tree.all()

		sortedEqual(self, result, data)
		sortedEqual(self, tree.search([0, 0, 100, 100]), data)

	def test_exports_json(self):
		"""toJSON & from_json exports and imports search tree in JSON format"""

		tree = rtree(4)
		tree.from_json(testTree)
		tree2 = rtree(4).load(data)
		sortedEqual(self, tree.all(), tree2.all())

	def test_insert_existing(self):
		"""insert adds an item to an existing tree correctly"""
		tree = rtree(4).load([[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2]])
		tree.insert([3, 3, 3, 3])

		self.assertEqual(tree.json, {
			'children': [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
			'leaf'    : true, 'height': 1, 'bbox': [0, 0, 3, 3]
		})

		tree.insert([1, 1, 2, 2])

		self.assertEqual(tree.json, {
			'children': [
				{'children': [[0, 0, 0, 0], [1, 1, 1, 1]], 'leaf': true, 'height': 1, 'bbox': [0, 0, 1, 1]},
				{'children': [[1, 1, 2, 2], [2, 2, 2, 2], [3, 3, 3, 3]], 'height': 1, 'leaf': true,
				 'bbox'    : [1, 1, 3, 3]}
			],
			'height'  : 2, 'leaf': False, 'bbox': [0, 0, 3, 3]
		})

	def test_remove_nothingfound(self):
		"""remove does nothing if nothing found"""
		self.assertEqual(
			rtree().load(data).data,
			rtree().load(data).remove([13, 13, 13, 13]).data
		)

	def test_remove_nothing(self):
		"""remove does nothing if given undefined """
		self.assertEqual(
			rtree().load(data).data,
			rtree().load(data).remove().data
		)

	def test_remove_all(self):
		"""remove brings the tree to a clear state when removing everything one by one"""
		tree = rtree(4).load(data)

		for d in data:
			tree.remove(d)

		self.assertEqual(tree.json, rtree(4).json)

	def test_clear_all(self):
		"""clear should clear all the data in the tree"""
		self.assertEqual(
			rtree(4).load(data).clear().json,
			rtree(4).json
		)

	def test_chainable(self):
		"""should have chainable API"""
		rtree().load(data).insert(data[0]).remove(data[0]).from_json(testTree)

	def test_bigdata(self):
		"""should have chainable API"""
		N = int(700)
		data = GenDataItems(N, 1)
		dp_data = copy.deepcopy(data)

		r0 = rtree()
		for d in data:
			r0.insert(d)
		r1 = rtree().load(dp_data)

		self.assertEqual(r0.data.bbox, r1.data.bbox)
		self.assertTrue(r1.data.height - r0.data.height < 2)


unittest.TextTestRunner(verbosity=10).run(
	unittest.TestLoader().loadTestsFromTestCase(TestRTree)
)
