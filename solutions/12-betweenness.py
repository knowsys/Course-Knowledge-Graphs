#!/usr/bin/env python3

import argparse
from networkit import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Compute Betweenness for a given graph")
    )
    parser.add_argument("input", help="path to input graph")
    parser.add_argument("dict", help="path to input dict")
    args = parser.parse_args()

    graph = None
    labels = {}

    with open(args.dict, "r") as dictfile:
        for line in dictfile:
            vertex, label = line.split(",", 1)
            labels[int(vertex)] = label.strip()[1:-1]

    graph = readGraph(args.input, Format.METIS)
    betweenness = centrality.Betweenness(graph)
    ranking = betweenness.run().ranking()

    for vertex, rank in ranking[:20]:
        print("{}. {}".format(rank, labels[int(vertex + 1)]))
