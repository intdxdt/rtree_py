__author__ = 'titus'

"""
Author : Titus Tienaah  - 2015
@after Vladimir Agafonkin - 2013
 rtree, a python library for high-performance
 2D spatial indexing of points and rectangles.
 https:#github.com/mourner/rbush
"""

import json
import math
from _mbr import empty
from node import Node
from knn import KNN

MinX, MinY, MaxX, MaxY = 0, 1, 2, 3


def _knn_predicate(_):
    return True, False


def _axis_dist(k, min_val, max_val):
    v = k - max_val

    if k < min_val:
        v = min_val - k

    elif k <= max_val:
        v = 0.0

    return v


def _box_score_dist(defaultPt, child):
    x, y = defaultPt[0], defaultPt[1]
    box = child
    return math.hypot(
        _axis_dist(x, box[MinX], box[MaxX]),
        _axis_dist(y, box[MinY], box[MaxY]),
    )


class RTree(object):
    def __init__(self, maxEntries=9, attribute=None):
        self.maxEntries = max(4, maxEntries)
        self.minEntries = max(2, int(math.ceil(self.maxEntries * 0.4)))
        self.compareMinX = compareMinX
        self.compareMinY = compareMinY
        self.toBBox = toBBox

        self.data = Node()

        if attribute:
            attribute = [f.replace(".", "") for f in attribute]
            self._init_format(attribute)

        self.clear()

    def all(self):
        return _all(self.data, [])

    @property
    def json(self):
        return json.loads(json.dumps(self.data))

    def insert(self, item=None):
        if item:
            self._insert(item, self.data.height - 1)
        return self

    def remove(self, item=None):
        if not item:
            return self

        node, bbox, path, indexes = self.data, self.toBBox(item), [], []
        i = parent = goingUp = None

        # depth-first iterative self traversal
        while node or path:
            if not node:  # go up
                node = path.pop()
                parent = path[-1] if path else None
                i = indexes.pop()
                goingUp = True

            if node.leaf:  # check current node
                try:
                    index = node.children.index(item)
                except:
                    index = None

                if index is not None:
                    # item found, remove the item and condense self upwards
                    node.children.pop(index)
                    path.append(node)
                    self._condense(path)
                    return self

            if (not goingUp) and (not node.leaf) and contains(node.bbox, bbox):  # go down
                path.append(node)
                indexes.append(i)
                i = 0
                parent = node
                node = node.children[0]
            elif parent:  # go right
                i += 1
                node = parent.children[i] if i < len(parent.children) else None
                goingUp = False

            else:
                node = None
                # nothing found
        return self

    def clear(self):
        self.data = Node(children=[], height=1, bbox=empty(), leaf=True)
        return self

    def from_json(self, data):
        data = Node(**data)
        stack = [data]
        while stack:
            node = stack.pop()
            for i, n in enumerate(node.children):
                if isinstance(n, dict):
                    node.children[i] = Node(**n)
                    stack.append(node.children[i])
        self.data = data
        return self

    def search(self, bbox):
        node = self.data
        result = []

        if not intersects(bbox, node.bbox):
            return result

        nodesToSearch = []

        while node:
            for i in xrange(len(node.children)):
                child = node.children[i]
                childBBox = self.toBBox(child) if node.leaf else child.bbox

                if intersects(bbox, childBBox):
                    if node.leaf:
                        result.append(child)
                    elif contains(bbox, childBBox):
                        _all(child, result)
                    else:
                        nodesToSearch.append(child)
            node = nodesToSearch.pop() if nodesToSearch else None
        return result

    def load(self, data):
        if not data:
            return self

        if len(data) < self.minEntries:
            for i in xrange(len(data)):
                self.insert(data[i])

            return self

        # recursively build the self with the given data from stratch using OMT algorithm
        node = self._build(data[:], 0, len(data) - 1, 0)

        if self.data.size == 0:
            # save as is if self is empty
            self.data = node

        elif self.data.height == node.height:
            # split root if trees have the same height
            self._splitRoot(self.data, node)

        else:
            if self.data.height < node.height:
                # swap trees if inserted one is bigger
                tmpNode = self.data
                self.data = node
                node = tmpNode
                # self.data, node = node, self.data

            # insert the small self into the large self at appropriate level
            self._insert(node, self.data.height - node.height - 1, True)

        return self

    def knn(self, gobj, limit, score=_box_score_dist, predicate=_knn_predicate):
        return KNN(self, gobj, limit, score=score, predicate=predicate)

    def _init_format(self, attribute):
        def _diff(attr):
            def cmpattr(oa, ob):
                return comparator(getattr(oa, attr), getattr(ob, attr))

            return cmpattr

        def _bbox(o):
            if isinstance(o, dict):
                return [o[f] for f in attribute]
            return [getattr(o, f) for f in attribute]

        self.compareMinX = _diff(attribute[0])
        self.compareMinY = _diff(attribute[1])
        self.toBBox = _bbox
        return self

    def _condense(self, path):
        # go through the path, removing empty nodes and updating bboxes
        for i in xrange(len(path) - 1, 0 - 1, -1):
            if len(path[i].children) == 0:
                if i > 0:
                    siblings = path[i - 1].children
                    siblings.pop(siblings.index(path[i]))
                else:
                    self.clear()
            else:
                calcBBox(path[i], self.toBBox)

    # split overflowed node into two
    def _split(self, insertPath, level):
        node = insertPath[level]
        M = node.size  # .children
        m = self.minEntries

        self._chooseSplitAxis(node, m, M)

        splice = self._chooseSplitIndex(node, m, M)
        newNode = Node(children=node.children[splice:], height=node.height, leaf=node.leaf)
        node.children = node.children[:splice]

        calcBBox(node, self.toBBox)
        calcBBox(newNode, self.toBBox)

        if level:
            insertPath[level - 1].children.append(newNode)
        else:
            self._splitRoot(node, newNode)

    def _splitRoot(self, node, newNode):
        # split root node
        self.data = Node(
            children=[node, newNode],
            height=node.height + 1
        )
        calcBBox(self.data, self.toBBox)

    def _chooseSplitIndex(self, node, m, M):
        minOverlap = minArea = float("inf")
        index = None
        for i in xrange(m, (M - m) + 1):
            bbox1 = distBBox(node, 0, i, self.toBBox)
            bbox2 = distBBox(node, i, M, self.toBBox)

            overlap = intersectionArea(bbox1, bbox2)
            area = bboxArea(bbox1) + bboxArea(bbox2)

            # choose distribution with minimum overlap
            if overlap < minOverlap:
                minOverlap = overlap
                index = i
                minArea = min(area, minArea)


            elif overlap == minOverlap:
                # otherwise choose distribution with minimum area
                if area < minArea:
                    minArea = area
                    index = i
        return index

    # sorts node children by the best axis for split
    def _chooseSplitAxis(self, node, m, M):
        compareMinX = self.compareMinX if node.leaf else compareNodeMinX
        compareMinY = self.compareMinY if node.leaf else compareNodeMinY

        xMargin = self._allDistMargin(node, m, M, compareMinX)
        yMargin = self._allDistMargin(node, m, M, compareMinY)

        # if total distributions margin value is minimal for x, sort by minX,
        # otherwise it's already sorted by minY
        if xMargin < yMargin:
            node.children.sort(compareMinX)

    # total margin of all possible split distributions where each node is at least m full
    def _allDistMargin(self, node, m, M, compare):
        node.children.sort(compare)

        leftBBox = distBBox(node, 0, m, self.toBBox)
        rightBBox = distBBox(node, M - m, M, self.toBBox)

        margin = bboxMargin(leftBBox) + bboxMargin(rightBBox)

        for i in xrange(m, M - m):
            child = node.children[i]
            extend(leftBBox, self.toBBox(child) if node.leaf  else child.bbox)
            margin += bboxMargin(leftBBox)

        for i in xrange(M - m - 1, m - 1, -1):  # M-m-1 to m
            child = node.children[i]
            extend(rightBBox, self.toBBox(child) if node.leaf else child.bbox)
            margin += bboxMargin(rightBBox)

        return margin

    def _build(self, items, left, right, height):
        N, M = (right - left + 1, self.maxEntries)

        if N <= M:
            # reached leaf level return leaf
            node = Node(children=items[left: right + 1], height=1, bbox=None, leaf=True)
            calcBBox(node, self.toBBox)
            return node

        if not height:
            # target height of the bulk-loaded self
            height = int(math.ceil(math.log(N) / math.log(M)))

            # target number of root entries to maximize storage utilization
            M = int(math.ceil(N / float(math.pow(M, height - 1))))

        # TODO eliminate recursion?
        node = Node(children=[], height=height, bbox=None)

        # split the items into M mostly square tiles
        N2 = int(math.ceil(N / float(M)))
        N1 = N2 * int(math.ceil(math.sqrt(M)))

        multiSelect(items, left, right, N1, self.compareMinX)

        i = left
        while i <= right:
            right2 = min(i + N1 - 1, right)
            multiSelect(items, i, right2, N2, self.compareMinY)

            j = i
            while j <= right2:
                right3 = min(j + N2 - 1, right2)
                # pack each entry recursively
                node.children.append(self._build(items, j, right3, height - 1))
                j += N2

            # increment
            i += N1

        calcBBox(node, self.toBBox)

        return node

    def _insert(self, item, level, isNode=False):
        bbox = item.bbox if isNode  else self.toBBox(item)
        insertPath = []

        # find the best node for accommodating the item, saving all nodes along the path too
        node = _chooseSubtree(bbox, self.data, level, insertPath)

        # put the item into the node
        node.children.append(item)
        extend(node.bbox, bbox)

        # split on node overflow propagate upwards if necessary
        while level >= 0:
            if len(insertPath[level].children) > self.maxEntries:
                self._split(insertPath, level)
                level -= 1
            else:
                break

        # adjust bboxes along the insertion path
        _adjustParentBBoxes(bbox, insertPath, level)


def _chooseSubtree(bbox, node, level, path):
    """
    choose sub tree
    :param bbox:
    :param node:
    :param level:
    :param path:
    :return:
    """
    while True:
        path.append(node)

        if node.leaf or (len(path) - 1 == level):
            break

        targetNode = Node(children=[])
        minArea = minEnlargement = float("inf")

        for i in xrange(node.size):
            child = node.children[i]
            area = bboxArea(child.bbox)
            enlargement = enlargedArea(bbox, child.bbox) - area

            # choose entry with the least area enlargement
            if enlargement < minEnlargement:
                minEnlargement = enlargement
                minArea = min(area, minArea)
                targetNode = child

            elif enlargement == minEnlargement:
                # otherwise choose one with the smallest area
                if area < minArea:
                    minArea, targetNode = area, child

        node = targetNode

    return node


def _adjustParentBBoxes(bbox, path, level):
    """
    adjust bboxes along the given tree path
    :param bbox:
    :param path:
    :param level:
    :return:
    """
    for i in xrange(level, 0 - 1, -1):
        extend(path[i].bbox, bbox)


def _all(node, result):
    nodesToSearch = []
    while node:
        if node.leaf:
            result.extend(node.children)
        else:
            nodesToSearch.extend(node.children)
        node = nodesToSearch.pop() if nodesToSearch else None
    return result


def toBBox(item):
    return item


def compareMinX(a, b):
    """
    compare min x
    :param a:
    :param b:
    :return:
    """
    return comparator(a[0], b[0])


def compareMinY(a, b):
    """
    compare min y
    :param a:
    :param b:
    :return:
    """
    return comparator(a[1], b[1])


def calcBBox(node, toBBox):
    """
    calculate node's bbox from bboxes of its children
    :param node:
    :param toBBox:
    :return:
    """
    node.bbox = distBBox(node, 0, node.size, toBBox)


def distBBox(node, k, p, toBBox):
    """
    min bounding rectangle of node children from k to p-1
    :param node:
    :param k:
    :param p:
    :param toBBox:
    :return:
    """
    bbox = empty()

    for i in xrange(k, p):
        child = node.children[i]
        extend(bbox, toBBox(child) if node.leaf else child.bbox)
    return bbox


def extend(a, b):
    """
    extend
    :param a:
    :param b:
    :return:
    """
    a[0] = min(a[0], b[0])
    a[1] = min(a[1], b[1])
    a[2] = max(a[2], b[2])
    a[3] = max(a[3], b[3])
    return a


def compareNodeMinX(a, b):
    """
    compare min x
    :param a:
    :param b:
    :return:
    """
    return comparator(a.bbox[0], b.bbox[0])


def compareNodeMinY(a, b):
    """
    compare min y
    :param a:
    :param b:
    :return:
    """
    return comparator(a.bbox[1], b.bbox[1])


def comparator(x, y):
    """
    default comparator
    :param x:
    :param y:
    :return:
    """
    if x < y:
        return -1
    elif x > y:
        return 1
    return 0


def bboxArea(a):
    """
    box area
    :param a:
    :return:
    """
    return (a[2] - a[0]) * (a[3] - a[1])


def bboxMargin(a):
    """
    box margin
    :param a:
    :return:
    """
    return (a[2] - a[0]) + (a[3] - a[1])


def enlargedArea(a, b):
    """
    enlarge area
    :param a:
    :param b:
    :return:
    """
    mx2 = b[2] if b[2] > a[2] else a[2]
    mx3 = b[3] if b[3] > a[3] else a[3]

    mn0 = b[0] if b[0] < a[0] else a[0]
    mn1 = b[1] if b[1] < a[1] else a[1]
    return (mx2 - mn0) * (mx3 - mn1)


def intersectionArea(a, b):
    """
    intersect area
    :param a:
    :param b:
    :return:
    """
    minX, minY, maxX, maxY = max(a[0], b[0]), max(a[1], b[1]), \
                             min(a[2], b[2]), min(a[3], b[3])
    return max(0, maxX - minX) * max(0, maxY - minY)


def contains(a, b):
    """
    contains
    :param a:
    :param b:
    :return:
    """
    return a[0] <= b[0] and \
           a[1] <= b[1] and \
           b[2] <= a[2] and \
           b[3] <= a[3]


def intersects(a, b):
    """
    intersects
    :param a:
    :param b:
    :return:
    """
    return b[0] <= a[2] and \
           b[1] <= a[3] and \
           b[2] >= a[0] and \
           b[3] >= a[1]


def multiSelect(arr, left, right, n, compare):
    """
    sort an array so that items come in groups
    of n unsorted items, with groups sorted between each other
    combines selection algorithm with binary divide & conquer approach
    :param arr:
    :param left:
    :param right:
    :param n:
    :param compare:
    :return:
    """
    stack = [left, right]

    while stack:
        right = stack.pop()
        left = stack.pop()
        if right - left <= n:
            continue

        mid = left + int(math.ceil((right - left) / float(n) / 2.0)) * n
        select(arr, left, right, mid, compare)
        stack.extend([left, mid, mid, right])


def select(arr, left, right, k, compare):
    """
    sort array between left and right (inclusive) so that the
    smallest k elements come first (unordered)
    Floyd-Rivest selection algorithm
    :param arr:
    :param left:
    :param right:
    :param k:
    :param compare:
    :return:
    """
    while right > left:
        if right - left > 600:
            n = float(right - left + 1)
            i = k - left + 1
            z = math.log(n)
            s = 0.5 * math.exp(2 * z / 3.0)
            sd = 0.5 * math.sqrt(z * s * (n - s) / n) * (-1 if i - n / 2.0 < 0 else 1)
            newLeft = int(max(left, math.floor(k - i * s / n + sd)))
            newRight = int(min(right, math.floor(k + (n - i) * s / n + sd)))
            select(arr, newLeft, newRight, k, compare)

        t = arr[k]
        i = left
        j = right

        swap(arr, left, k)
        if compare(arr[right], t) > 0:
            swap(arr, left, right)

        while i < j:
            swap(arr, i, j)
            i += 1
            j -= 1
            while compare(arr[i], t) < 0:
                i += 1

            while compare(arr[j], t) > 0:
                j -= 1

        if compare(arr[left], t) == 0:
            swap(arr, left, j)

        else:
            j += 1
            swap(arr, j, right)

        if j <= k:
            left = j + 1

        if k <= j:
            right = j - 1


def swap(arr, i, j):
    """
    swap
    :param arr:
    :param i:
    :param j:
    :return:
    """
    arr[i], arr[j] = arr[j], arr[i]
