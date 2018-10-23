from . import Graph
from collections import defaultdict


def number_of_triangles(graph):
    triangles = 0

    for x in graph.vertices:
        for y in graph.edges[x]:
            triangles += sum((1 if x in graph.edges[z] else 0
                              for z in graph.edges[y]))

    return triangles
