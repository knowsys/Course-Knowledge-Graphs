#!/usr/bin/env python3

import argparse
from graphs import Graph


def read_edge_list_graph(infile):
    """Parse an edge-list formatted graph from `infile`."""
    num_vertices = int(infile.readline())
    graph = Graph(range(num_vertices))

    for line in infile:
        source, target = line.split(" ")
        graph.add_edge(int(source), int(target))

    return graph


def write_metis_graph(outfile, graph):
    """Write `graph` to `outfile`, in METIS format."""
    print("{} {}".format(graph.number_of_vertices, graph.number_of_edges), file=outfile)

    for source in graph.vertices:
        if graph.out_degree(source) > 0:
            print(
                source,  # source vertex first
                *graph.edges[source],  # then all target vertices
                sep=" ",  # separated by a space
                file=outfile
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert edge-list graph to METIS format"
    )
    parser.add_argument("input", help="path to input graph")
    parser.add_argument("output", help="path to output graph")
    args = parser.parse_args()

    graph = None
    with open(args.input, "r") as infile:
        graph = read_edge_list_graph(infile)

    with open(args.output, "w") as outfile:
        write_metis_graph(outfile, graph)
