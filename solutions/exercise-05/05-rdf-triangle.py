#!/usr/bin/env python3

import argparse
import gzip
from graphs import Graph, io


def number_of_triangles(graph, predicate):
    triangles = 0

    for x in graph.vertices:
        for (p, y) in graph.edges[x]:
            if p != predicate:
                continue

            for (q, z) in graph.edges[y]:
                if q != predicate:
                    continue

                if (predicate, x) in graph.edges[z]:
                    if x != y and y != z and x != z:
                        #print('{} -> {} -> {} -> {}'.format(x, y, z, x))
                        triangles += 1

    return triangles


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Count number of triangles "
                                                  "along a given predicate of "
                                                  "an RDF graph"))
    parser.add_argument('input',
                        help='path to input graph')
    parser.add_argument('predicate',
                        help='predicate to follow')
    args = parser.parse_args()

    graph = None
    with gzip.open(args.input, 'rt') as infile:
        graph = io.read_ntriples_graph(infile)

    print('{} triangles'.format(number_of_triangles(graph, args.predicate)))
