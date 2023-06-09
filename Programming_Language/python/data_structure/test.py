class Vertex(object):

    def __init__(self, key) -> None:
        self.id = key
        self.connectedTo = {}

    def addNeighbour(self, node, weight):
        self.connectedTo[node.id] = weight
        print(self.connectedTo)

    def __str__(self) -> str:
        return str(self.id) + ' connectedTo: ' + str([x for x in self.connectedTo])


a = Vertex('a')
b = Vertex('b')
c = Vertex('c')
a.addNeighbour(b, 3)
a.addNeighbour(c, 1)
print(b.connectedTo)
