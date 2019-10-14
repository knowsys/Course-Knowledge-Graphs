#!/usr/bin/env python3

import argparse
import networkx
from operator import itemgetter
from collections import defaultdict


def ranks(ranking):
    idx = 0
    worst = float('inf')

    for label, rank in sorted(ranking.items(),
                            key=itemgetter(1),
                            reverse=True):
        if rank < worst:
            idx += 1
            worst = rank

        yield (idx, label)


def read_nx_digraph_from_metis_file(graphfile, dictfile=None):
    vertices_edges = graphfile.readline().split(' ')
    num_vertices = int(vertices_edges[0])
    num_edges = int(vertices_edges[1])

    labels = {}

    if dictfile is not None:
        for line in dictfile:
            vertex, label = line.split(',', 1)
            labels[int(vertex)] = label.strip()[1:-1]
    else:
        labels = defaultdict(lambda label: label)

    def edgelist():
        for line in graphfile:
            vertices = [labels[int(vertex)] for vertex in line.split(' ')]
            source = vertices[0]

            for target in vertices[1:]:
                yield (source, target)

    return networkx.from_edgelist(edgelist(),
                                  create_using=networkx.DiGraph)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Compute PageRank for a given graph"))
    parser.add_argument('input',
                        help='path to input graph')
    parser.add_argument('dict',
                        help='path to input dict')
    args = parser.parse_args()

    graph = None

    with open(args.input, 'r') as infile:
        with open(args.dict, 'r') as dictfile:
            graph = read_nx_digraph_from_metis_file(infile, dictfile)

    ranking = ranks(networkx.pagerank_scipy(graph))

    for rank, label in ranking:
        print('{:5d}. {}'.format(rank, label))
