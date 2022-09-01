import os
import sys

base, _ = os.path.split(os.path.realpath(__file__))
base = os.path.abspath(os.path.join(base, "../"))
sys.path.insert(0, base)

from mbr import MBR

rtree_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(rtree_path)

import unittest

from rtree import RTree


def bbox(o):
    if isinstance(o, (tuple, list)):
        return o
    try:
        bx = o.bounds
    except:
        bx = tuple(o.bbox)
    return bx


def init_knn_data():
    return [[87, 55, 87, 56], [38, 13, 39, 16], [7, 47, 8, 47], [89, 9, 91, 12], [4, 58, 5, 60], [0, 11, 1, 12],
            [0, 5, 0, 6], [69, 78, 73, 78], [56, 77, 57, 81], [23, 7, 24, 9], [68, 24, 70, 26], [31, 47, 33, 50],
            [11, 13, 14, 15], [1, 80, 1, 80], [72, 90, 72, 91], [59, 79, 61, 83], [98, 77, 101, 77], [11, 55, 14, 56],
            [98, 4, 100, 6], [21, 54, 23, 58], [44, 74, 48, 74], [70, 57, 70, 61], [32, 9, 33, 12], [43, 87, 44, 91],
            [38, 60, 38, 60], [62, 48, 66, 50], [16, 87, 19, 91], [5, 98, 9, 99], [9, 89, 10, 90], [89, 2, 92, 6],
            [41, 95, 45, 98], [57, 36, 61, 40], [50, 1, 52, 1], [93, 87, 96, 88], [29, 42, 33, 42], [34, 43, 36, 44],
            [41, 64, 42, 65], [87, 3, 88, 4], [56, 50, 56, 52], [32, 13, 35, 15], [3, 8, 5, 11], [16, 33, 18, 33],
            [35, 39, 38, 40], [74, 54, 78, 56], [92, 87, 95, 90], [12, 97, 16, 98], [76, 39, 78, 40], [16, 93, 18, 95],
            [62, 40, 64, 42], [71, 87, 71, 88], [60, 85, 63, 86], [39, 52, 39, 56], [15, 18, 19, 18], [91, 62, 94, 63],
            [10, 16, 10, 18], [5, 86, 8, 87], [85, 85, 88, 86], [44, 84, 44, 88], [3, 94, 3, 97], [79, 74, 81, 78],
            [21, 63, 24, 66], [16, 22, 16, 22], [68, 97, 72, 97], [39, 65, 42, 65], [51, 68, 52, 69], [61, 38, 61, 42],
            [31, 65, 31, 65], [16, 6, 19, 6], [66, 39, 66, 41], [57, 32, 59, 35], [54, 80, 58, 84], [5, 67, 7, 71],
            [49, 96, 51, 98], [29, 45, 31, 47], [31, 72, 33, 74], [94, 25, 95, 26], [14, 7, 18, 8], [29, 0, 31, 1],
            [48, 38, 48, 40], [34, 29, 34, 32], [99, 21, 100, 25], [79, 3, 79, 4], [87, 1, 87, 5], [9, 77, 9, 81],
            [23, 25, 25, 29], [83, 48, 86, 51], [79, 94, 79, 95], [33, 95, 33, 99], [1, 14, 1, 14], [33, 77, 34, 77],
            [94, 56, 98, 59], [75, 25, 78, 26], [17, 73, 20, 74], [11, 3, 12, 4], [45, 12, 47, 12], [38, 39, 39, 39],
            [99, 3, 103, 5], [41, 92, 44, 96], [79, 40, 79, 41], [29, 2, 29, 4]]


def all_found(res, expected):
    expdict = dict()
    for x in expected:
        expdict[tuple(bbox(x))] = True

    bln = True
    for r in res:
        key = tuple(bbox(r))
        bln = bln and expdict.get(key, False)
    return bln


def fn_rich_data():
    richData = []
    data = [
        [1, 2, 1, 2], [3, 3, 3, 3], [5, 5, 5, 5], [4, 2, 4, 2],
        [2, 4, 2, 4], [5, 3, 5, 3], [3, 4, 3, 4], [2.5, 4, 2.5, 4],
    ]
    for i, d in enumerate(data):
        dd = d[:]
        dd.append(i + 1)
        richData.append(dd)
    return richData


def score(query, boxer):
    q = MBR(query[0], query[1], query[0], query[1])
    o = MBR(*boxer[:4])
    return q.distance(o)


class TestRTree_KNN(unittest.TestCase):
    def test_knn(self):
        rt = RTree(9)
        data = init_knn_data()
        rt.load(data)
        nn = rt.knn((40, 40), score=score, limit=10)
        nr = rt.knn((40, 40), limit=10)
        expected = [
            [38, 39, 39, 39], [35, 39, 38, 40], [34, 43, 36, 44], [29, 42, 33, 42], [48, 38, 48, 40],
            [31, 47, 33, 50], [34, 29, 34, 32], [29, 45, 31, 47], [39, 52, 39, 56], [57, 36, 61, 40]
        ]
        self.assertTrue(all_found(nn, expected))
        nn = rt.knn((40, 40), score=score, limit=1000)
        self.assertEqual(len(nn), len(data))
        # --------------------------------------------------
        self.assertTrue(all_found(nr, expected))
        nr = rt.knn((40, 40), limit=1000)
        self.assertEqual(len(nr), len(data))

    def test_rtree_knn_predicate(self):
        predicate_mbr = []

        def scoreFunc(query, obj):
            if isinstance(obj, MBR):
                dist = query.distance(obj)
            else:
                dist = query.distance(MBR(*obj[:4]))
            return dist

        def createPredicate(dist):
            def func(candidate):
                self.assertTrue(candidate.leaf)
                if candidate.dist <= dist:
                    predicate_mbr.append(MBR(*candidate.node))
                    return True, False
                return False, True

            return func

        rt = RTree(9)
        data = init_knn_data()
        rt.load(data)
        prefFn = createPredicate(6)
        query = MBR(
            74.88825108886668, 82.678427498132,
            74.88825108886668, 82.678427498132,
        )
        res = rt.knn(query, limit=10, score=scoreFunc, predicate=prefFn)
        self.assertEqual(len(res), 2)
        for i, r in enumerate(res):
            self.assertTrue(tuple(r), predicate_mbr[i].as_tuple())

    def test_knn_predicate(self):
        rt = RTree(9)
        rt.load(fn_rich_data())

        def pred(v):
            return v.node[-1] < 5, False

        query = (2, 4)
        result = rt.knn(query, limit=1, predicate=pred, score=score)
        self.assertTrue(len(result) == 1)
        v = result[0][:4]
        self.assertEqual(tuple(bbox(v)), tuple(bbox([3, 3, 3, 3])))
        self.assertEqual(2, result[0][-1])


unittest.TextTestRunner(verbosity=10).run(
    unittest.TestLoader().loadTestsFromTestCase(TestRTree_KNN)
)
