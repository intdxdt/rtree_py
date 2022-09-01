import math
import unittest
from mbr import MBR

m00 = MBR(0, 0, 0, 0)
m00.expand_include_xy(2, 2)

n00 = MBR(0, 0, 0, 0)
n00.expand_include_xy(-2, -2)

m0 = MBR(1, 1, 1, 1)
m0.expand_by_delta(1, 1)

m1 = MBR(0, 0, 2, 2)
m2 = MBR(4, 5, 8, 9)
m3 = MBR(1.7, 1.5, 5, 9)
m4 = MBR(5, 0, 8, 2)
m5 = MBR(5, 11, 8, 9)
m6 = MBR(0, 0, 2, -2)
m7 = MBR(-2, 1, 4, -2)
m8 = MBR(-1, 0, 1, -1.5)
p = [1.7, 1.5, 3.4]  # POINT(1.7 1.5, 3.4)
p0 = [1.7]


class TestMBR(unittest.TestCase):
    def test_special_cases(self):
        self.assertEqual(str(m1), "POLYGON ((0 0, 0 2, 2 2, 2 0, 0 0))")
        mz = MBR(0, 0, 0, 0)
        self.assertTrue(mz.is_point())
        self.assertFalse(m0.is_point())
        m1vals = []
        for v in m1:
            m1vals.append(v)
        self.assertEqual(tuple(m1vals), (0, 0, 2, 2))

        with self.assertRaises(Exception):
            m1[4] = 3.5
        with self.assertRaises(Exception):
            _ = m1[4]

    def test_equals(self):
        m0123 = MBR(0, 2, 1, 3)
        clone_m0123 = m0123.clone()
        self.assertEqual(m1.llur, ((0, 0), (2, 2)))
        self.assertTrue(clone_m0123.equals(m0123))
        self.assertTrue(m0.equals(m1))
        self.assertTrue(m00.equals(m1))

    def test_dist_relates(self):
        self.assertTrue(m1.intersects_point(p))
        self.assertFalse(m1.intersects_point(p0))

        self.assertTrue(m00.intersects(n00))
        nm00, success = m00.intersection(n00)
        self.assertTrue(success)

        self.assertTrue(nm00.minx == 0.0 and nm00.miny == 0.0)
        self.assertTrue(nm00.maxx == 0.0 and nm00.maxy == 0.0)
        self.assertTrue(nm00.is_point())

        self.assertFalse(m1.intersects(m2))
        _, success = m1.intersection(m2)
        self.assertFalse(success)
        self.assertTrue(m1.intersects(m3))
        self.assertTrue(m2.intersects(m3))

        m13, _ = m1.intersection(m3)
        m23, _ = m2.intersection(m3)
        _m13 = (1.7, 1.5, 2, 2)
        _m23 = (4, 5, 5, 9)

        self.assertEqual(_m13, m13.as_tuple())
        self.assertEqual(_m23, m23.as_tuple())

        self.assertTrue(m3.intersects(m4))
        self.assertTrue(m2.intersects(m5))
        self.assertTrue(m7.intersects(m6))
        self.assertTrue(m6.intersects(m7))

        m67, _ = m6.intersection(m7)
        m76, _ = m7.intersection(m6)
        m78, _ = m7.intersection(m8)

        self.assertTrue(m67.equals(m6))
        self.assertTrue(m67.equals(m76))
        self.assertTrue(m78.equals(m8))

        m25, _ = m2.intersection(m5)
        m34, _ = m3.intersection(m4)

        self.assertEqual(m25.width, m5.width)
        self.assertEqual(m25.height, 0.0)
        self.assertEqual(m34.width, 0.0)
        self.assertEqual(m34.height, 0.5)
        self.assertEqual(m3.distance(m4), 0.0)

        d = math.hypot(2, 3)
        self.assertEqual(m1.distance(m2), d)
        self.assertEqual(m1.distance_square(m2), round(d * d, 12))
        self.assertEqual(m1.distance(m3), 0.0)
        self.assertEqual(m1.distance_square(m3), 0.0)

        a = MBR(
            -7.703505430214746, 3.0022503796012305,
            -5.369812194018422, 5.231449888803689)
        self.assertTrue(m1.distance(a), math.hypot(-5.369812194018422, 3.0022503796012305 - 2))

        b = MBR(-4.742849832055231, -4.1033230559816065,
                -1.9563504455521576, -2.292098454754609)
        self.assertTrue(m1.distance(b), math.hypot(-1.9563504455521576, -2.292098454754609))

    def test_containment_relates(self):
        x1, y1, x2, y2 = 0, 1, 2, 3
        p1 = (-5.95, 9.28)
        p2 = (-0.11, 12.56)
        p3 = (3.58, 11.79)
        p4 = (-1.16, 14.71)
        p4x = (-1.16,)

        mp12 = MBR(p1[x1], p1[y1], p2[x1], p2[y1])
        mp34 = MBR(p3[x1], p3[y1], p4[x1], p4[y1])

        # intersects but segment are disjoint
        self.assertTrue(mp12.intersects(mp34))
        self.assertTrue(mp12.intersects_bounds(p3, p4))
        self.assertFalse(mp12.intersects_bounds(p3, p4x))
        self.assertFalse(mp12.intersects_bounds(
            [m1.minx, m1.miny],
            [m1.maxx, m1.maxy],
        ))
        self.assertFalse(mp12.intersects_point(p3))
        self.assertTrue(m1.contains_xy(1, 1))

        mbr11 = MBR(1, 1, 1.5, 1.5)
        mbr12 = MBR(1, 1, 2, 2)
        mbr13 = MBR(1, 1, 2.000045, 2.00001)
        mbr14 = MBR(2.000045, 2.00001, 4.000045, 4.00001)

        self.assertTrue(m1.contains(mbr11))
        self.assertTrue(m1.contains(mbr12))
        self.assertFalse(m1.contains(mbr13))
        self.assertFalse(m1.disjoint(mbr13))
        self.assertTrue(m1.disjoint(mbr14))

        self.assertTrue(m1.contains_xy(1.5, 1.5))
        self.assertTrue(m1.contains_xy(2, 2))

        self.assertTrue(m1.completely_contains_mbr(mbr11))
        self.assertTrue(m1.completely_contains_xy(1.5, 1.5))
        self.assertTrue(m1.completely_contains_xy(1.5, 1.5))
        self.assertFalse(m1.completely_contains_xy(2, 2))
        self.assertFalse(m1.completely_contains_mbr(mbr12))
        self.assertFalse(m1.completely_contains_mbr(mbr13))

    def test_area_translate_expand(self):
        ma = MBR(0, 0, 2, 2)
        mb = MBR(-1, -1, 1.5, 1.9)
        mc = MBR(1.7, 1.5, 5, 9)
        md = ma.clone()
        ma.expand_include_mbr(mc)
        md.expand_include_mbr(mb)

        self.assertEqual(ma.as_tuple(), (0, 0, 5, 9))  # ma modified by expand
        self.assertEqual(ma.as_poly_array(), ((0, 0), (0, 9), (5, 9), (5, 0), (0, 0)))  # ma modified by expand
        self.assertEqual(mc.as_tuple(), (1.7, 1.5, 5, 9))  # should not be touched
        self.assertEqual(md.as_tuple(), (-1, -1, 2, 2))  # ma modified by expand

        # mc area
        self.assertTrue(mc.area, 24.75)
        mt = m1.translate(1, 1)
        mby = m1.clone()
        mby.expand_by_delta(-3, -3)
        m1c = m1.center
        mtc = mt.center

        self.assertEqual(m1c, (1, 1))
        self.assertEqual(mtc, (2, 2))
        self.assertEqual(mt.as_tuple(), (1, 1, 3, 3))
        self.assertEqual(mby.as_tuple(), (-1, -1, 3, 3))


suite = unittest.TestLoader().loadTestsFromTestCase(TestMBR)
unittest.TextTestRunner(verbosity=4).run(suite)
