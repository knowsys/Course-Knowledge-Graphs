#!/usr/bin/env python3

import json
import argparse
import requests
import itertools
from collections import defaultdict
from graphs import Graph, io


SPARQL_ENDPOINT = 'https://query.wikidata.org/sparql'
QUERY = """#TOOL:tud-kbs-example-subgraph-extractor
SELECT ?v ?vLabel ?w ?wLabel WHERE {
  ?v wdt:P1344/^wdt:P2522 ?w .
  FILTER (?v != ?w)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  }
"""


def counter():
    c = itertools.count(1)
    def step():
        return next(c)

    return step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Extract tournament winner/"
                                                  "participant subgraph from"
                                                  "Wikidata"))
    parser.add_argument('output',
                        help='path to output graph')
    parser.add_argument('dict',
                        help='path to output dictionary')
    args = parser.parse_args()

    request = requests.get(SPARQL_ENDPOINT,
                           params={'query': QUERY,
                                   'format': 'json'})
    request.raise_for_status()
    results = request.json()['results']['bindings']

    ids = defaultdict(counter())
    labels = {}
    edges = set([])

    for binding in results:
        v = ids[binding['v']['value']]
        labels[v] = binding['vLabel']['value']
        w = ids[binding['w']['value']]
        labels[w] = binding['wLabel']['value']

        edges |= {(w, v)}

    graph = Graph(vertices=ids.values())

    for (w, v) in edges:
        graph.add_edge(w, v)

    with open(args.output, 'w') as metis:
        io.write_metis_graph(metis, graph)

    with open(args.dict, 'w') as dictionary:
        for vertex_id, label in labels.items():
            print('{},"{}"'.format(vertex_id, label),
                  file=dictionary)
