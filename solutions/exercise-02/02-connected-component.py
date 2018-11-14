#!/usr/bin/env python3

import gzip
import argparse

from graphs import Graph, io


def extract_connected_component(graph, needle):
    subgraph = Graph([needle])
    queue = [needle]

    step = 0
    while queue:
        vertex = queue.pop(0)
        step += 1
        if step % 10000 == 0:
            print(len(queue), repr(queue[0:min(5,len(queue))]))
            step = 0
        for (pred, obj) in graph.edges[vertex]:
            # examine all neighbours of vertex
            if not obj in subgraph.vertices:
                # we haven't visited this vertex before
                subgraph.add_vertex(obj)
                subgraph.add_edge(vertex, obj, label=pred)
                # we also needle to consider all new neighbours of `obj`
                queue.append(obj)
            elif (pred, obj) not in subgraph.edges[vertex]:
                # we already have `obj`, but not this edge
                subgraph.add_edge(vertex, obj, label=pred)

    return subgraph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='extract a connected component from an N-Triples graph')
    parser.add_argument('input',
                        help='path to input graph')
    parser.add_argument('output',
                        help='path to output graph')
    parser.add_argument('needle',
                        help='node to identify the connected component by')

    args = parser.parse_args()

    graph = None
    with gzip.open(args.input, 'rt') as infile:
        graph = io.read_ntriples_graph(infile)

    print('finished reading input')

    subgraph = extract_connected_component(graph, args.needle)

    print('starting to write output')

    with gzip.open(args.output, 'wt') as outfile:
        io.write_ntriples_graph(outfile, subgraph)
