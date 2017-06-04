import pickle
import unittest
from node import Node


class TestRTreeNode(unittest.TestCase):
	def test_knn(self):
		b = Node(a=1, c=3, b=2)
		d = Node(b=2000, m=55, children=[1, 2, 3])
		self.assertEqual(d.m, 55)
		self.assertEqual(d.children, [1, 2, 3])
		self.assertEqual(d.size, 3)
		self.assertEqual(b.children, [])
		self.assertFalse(b.leaf)
		self.assertFalse(b.hasattr("m"))
		with self.assertRaises(Exception):
			print b.m

		b.update(d)
		self.assertDictEqual(b, {'a'       : 1, 'c': 3, 'b': 2000, 'leaf': False,
		                         'm'       : 55, 'height': 1,
		                         'bbox'    : [float('inf'), float('inf'), float('-inf'), float('-inf')],
		                         'children': [1, 2, 3]})

		self.assertFalse(hasattr(b, 'x'))
		self.assertFalse(b.hasattr('x'))
		self.assertEqual(getattr(b, 'm'), 55)
		self.assertTrue(hasattr(b, 'c'))
		self.assertTrue(b.hasattr('c'))

		self.assertEqual(d, {'b'   : 2000, 'leaf': False, 'm': 55, 'height': 1,
		                     'bbox': [float('inf'), float('inf'), float('-inf'), float('-inf')],
		                     'children': [1, 2, 3]})
		self.assertTrue(isinstance(b, dict))
		self.assertEqual(b['b'], 2000)

		self.assertDictEqual(pickle.loads(pickle.dumps(b)), b)



unittest.TextTestRunner(verbosity=10).run(
	unittest.TestLoader().loadTestsFromTestCase(TestRTreeNode)
)
