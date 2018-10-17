#!/usr/bin/env python3

import random
import argparse


def write_graph_to_file(outfile, graph):
    print(len(graph['vertices']), file=outfile)

    for source, target in graph['edges']:
        print('{} {}'.format(source, target), file=outfile)


def generate_random_graph(vertices, edges, undirected):
    graph = {'vertices': range(vertices)}
    possible_edges = [(v, w)
                      for v in graph['vertices']
                      for w in graph['vertices']
                      if v != w]

    graph['edges'] = random.sample(possible_edges, edges)

    if undirected:
        backwards_edges = [(target, source)
                           for (source, target) in graph['edges']
                           if (target, source) not in graph['edges']]
        graph['edges'] += backwards_edges

    return graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random graphs')
    parser.add_argument('output',
                        help='path to output graph')
    parser.add_argument('vertices',
                        metavar='N',
                        help='number of vertices in the graph')
    parser.add_argument('edges',
                        metavar='M',
                        help='number of edges in the graph')
    parser.add_argument('--undirected', '-u',
                        action='store_true',
                        help='generate an undirected graph')

    args = parser.parse_args()

    with open(args.output, 'w') as outfile:
        write_graph_to_file(outfile,
                            generate_random_graph(vertices=int(args.vertices),
                                                  edges=int(args.edges),
                                                  undirected=args.undirected))
