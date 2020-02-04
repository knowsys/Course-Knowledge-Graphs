#!/usr/bin/env python3

import argparse
import networkx
from itertools import islice
from graphs.io import read_nx_digraph_from_metis_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Compute Girvan-Newman hierarchical clustering"))
    parser.add_argument('input',
                        help='path to input graph')
    parser.add_argument('dict',
                        help='path to input dict')
    parser.add_argument('k',
                        type=int,
                        help='level of the hierarchical clustering to print')
    args = parser.parse_args()

    graph = None

    with open(args.input, 'r') as infile:
        with open(args.dict, 'r') as dictfile:
            graph = read_nx_digraph_from_metis_file(infile, dictfile)

    clustering = networkx.community.girvan_newman(graph)

    level = list(islice(clustering, args.k, args.k + 1))[0]
    print('level {}, {} communities'.format(args.k, len(level)))
    for community in level:
        print(repr(sorted(community)))
