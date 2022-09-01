import sys
import math

x1, y1, x2, y2 = 0, 1, 2, 3
Eps = 1.0e-10
Eps2 = Eps * Eps


def float_equal(a, b):
    """
    float_equal compare the equality of floats
    Ref: http:#floating-point-gui.de/errors/comparison/
    compare floating point precision

    >>> 0.3 == 0.1+ 0.2
    False
    >>> float_equal(0.3, 0.1+ 0.2)
    True

    :param b:
    :param a:
    """
    absA = abs(a)
    absB = abs(b)
    diff = abs(a - b)

    if a == b:
        # shortcut, handles infinities
        return True
    elif a == 0.0 or b == 0.0 or diff < Eps:
        # a or b is zero or both are extremely close to it
        # relative error is less meaningful here
        return (diff < Eps) or (diff < Eps2)
    # use relative error
    return (diff / min((absA + absB), sys.float_info.max)) < Eps


class MBR(object):
    """
     minimum bounding rectangle
     @class :MBR
    """

    def __init__(self, ax, ay, bx, by):
        """
         MBR
         :param ax:float
         :param bx:float
         :param ay:float
         :param by:float
        """
        self.minx, self.maxx = min(ax, bx), max(ax, bx)
        self.miny, self.maxy = min(ay, by), max(ay, by)

    def __iter__(self):
        """
        interable
        :return: iter
        """
        return iter((self.minx, self.miny, self.maxx, self.maxy))

    def __getitem__(self, index):
        """
        get item
        :param index:
        :return: float
        """
        if index == 0:
            v = self.minx
        elif index == 1:
            v = self.miny
        elif index == 2:
            v = self.maxx
        elif index == 3:
            v = self.maxy
        else:
            raise Exception('invalid index')
        return v

    def __setitem__(self, index, v):
        """
        set item
        :param index:
        :param v:
        """
        if index == 0:
            self.minx = v
        elif index == 1:
            self.miny = v
        elif index == 2:
            self.maxx = v
        elif index == 3:
            self.maxy = v
        else:
            raise Exception('invalid index')

    def __repr__(self):
        """
         MBR to string
         :return:string
        """
        return "POLYGON ((" + ", ".join([
            str(self.minx) + " " + str(self.miny),
            str(self.minx) + " " + str(self.maxy),
            str(self.maxx) + " " + str(self.maxy),
            str(self.maxx) + " " + str(self.miny),
            str(self.minx) + " " + str(self.miny)
        ]) + "))"

    def as_poly_array(self):
        """
        as polygon array
        :return:tuple
        """
        lx, ly = self.minx, self.miny
        ux, uy = self.maxx, self.maxy
        return (lx, ly), (lx, uy), (ux, uy), (ux, ly), (lx, ly)

    def is_point(self):
        """
        is mbr point
        :return:bool
        """
        return float_equal(self.height, 0.0) and float_equal(self.width, 0.0)

    def clone(self):
        """
         :return:MBR
        """
        return MBR(self.minx, self.miny, self.maxx, self.maxy)

    def as_tuple(self):
        """
         lower left and upper right
         :return:tuple
        """
        return self.minx, self.miny, self.maxx, self.maxy

    def equals(self, other):
        """
         compute equals
         @param other
         :return:bool
        """
        return float_equal(self.maxx, other.maxx) and \
               float_equal(self.maxy, other.maxy) and \
               float_equal(self.minx, other.minx) and \
               float_equal(self.miny, other.miny)

    def translate(self, dx, dy):
        """
        translate mbr  by change in x and y
        @param dy:float
        @param dx:float
        :return:MBR
        """
        return MBR(
            self.minx + dx, self.miny + dy,
            self.maxx + dx, self.maxy + dy,
        )

    def intersection(self, other):
        """
        intersection
        @param other:MBR
        :return:MBR,bool
        """
        minx, miny = float('nan'), float('nan')
        maxx, maxy = float('nan'), float('nan')
        inters = self.intersects(other)
        if inters:
            if self[x1] > other[x1]:
                minx = self[x1]
            else:
                minx = other[x1]

            if self[y1] > other[y1]:
                miny = self[y1]
            else:
                miny = other[y1]

            if self[x2] < other[x2]:
                maxx = self[x2]
            else:
                maxx = other[x2]

            if self[y2] < other[y2]:
                maxy = self[y2]
            else:
                maxy = other[y2]

        return MBR(minx, miny, maxx, maxy), inters

    def intersects_bounds(self, q1, q2):
        """
        intersects bounds
        @param q1:tuple
        @param q2:tuple
        :return:bool
        """
        if len(q1) < 2 or len(q2) < 2:
            return False

        minq = min(q1[x1], q2[x1])
        maxq = max(q1[x1], q2[x1])

        if self[x1] > maxq or self[x2] < minq:
            return False

        minq = min(q1[y1], q2[y1])
        maxq = max(q1[y1], q2[y1])

        # not disjoint
        return not (self[y1] > maxq or self[y2] < minq)

    def contains(self, other):
        """
        contains
        @param other:MBR
        :return:bool
        """
        return (other[x1] >= self[x1]) and (other[x2] <= self[x2]) and \
               (other[y1] >= self[y1]) and (other[y2] <= self[y2])

    def contains_xy(self, x, y):
        """
        contains xy
        :param x:float
        :param y:float
        :return:
        """
        return (x >= self[x1]) and (x <= self[x2]) and \
               (y >= self[y1]) and (y <= self[y2])

    def completely_contains_xy(self, x, y):
        """
        completely contains xy - xy cannot be on boundary
        @param x:float
        @param y:float
        :return:
        """
        return (x > self[x1]) and (x < self[x2]) and \
               (y > self[y1]) and (y < self[y2])

    def completely_contains_mbr(self, other):
        """
        contains other mbr - boundaries don't touch
        @param other:MBR
        :return:bool
        """
        return (other[x1] > self[x1]) and (other[x2] < self[x2]) and \
               (other[y1] > self[y1]) and (other[y2] < self[y2])

    def disjoint(self, other):
        """
        computes disjointness
        @param other:MBR
        :return:bool
        """
        return not self.intersects(other)

    def intersects(self, other):
        """
        intersects
        @param other:
        :return:bool
        """
        return not (other[x1] > self[x2] or other[x2] < self[x1] or
                    other[y1] > self[y2] or other[y2] < self[y1])

    def intersects_point(self, pt):
        """
        intersects point
        @param pt:tuple
        :return:bool
        """
        if len(pt) < 2:
            return False
        return self.contains_xy(pt[x1], pt[y1])

    def expand_include_mbr(self, other):
        """
        expand include other mbr
        @param other:MBR
        :return:bool
        """

        if other[x1] < self[x1]:
            self[x1] = other[x1]

        if other[x2] > self[x2]:
            self[x2] = other[x2]

        if other[y1] < self[y1]:
            self[y1] = other[y1]

        if other[y2] > self[y2]:
            self[y2] = other[y2]

        return self

    def expand_by_delta(self, dx, dy):
        """
        expand by delta in x and y
        @param dx:float
        @param dy:float
        :return:bool
        """
        minx, miny = self[x1] - dx, self[y1] - dy
        maxx, maxy = self[x2] + dx, self[y2] + dy

        minx, maxx = min(minx, maxx), max(minx, maxx)
        miny, maxy = min(miny, maxy), max(miny, maxy)

        self[x1], self[y1] = minx, miny
        self[x2], self[y2] = maxx, maxy
        return self

    # ExpandXY expands mbr to include x and y
    def expand_include_xy(self, x_coord, y_coord):
        """
        expand include xy
        @param x_coord:float
        @param y_coord:float
        :return:MBR
        """
        if x_coord < self[x1]:
            self[x1] = x_coord
        elif x_coord > self[x2]:
            self[x2] = x_coord

        if y_coord < self[y1]:
            self[y1] = y_coord
        elif y_coord > self[y2]:
            self[y2] = y_coord
        return self

    def _distance_dxdy(self, other):
        """
        computes dx and dy for computing hypot
        @param other:MBR
        :return:tuple
        """
        dx, dy = 0.0, 0.0

        # find closest edge by x
        if self[x2] < other[x1]:
            dx = other[x1] - self[x2]
        elif self[x1] > other[x2]:
            dx = self[x1] - other[x2]

        # find closest edge by y
        if self[y2] < other[y1]:
            dy = other[y1] - self[y2]
        elif self[y1] > other[y2]:
            dy = self[y1] - other[y2]

        return dx, dy

    def distance(self, other):
        """
        distance computes the distance between two mbrs
        @param other:MBR
        :return:float
        """
        if self.intersects(other):
            return 0.0

        dx, dy = self._distance_dxdy(other)
        return math.hypot(dx, dy)

    def distance_square(self, other):
        """
        distance square computes the distance
        squared between mbrs
        @param other:MBR
        :return:float
        """
        if self.intersects(other):
            return 0.0
        dx, dy = self._distance_dxdy(other)
        return (dx * dx) + (dy * dy)

    @property
    def llur(self):
        """
         lower left and upper right
         :return:tuple
        """
        return (self.minx, self.miny), (self.maxx, self.maxy)

    @property
    def width(self):
        """
         returns the difference between
         the maximum and minimum x values.
         :return:float
        """
        return self.maxx - self.minx

    @property
    def height(self):
        """
        returns the difference between
        the maximum and minimum y values.
        :return:float
        """
        return self.maxy - self.miny

    @property
    def area(self):
        """
         area
         :return:float
        """
        return self.height * self.width

    @property
    def center(self):
        """
        center mbr - x and y
        :returns:tuple
        """
        return (self.minx + self.maxx) / 2.0, (self.miny + self.maxy) / 2.0
