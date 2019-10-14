from . import Graph
from collections import defaultdict


def number_of_triangles(graph):
    triangles = 0

    for x in graph.vertices:
        for y in graph.edges[x]:
            for z in graph.edges[y]:
                if x in graph.edges[z]:
                    print('{} -> {} -> {} -> {}'.format(x, y, z, x))
                    triangles += 1

    return triangles
