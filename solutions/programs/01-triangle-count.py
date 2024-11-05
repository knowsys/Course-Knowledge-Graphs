#!/usr/bin/env python3

import argparse
from graphs import Graph, io


def number_of_triangles(graph):
    triangles = 0

    for x in graph.vertices:
        for y in graph.edges[x]:
            for z in graph.edges[y]:
                if x in graph.edges[z]:
                    if x == y or y == z or x == z:
                        continue
                    # print("{} -> {} -> {} -> {}".format(x, y, z, x))
                    triangles += 1

    return triangles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count triangles in a graph")
    parser.add_argument("input", help="path to input graph")
    args = parser.parse_args()

    graph = None
    with open(args.input, "r") as infile:
        graph = io.read_edge_list_graph(infile)

    print("{} triangles".format(number_of_triangles(graph)))
