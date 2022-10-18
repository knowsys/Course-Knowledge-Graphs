#!/usr/bin/env python3

import sys


def min_degree_vertices(filename):
    # a set to hold the edges we've already seen
    known_edges = set()
    # read the input file
    with open(filename, "r") as input_file:
        # first line has the number of vertices
        vertices = int(input_file.readline())
        # we keep only the degree sequence in memory
        degrees = [0] * vertices

        for line in input_file:
            # for every edge in the file
            source, target = line.split(" ")
            source = int(source)
            target = int(target)
            edge = (source, target)

            # check if we've seen this edge before
            if edge in known_edges:
                # we've already seen this edge, skip it
                continue
            known_edges.add(edge)
            # increment the degree of the source vertex
            degrees[int(target)] += 1

    # now we have seen every edge, find the vertices with maximal
    # degree
    result = [
        vertex for (vertex, degree) in enumerate(degrees) if degree == min(degrees)
    ]
    print(min(degrees), result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} graph.txt".format(sys.argv[0]))
        sys.exit(1)

    min_degree_vertices(sys.argv[1])
