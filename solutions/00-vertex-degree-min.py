#!/usr/bin/env python3

import sys

def min_degree_vertices(filename):
    # read the input file
    with open(filename, 'r') as input_file:
        vertices = int(input_file.readline())  # first line has the
                                               # number of vertices
        degrees = [0] * vertices               # we keep only the
                                               # degree sequence in
                                               # memory

        for line in input_file:
            source, target = line.split()         # for every edge in
                                                  # the file
            degrees[int(target)] += 1             # increment the
                                                  # degree of the
                                                  # target vertex

    # now we have seen every edge, find the vertices with minimal
    # degree
    result = [vertex
              for (vertex, degree) in enumerate(degrees)
              if degree == min(degrees)]
    print(min(degrees), result)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} graph.txt'.format(sys.argv[0]))
        sys.exit(1)

    max_degree_vertices(sys.argv[1])
