#!/usr/bin/env python3

import gzip
import time
import argparse
import requests

from graphs import Graph, io

DBLP_AUTHOR_OF = 'https://dblp.org/rdf/schema#authorOf'
DBLP_AUTHORED_BY = 'https://dblp.org/rdf/schema#authoredBy'


class RedirectError(RuntimeError):
    def __init__(self, iri):
        self.iri = iri

    def __repr__(self):
        return f"<Redirect [{self.iri}]>"


def _get_ntriples_from_linked_data(iri):
    request = requests.get(f"{iri}.nt", allow_redirects=False)

    if request.status_code == 429:
        # we're making too many requests, wait a bit
        delay = int(request.headers['Retry-After'])
        print("got 429, sleeping for {delay} seconds")
        time.sleep(delay)
        return _get_ntriples_from_linked_data(iri)

    if request.is_redirect:
        # this is a redirect, find the new IRI
        iri = requests.head(f"{iri}.nt", allow_redirects=True).url

        if iri.endswith('.nt'):
            iri = iri[:-len('.nt')]
        raise RedirectError(iri)

    return io.read_ntriples_graph(request.text.splitlines())


def extract_single_author_papers(author):
    papers = set([])
    single_author_papers = set([])
    fragment = _get_ntriples_from_linked_data(author)

    for (prop, obj) in fragment.edges[author]:
        if prop != DBLP_AUTHOR_OF:
            continue

        papers |= {obj}

    while papers:
        paper = papers.pop()

        fragment = _get_ntriples_from_linked_data(paper)
        authors = 0

        for (prop, _) in fragment.edges[paper]:
            if prop == DBLP_AUTHORED_BY:
                authors += 1

        if authors == 1:
            single_author_papers |= {paper}

    return single_author_papers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=('finds all single-author publications by a given '
                     'person an DBLP'))
    parser.add_argument('author',
                        metavar='IRI',
                        help='starting point for the extraction')


    args = parser.parse_args()
    papers = {}
    try:
        papers = extract_single_author_papers(args.author)
    except RedirectError as e:
        # got redirected to new IRI, follow it
        papers = extract_single_author_papers(e.iri)

    for paper in papers:
        print(paper)
