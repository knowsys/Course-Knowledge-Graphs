#!/usr/bin/env python3

import sys

def max_degree_vertices(filename):
    # read the input file
    with open(filename, 'r') as input_file:
        vertices = int(input_file.readline())  # first line has the
                                               # number of vertices
        degrees = [0] * vertices               # we keep only the
                                               # degree sequence in
                                               # memory

        for line in input_file:
            source, target = line.split(' ')      # for every edge in
                                                  # the file
            degrees[int(source)] += 1             # increment the
                                                  # degree of the
                                                  # source vertex

    # now we have seen every edge, find the vertices with maximal
    # degree
    extremal_degree = max(degrees)
    extremal_vertices = [vertex
                         for (vertex, degree) in enumerate(degrees)
                         if degree == extremal_degree]
    return extremal_degree, extremal_vertices


# the following code is only executed when this file is invoked on the
# command line, not on import
if __name__ == '__main__':
    if len(sys.argv) != 2:  # number of commandline argument is not 2
        # first argument is the name of the program file
        print('Usage: {} graph.txt'.format(sys.argv[0]))

    degree, vertices = max_degree_vertices(sys.argv[1])
    print(degree, vertices)
