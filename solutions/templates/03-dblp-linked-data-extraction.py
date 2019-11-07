#!/usr/bin/env python3

import gzip
import time
import argparse
import requests

from graphs import Graph, io

DBLP_AUTHOR_OF = 'https://dblp.org/rdf/schema-2017-04-18#authorOf'
DBLP_AUTHORED_BY = 'https://dblp.org/rdf/schema-2017-04-18#authoredBy'


"""
Returns a Graph instance that represents the graph of the NT-file in the DBLP uri.
@note: in the exercise sheet, there is a commment related to HTTP 429 status code Retry-After.
This behaviour was changed in DBLP servers.
@note use time.sleep(2) to avoid requests.exceptions.ConnectionError
@param (string) iri to be retrieved from dblp
@returns an instance of Graph
@hint: use {@code io.read_ntriples_graph} to return an instance of Graph.
"""
def _get_ntriples_from_linked_data(iri):
    request = requests.get('{}.nt'.format(iri))
    time.sleep(1)

    if request.status_code == 429:
        delay = int(request.headers['Retry-After'])
        print('got 429, sleeping for {} seconds'.format(delay))
        time.sleep(delay)
        return _get_ntriples_from_linked_data(iri)

    #edit the next line
    return io.read_ntriples_graph(request.text.splitlines())

"""
(a) get the graph of publications of the author
(b) check if there is only one author
(c) return single_autor_papers
"""
def extract_single_author_papers(author):
    papers = set([])
    single_author_papers = set([])

    #get the graph of the author
    fragment = _get_ntriples_from_linked_data(author)

    # for every (property, object) from author's node
    # if the predicate is DBLP_AUTHOR_OF then save the paper
    for (prop, obj) in fragment.edges[author]:

        # do something
        pass

    #for every paper
    #   get the graph of the paper
    #   if it is a single autor paper, then we save it
    while papers:
        paper = papers.pop()

        fragment = _get_ntriples_from_linked_data(paper)
        authors = 0

        # do something

    #return
    return single_author_papers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('finds all single-author publications by a given '
                     'person an DBLP'))
    parser.add_argument('author',
                        metavar='IRI',
                        help='starting point for the extraction')


    args = parser.parse_args()

    for paper in extract_single_author_papers(args.author):
        print(paper)
