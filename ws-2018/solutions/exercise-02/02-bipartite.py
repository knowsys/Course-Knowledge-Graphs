#!/usr/bin/env python3

import gzip
import argparse

from graphs import Graph, io


def graph_is_bipartite(graph):
    vertices = graph.vertices

    while vertices:
        first = vertices.pop()
        queue = {first}
        colours = {first: True}

        while queue:
            vertex = queue.pop()
            colour = colours[vertex]

            for _, neighbour in graph.edges[vertex]:
                if neighbour in colours:
                    if colours[neighbour] == colour:
                        return False
                    else:
                        continue
                colours[neighbour] = not colour
                queue |= {neighbour}
        vertices -= set(colours.keys())

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='determine whether a graph in N-Triples format is bipartite')
    parser.add_argument('input',
                        help='path to input graph')

    args = parser.parse_args()

    graph = None
    with gzip.open(args.input, 'rt') as infile:
        graph = io.read_ntriples_graph(infile)

    print('finished reading input')

    if graph_is_bipartite(graph):
        print('graph is bipartite')
    else:
        print('graph is not bipartite')
