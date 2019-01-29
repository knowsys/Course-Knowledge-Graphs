from . import Graph

import re
from collections import defaultdict
from html.entities import codepoint2name

NTRIPLES_PATTERN = re.compile(
    r'\s*'.join([r'^',
                  r'<(?P<subj>[^>]*)>',
                  r'<(?P<pred>[^>]*)>',
                  r'(<(?P<obj>[^>]*)>|"(?P<lit>[^"]*)"(@[a-z]+)?)',
                  r'.',
                  r'$']))
ENTITIES = str.maketrans({
    codepoint: '&{};'.format(name)
    for codepoint, name in codepoint2name.items()
})


def read_edge_list_graph(infile):
    "parse an edge-list formatted graph from `infile`"
    num_vertices = int(infile.readline())
    graph = Graph(range(num_vertices))

    for line in infile:
        source, target = line.split(' ')
        graph.add_edge(int(source), int(target))

    return graph


def read_metis_graph(infile):
    "parse a METIS formatted graph from `infile`"
    vertices_edges = infile.readline().split(' ')
    num_vertices = int(vertices_edges[0])
    num_edges = int(vertices_edges[1])
    graph = Graph (range(num_vertices))

    for line in infile:
        vertices = line.split(' ')
        if len(vertices) > 1:
            source = vertices[0]
            for target in vertices[1]:
                graph.add_edge(int(source), int(target))

    return graph


def read_nx_digraph_from_metis_file(graphfile, dictfile=None):
    import networkx

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


def write_metis_graph(outfile, graph):
    "write `graph` to `outfile`, in METIS format"
    print('{} {}'.format(graph.number_of_vertices,
                           graph.number_of_edges),
          file=outfile)

    for source in graph.vertices:
        if graph.out_degree(source) > 0:
            print(source,                # source vertex first
                  *graph.edges[source],  # then all target vertices
                  sep=' ',               # separated by a space
                  file=outfile)


def escape_html_entities(string):
    "replace known unicode codepoints in `string` with named HTML entities."
    return string.translate(ENTITIES)


def read_ntriples_graph(infile):
    "read a graph in N-Triples format from `infile`"
    graph = Graph([])

    for line in infile:
        stripped = line.strip()

        if stripped == '':
            continue

        match = NTRIPLES_PATTERN.match(stripped)

        if match is None:
            print("line `{}' not readable.".format(stripped))
            continue

        if not match.group('obj'):
            # literal match, ignore
            continue

        graph.add_vertex(match.group('subj'))
        graph.add_vertex(match.group('obj'))
        graph.add_edge(source=match.group('subj'),
                       label=match.group('pred'),
                       target=match.group('obj'))

    return graph


def write_ntriples_graph(outfile, graph):
    "write `graph` to `outfile`, in N-Triples format"
    for subj in graph.vertices:
        if graph.out_degree(subj) > 0:
            for (pred, obj) in graph.edges[subj]:
                print('<{}> <{}> <{}> .'.format(
                    escape_html_entities(subj),
                    escape_html_entities(pred),
                    escape_html_entities(obj)),
                      file=outfile)
