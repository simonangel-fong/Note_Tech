# DSA - Graph

[Back](../../index.md)

- [DSA - Graph](#dsa---graph)
  - [Graph](#graph)
  - [Terminology](#terminology)
  - [Representation of Graphs](#representation-of-graphs)
  - [Adjacency Matrix](#adjacency-matrix)
  - [Adjacency List](#adjacency-list)
    - [Implement: Graph using Adjacency List](#implement-graph-using-adjacency-list)

---

## Graph

- `Graph`

  - a **non-linear data structure** consisting of `vertices` and `edges`.
  - A graph is an ordered pair `G=(V,E)` comprising:

    - `V`, a set of `vertices` (also called **nodes** or **points**);
    - `E`, a set of `edges` (also called **links** or **lines**), which are **unordered pairs of vertices** (that is, an edge is associated with two distinct vertices). Each edge is **a tuple (v,w)** where w,v∈V

- **Components of a Graph**

  - `Vertex / Vertices`

    - also referred to as `node / nodes`.
    - the **fundamental units** of the graph.

    - `Key`

      - the **name** of a `vertex`

    - `Payload`

      - additional information that a vertex has.

  - `Edges`

    - also referred to as `lines`, `links`, or `arcs`.
    - **lines or arcs** that **connect any two nodes** in the graph show that there is a relationship between them.
    - Edges may be **one-way** or **two-way**.

## Terminology

- `Weight`

  - a **cost** to go from one vertex to another.

- `Path`

  - a **sequence of vertices** that are connected by edges.
  - Formally we would define a path as w1,w2,...,wn  such that (wi,wi+1)∈E for all 1≤i≤n−1.

- `unweighted path length`

  - the **number of edges** in the path, specifically n−1.

- `weighted path length`

  - **the sum of the weights** of all the edges in the path.

- `Subgraph`

  - A subgraph **s** is a set of edges **e** and vertices **v** such that **e⊂E and v⊂V**

- `Undirected Graph`

  - A graph in which **edges do not have any direction**.
  - The nodes of a undirected graphs are **unordered pairs** in the definition of every edge.

- `Directed Graph`

  - aka `digraph`
  - A graph in which **edge has direction**.
  - The nodes of a directed graph are **ordered pairs** in the definition of every edge.

- `cycle graph`

  - a **directed graph** is a path that **starts and ends at the same vertex**.

- `Cyclic Graph`

  - A graph containing **at least one cycle** is known as a Cyclic graph.

- `acyclic graph`

  - A graph with no cycles.

- `directed acyclic graph` or `DAG`
  - A directed graph with no cycles

---

## Representation of Graphs

- There are two ways to store a graph:

  - Adjacency Matrix
  - Adjacency List

| Action           | Adjacency Matrix | Adjacency List |
| ---------------- | ---------------- | -------------- |
| Adding Edge      | O(1)             | O(1)           |
| Removing an edge | O(1)             | O(N)           |
| Initializing     | O(N\*N)          | O(N)           |

---

## Adjacency Matrix

- `Adjacency Matrix`
  - In this method, the graph is stored in the form of the **2D matrix** where rows and columns denote vertices. Each entry in the matrix represents the weight of the edge between those vertices.

![matrix](./pic/adjacency_mat1.jpg)

- In this matrix implementation, each of the **rows** and **columns** represent a `vertex` in the graph.

- The value stored in the cell at the intersection of **row v** and **column w** indicates if there is an edge from **vertex v** to **vertex w**.

- When two vertices are connected by an edge, we say that they are **adjacent**.

- `Sparse matrix`

  - most of the cells in the matrix are **empty**

- `Full matrix`

  - A matrix is **full** when every vertex is connected to every other vertex.

- **Advantage** of the adjacency matrix

  - good for **small graphs** it is easy to see which nodes are connected to other nodes.
  - a good implementation for a graph when the **number of edges is large**.

    - Since there is one row and one column for every vertex in the graph, the number of edges required to fill the matrix is **|V|^2**.

  - A matrix is not a very efficient way to store sparse data.

---

## Adjacency List

- `Adjacency List`

  - This graph is represented as **a collection of linked lists**. There is an **array** of pointer which points to the edges connected to that vertex.

- In an adjacency list implementation we **keep a master list of all the vertices** in the Graph object and then **each vertex object** in the graph maintains a list of the other vertices that it is connected to.

- In our implementation of the Vertex class we will use a **dictionary** rather than a list where the dictionary keys are the vertices, and the values are the weights.

- **Advantage** of the adjacency list implementation
  - allows us to compactly represent a **sparse graph**.
  - allows us to easily **find all the links** that are directly connected to a particular vertex.

![list](./pic/adjacency_list.jpg)

---

### Implement: Graph using Adjacency List

- Vertex

```py
class Vertex(object):
    '''Implement vertex'''

    def __init__(self, key):
        self.id = key   # key of current vertex
        self.neighbor = {}  # initialize neighbors of current vertex

    def __str__(self):
        return 'Vertex {0} connects to {1}'.format(self.id, str([x.id for x in self.neighbor]))

    def get_id(self):
        return self.id

    def add_neighbor(self, vertex, weight):
        '''add a target vertex with specific weight'''
        # Note that the key here is vertex, an object
        self.neighbor[vertex] = weight
        # set weight for both current and target vertex
        vertex.neighbor[self] = weight

    def get_neighbors(self):
        '''get all neighbors'''
        return [k for k in self.neighbor.keys()]

    def get_weight(self, target_vertex):
        '''get weight from current to target vertex'''

        # if target is in the neighbors
        if target_vertex in self.neighbor:
            return self.neighbor[target_vertex]
        else:
            return None
```

- Graph

```py
class Graph(object):
    def __init__(self) -> None:
        self.vertice = {}

    def add_vertex(self, key):
        '''create a new vertex with key'''
        new_vertext = Vertex(key)       # create a new vertex
        self.vertice[key] = new_vertext
        return new_vertext

    def get_vertex(self, key):
        if key in self.vertice.keys():
            return self.vertice[key]
        else:
            None

    def add_edge(self, from_key, to_key, cost=0):
        '''add edge'''
        # if from key does not exist, then create a new vertex
        if from_key not in self.vertice:
            self.add_vertex(from_key)

        # if to key does not exist, then create a new vertex
        if to_key not in self.vertice:
            self.add_vertex(to_key)

        self.vertice[from_key].add_neighbor(self.vertice[to_key], cost)

    def get_all_vertice(self):
        '''get all vertice'''
        return [k for k in self.vertice.keys()]

    def __iter__(self):
        return iter(self.vertList.values())

    def __contains__(self, key):
        return key in self.vertice
```

- Test

```py
g = Graph()

for i in range(6):
    g.add_vertex(i)

print(g.get_vertex(0))  # Vertex 0 connects to []
g.add_edge(0, 1, 1)
g.add_edge(0, 2, 2)
g.add_edge(0, 3, 3)
g.add_edge(0, 7, 3)
print(g.get_vertex(0))      # Vertex 0 connects to [1, 2, 3, 7]
print(g.get_vertex(1))      # Vertex 1 connects to [0]
print(g.get_vertex(2))      # Vertex 2 connects to [0]
print(g.get_vertex(3))      # Vertex 3 connects to [0]
print(g.get_vertex(0))      # Vertex 0 connects to [1, 2, 3, 7]

g.get_all_vertice()     # [0, 1, 2, 3, 4, 5, 7]

3 in g      # True
10 in g     # False
```

---

[TOP](#dsa---graph)
