__author__ = 'titus'

from box import empty


class Node(dict):
    """
    BST - Node
    """

    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__ = self

        if 'leaf' not in self:
            self.leaf = False

        if 'children' not in self:
            self.children = []

        if 'height' not in self:
            self.height = 1

        if 'bbox' not in self:
            self.bbox = empty()

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self

    def __getattr__(self, item):
        # only gets called if key is missing
        if item not in self.__dict__:
            raise Exception("invalid attribute")
        # return getattr(self, item)

    def __lt__(self, other):
        return 0

    def __le__(self, other):
        return 0

    def __gt__(self, other):
        return 0

    def __ge__(self, other):
        return 0

    def hasattr(self, attr):
        return attr in self.__dict__

    @property
    def size(self):
        return len(self.children)
