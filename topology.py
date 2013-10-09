#!/usr/bin/env python

from collections import defaultdict

class Topology(object):
    '''
    Our datastructure that defines our topology.
    '''
    def __init__(self, topology_file):
        self.vertices = set()
        self.edges = defaultdict(list)
        self.weights  = {}
        self.parse(topology_file)

    def parse(self, topology_file):
        fin = open(topology_file, 'rU')
        for line in fin:
            vert_from, vert_to, delay, conns = line.split()
            self.add_vertex(vert_from)
            self.add_vertex(vert_to)
            self.add_edge(vert_from, vert_to, (delay, conns))

    def add_vertex(self, value):
        self.vertices.add(value)

    def add_edge(self, vert_from, vert_to, weight):
        self.edges[vert_from].append(vert_to)
        self.edges[vert_to].append(vert_from)
        self.weights[(vert_from, vert_to)] = weight

if __name__ == '__main__':
    topology = Topology('topology.txt')
    print topology.vertices, dict(topology.edges), topology.weights
