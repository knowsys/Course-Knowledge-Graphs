#!/usr/bin/env python3


import rdflib
import argparse
from datetime import datetime


DIRECT_PROPERTY_PREFIX = 'http://www.wikidata.org/prop/direct/{}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract a subgraph from a (truthy) Wikidata dump')
    parser.add_argument('dump',
                        help='path to the Wikidata dump')
    parser.add_argument('out',
                        help='path to the output graph')
    parser.add_argument('--property', '-p', dest='prop',
                        help='include property in output graph')
    parser.add_argument('--language', '-l',
                        help=('include (preferred) labels in language '
                              'in the output graph'))
    parser.add_argument('--additional-properties',
                        action='append', dest='properties',
                        help='include properties on subjects of --property')

    args = parser.parse_args()
    properties = { DIRECT_PROPERTY_PREFIX.format(prop)
                   for prop in args.properties }
    prop = DIRECT_PROPERTY_PREFIX.format(args.prop)

    out = rdflib.Graph()
    graph = rdflib.Graph()

    start = datetime.now()
    print('[{}] starting parsing'.format(start))
    # might fail due to https://github.com/RDFLib/rdflib/issues/835
    graph.parse(args.dump, format='nt')

    stop = datetime.now()
    print('[{}] finished parsing, took {}'.format(stop, stop - start))
    start = datetime.now()

    for p in properties | {prop}:
        pl, pll = graph.preferredLabel(p, lang=args.language)
        out.add([p, pl, pll])

    for (subj, obj) in graph.subject_objects(prop):
        sl, sll = graph.preferredLabel(subj, lang=args.language)
        ol, oll = graph.preferredLabel(obj, lang=args.language)
        out.add([subj, prop, obj])
        out.add([subj, sl, sll])
        out.add([obj, ol, oll])

    for p in properties:
        for o in graph.objects(subj, p):
            ol, oll = graph.preferredLabel(o, lang=args.language)
            out.add([subj, p, o])
            out.add([o, ol, oll])

    stop = datetime.now()
    print('[{}] finished constructing subgraph, took {}'.format(stop,
                                                                stop - start))

    start = datetime.now()
    out.serialize(args.out, format='nt')

    stop = datetime.now()
    print('[{}] finished writing output, took {}'.format(stop, stop - start))
