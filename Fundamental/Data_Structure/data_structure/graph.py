class Graph:
    def __init__(self) -> None:
        self.adj_list = {}

    def add_vertex(self, vertex):
        # check if the vertext in the graph already
        if vertex not in self.adj_list.keys():
            # if not, add vertex into the dict.
            # value is the adjacent vertice of this vertex.By default is empty
            self.adj_list[vertex] = []
            return True  # return true if the vertex has been added
        return False

    def add_edge(self, v1, v2):
        # Basically, just append both vertices of an edge into each other's adjacent_list.
        # check if both verteces exist before adding edge
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys():
            self.adj_list[v1].append(v2)
            self.adj_list[v2].append(v1)
            return True
        return False

    def remove_edge(self, v1, v2):
        # Basically, just remove both vertices of an edge from each other's adjacent_list.
        # check if both vertices exist
        if v1 in self.adj_list.keys() and v2 in self.adj_list.keys():
            # the reason of applying try except here is considering the situation:
            #   if no edge connects both vertices, that is,
            #   both vertices do not exist in each other's list. It will create ValueError.
            try:
                # if v2 is not an adjacent vetex of v1, and error will raise
                self.adj_list[v1].remove(v2)
                # if the above raise an error, which means v1 and v2 are no adjacent, then v1 does not need to remove.
                self.adj_list[v2].remove(v1)
            except ValueError:
                # pass here is that it donot need to do anything even no edge connecting both vertices.
                pass
            return True
        return False

    def remove_vertext(self, vertex):
        # Basically, remove each possible edges connecting with target vertex, then remove the target vertex.

        # check if vertex in adjacent list
        if vertex in self.adj_list.keys():
            # loop all adjacent vertices (other_vertex) of the target vertex,
            for other_vertex in self.adj_list[vertex]:
                # then remove target vertex from each adjacent vertex.
                self.adj_list[other_vertex].remove(vertex)
            # at last, remove the target vertex.
            del self.adj_list[vertex]
            return True
        return False

    def print_graph(self):
        for vertex in self.adj_list:
            print(vertex, ":", self.adj_list[vertex])


# my_graph = Graph()
# my_graph.add_vertex("A")
# my_graph.add_vertex("B")
# my_graph.add_vertex("C")    # a stand alone vertex

# my_graph.add_edge("A", "B")

# # will not create ValueError exception, due to the try...except block.
# my_graph.remove_edge("A", "C")

# my_graph.print_graph()

# remove vertex

my_graph = Graph()
my_graph.add_vertex("A")
my_graph.add_vertex("B")
my_graph.add_vertex("C")
my_graph.add_vertex("D")

my_graph.add_edge('A', 'B')
my_graph.add_edge('A', 'C')
my_graph.add_edge('A', 'D')
my_graph.add_edge('B', 'D')
my_graph.add_edge('C', 'D')

my_graph.print_graph()
# before remove vertex D
# A : ['B', 'C', 'D']
# B : ['A', 'D']
# C : ['A', 'D']
# D : ['A', 'B', 'C']


my_graph.remove_vertext("D")
my_graph.print_graph()
# after remove vertex D
# A : ['B', 'C']
# B : ['A']
# C : ['A']
