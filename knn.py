from node import Node
from heap import Heap
from collections import namedtuple

QObj = namedtuple('QObj', ('dist', 'node', 'leaf'))


def KNN(tree, query, limit, score, predicate):
    node = tree.data
    result = []
    queue = Heap()
    stop = False

    while node and (not stop):
        for child in node.children:
            if isinstance(child, Node):
                dist = score(query, child.bbox)
            else:
                dist = score(query, child)
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
