import re
import argparse


from collections import defaultdict
from itertools import count


ORIGIN = '3582'  # origin AS number (University of Oregon)
LABEL_RE = re.compile(r'^<a href="/cgi-bin/as-report\?as=AS(?P<asn>\d+)&view=2\.0">AS(?P=asn)\s*</a> (?P<asl>.+)$')


def labels_from_autnums(infile):
    labels = {}

    for line in infile:
        match = LABEL_RE.match(line)

        if match is None:
            continue

        labels[int(match.group('asn'))] = 'AS{}: {}'.format(
            int(match.group('asn')),
            match.group('asl').strip())

    return labels


def graph_from_as_paths(infile):
    def counter():
        c = count(1)

        def step():
            return next(c)
        return step


    vertices = defaultdict(counter())
    edges = defaultdict(set)

    for line in infile:
        path = [ORIGIN] + [asn.strip()
                           for asn in line.split(' ')[1:]]

        for source, sink in zip(path, path[1:]):
            s = vertices[source]
            t = vertices[sink]
            edges[s] |= {t}

    return vertices, edges



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Turn an AS-path list and AS '
                                                  'names list into a METIS graph/dict'))
    parser.add_argument('routes',
                        help='path to AS-paths list')
    parser.add_argument('asnames',
                        help='path to AS names list')
    parser.add_argument('graph',
                        help='path to output graph')
    parser.add_argument('dict',
                        help='path to output dict')
    args = parser.parse_args()

    vertices = None
    edges = None
    labels = None

    with open(args.routes, 'r') as infile:
        vertices, edges = graph_from_as_paths(infile)

    with open(args.asnames, 'r') as infile:
        labels = labels_from_autnums(infile)

    with open(args.graph, 'w') as outfile:
        num_vertices = len(vertices.items())
        num_edges = sum((len(list(e)) for e in edges.values()))
        print('{} {}'.format(num_vertices, num_edges),
              file=outfile)

        for source, sinks in edges.items():
            if len(sinks):
                print(source,
                      *sinks,
                      sep=' ',
                      file=outfile)

    with open(args.dict, 'w') as outfile:
        for asn, vertex in vertices.items():
            label = asn
            try:
                label = labels[int(asn)]
            except:
                pass

            print('{},"{}"'.format(vertex, label),
                  file=outfile)
