#!/usr/bin/env python3

import string
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.entities import entitydefs, codepoint2name

PREFIX_PERSON = 'http://dblp.uni-trier.de/pers/{}/{}'
DBLP_COAUTHOR_WITH = 'https://dblp.uni-trier.de/rdf/schema-2017-04-18#coAuthorWith'

def uri_for_author(author):
    def _map_char(x):
        if x.isalnum():
            return x
        elif x == ' ':
            return '_'
        else:
            return '='

    def _is_hidden_suffix(x):
        if len(x) == 0:
            return False

        if not any([x[i].isdigit()
                    for i in range(min(len(x), 4))]):
            return False

        return len(x) <= 4

    if ' ' not in author:
        result = ''.join([_map_char(c) for c in author])
        result += ':'
        return PREFIX_PERSON.format(result[0].lower(), result)

    fname, lname = author.rsplit(' ', maxsplit=1)

    if (lname in ['Jr.', 'II', 'III', 'IV'] or
        _is_hidden_suffix(lname)):
        if ' ' in fname:
            fname, tmp = fname.rsplit(' ', maxsplit=1)
        else:
            tmp = fname
            fname = None
        lname = '{} {}'.format(tmp, lname)

    if lname:
        result = ''.join([_map_char(c) for c in lname])
    result += ':'
    if fname:
        result += ''.join([_map_char(c) for c in fname])
    return PREFIX_PERSON.format(lname[0].lower(), result)


def handle_publication(graph, element):
    key = element.get('key')
    authors = element.findall('author')

    if len(authors) <= 1:
        # single author, ignore
        return

    for a, b in ((a.text, b.text)
                   for a in authors
                   for b in authors
                   if a != b):
        graph[a] |= {b}


HANDLERS = {
    'phdthesis': handle_publication,
    'mastersthesis': handle_publication,
    'article': handle_publication,
    'inproceedings': handle_publication,
    'proceedings': handle_publication,
    'book': handle_publication,
    'incollection': handle_publication,
    }


PUBLICATIONS = HANDLERS.keys()


def coauthor_graph_from_dblp(infile):
    graph = defaultdict(set)
    parser = ET.XMLParser()

    for entity, value in entitydefs.items():
        parser.entity[entity] = value

    for _, element in ET.iterparse(infile, parser=parser):
        if element.tag in PUBLICATIONS:
            HANDLERS[element.tag](graph, element)
            element.clear()
    return graph


def write_rdf_to_file(outfile, graph):
    entities = str.maketrans({codepoint: '&{};'.format(name)
                              for codepoint, name in codepoint2name.items()})
    for author, coauthors in graph.items():
        subj = uri_for_author(author.translate(entities))
        for coauthor in coauthors:
            obj = uri_for_author(coauthor.translate(entities))

            print('<{}> <{}> <{}> .'.format(subj, DBLP_COAUTHOR_WITH, obj),
                  file=outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract the coauthor graph from the DBLP dump')
    parser.add_argument('input',
                        help='path to dblp.xml')
    parser.add_argument('output',
                        help='path to output graph')

    args = parser.parse_args()
    graph = coauthor_graph_from_dblp(args.input)

    with open(args.output, 'w') as outfile:
        write_rdf_to_file(outfile, graph)
