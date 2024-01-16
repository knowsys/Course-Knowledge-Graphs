#!/usr/bin/env python3

import argparse
import requests
import itertools
from collections import defaultdict
from graphs import Graph, io


# getting all the results will time out, so we do paging
PAGE_SIZE = 10000
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "tud-kbs-example-subgraph-extractor/0.0.1 (https://github.com/knowsys/Course-Knowledge-Graphs/)"
# first, in a subquery, get the v/w pairs in a stable order and
# retrieve a page of those. then find the labels for these results.
QUERY = """#TOOL:tud-kbs-example-subgraph-extractor
SELECT DISTINCT ?v ?vLabel ?w ?wLabel WHERE {{
  {{ SELECT DISTINCT ?v ?w WHERE {{
    ?v wdt:P1344 ?tournament .
    ?tournament ^wdt:P2522 ?w .
    ?tournament wdt:P361* wd:Q170645 .
  }} ORDER BY ASC(?v) ASC(?w) LIMIT {limit} OFFSET {offset} }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .
    ?v rdfs:label ?vLabel .
    ?w rdfs:label ?wLabel .
  }}
}}
"""


def counter():
    c = itertools.count(1)

    def step():
        return next(c)

    return step


def paged(page):
    return QUERY.format(limit=PAGE_SIZE + 1, offset=(PAGE_SIZE + 1) * page)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Extract tournament winner/" "participant subgraph from" "Wikidata"
        )
    )
    parser.add_argument("output", help="path to output graph")
    parser.add_argument("dict", help="path to output dictionary")
    args = parser.parse_args()

    ids = defaultdict(counter())
    labels = {}
    edges = set([])
    done = False
    page = 0

    while not done:
        print("-!- getting page {}".format(page))
        request = requests.get(
            SPARQL_ENDPOINT,
            params={"query": paged(page), "format": "json"},
            headers={"user-agent": USER_AGENT},
        )
        request.raise_for_status()
        results = request.json()["results"]["bindings"]
        done = len(results) <= PAGE_SIZE
        page += 1

        for binding in results:
            v = ids[binding["v"]["value"]]
            labels[v] = binding["vLabel"]["value"]
            w = ids[binding["w"]["value"]]
            labels[w] = binding["wLabel"]["value"]

            edges |= {(w, v)}

    graph = Graph(vertices=ids.values())

    for w, v in edges:
        graph.add_edge(w, v)

    with open(args.output, "w") as metis:
        io.write_metis_graph(metis, graph)

    with open(args.dict, "w") as dictionary:
        for vertex_id, label in labels.items():
            print('{},"{}"'.format(vertex_id, label), file=dictionary)
