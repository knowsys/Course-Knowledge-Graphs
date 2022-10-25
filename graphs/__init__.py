from collections import defaultdict


class Graph:
    def __init__(self, vertices, edges=None):
        self.vertices = set(vertices)
        self.edges = defaultdict(list)

        if edges is not None:
            for (source, target) in edges:
                self.add_edge(source, target)

    def add_vertex(self, vertex):
        "add a vertex `vertex` to the graph"
        if vertex not in self.vertices:
            self.vertices |= {vertex}

    def add_edge(self, source, target, label=None):
        "add an edge from `source` to `target` to the graph"
        if label is None:
            self.edges[source].append(target)
        else:
            self.edges[source].append((label, target))

    @property
    def number_of_vertices(self):
        "return the number of edges in the graph"
        return len(self.vertices)

    @property
    def number_of_edges(self):
        "return the number of edges in the graph"
        return sum((len(self.edges[source]) for source in self.vertices))

    def out_degree(self, vertex):
        if vertex not in self.vertices:
            raise ValueError("Vertex {} is invalid".format(vertex))

        return len(self.edges[vertex])

    def in_degree(self, vertex):
        if vertex not in self.vertices:
            raise ValueError("Vertex {} is invalid".format(vertex))

        return sum(
            (1 if vertex in self.edges[source] else 0 for source in self.vertices)
        )

    def __repr__(self):
        "generate a representation (in edge-list format) of the graph"
        result = "{}\n".format(len(self.vertices))

        for source in self.vertices:
            for target in self.edges[source]:
                result += "{} {}\n".format(source, target)

        return result
