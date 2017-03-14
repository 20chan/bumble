class Node():
    def __init__(self, loc=None):
        self.children = []
        self.loc = loc

    def __repr__(self):
        return '<{}>'.format(type(self).__name__)