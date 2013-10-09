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

    def add_vertex(self, value):
        self.vertices.add(value)

    def add_edge(self, vert_from, vert_to, weight):
        self.edges[vert_from].append(vert_to)
        self.edges[vert_to].append(vert_from)
        self.weights[(vert_from, vert_to)] = weight
