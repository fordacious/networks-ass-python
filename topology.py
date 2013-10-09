#!/usr/bin/env python

from collections import defaultdict

class Topology(object):
    '''
    Our datastructure that defines our topology.
    '''
    def __init__(self, topology_file):
        self.vertices = set()
        self.edges    = {}
        self.parse(topology_file)

    def parse(self, topology_file):
        fin = open(topology_file, 'rU')
        for line in fin:
            vert_from, vert_to, delay, conns = line.split()
            self.add_vertex(vert_from)
            self.add_vertex(vert_to)
            self.add_edge(vert_from, vert_to, delay, conns)

    def create_edge (self, weight, capacity):
        return {
                "weight"      : weight, 
                "capacity"    : capacity,
                "connections" : {}
            }

    def add_vertex(self, value):
        self.vertices.add(value)

    def add_edge(self, vert_from, vert_to, weight, capacity):
        new_edge = self.create_edge(weight, capacity)
        self.edges[(vert_from, vert_to)] = new_edge
        self.edges[(vert_to, vert_from)] = new_edge

    def add_connection (vert_from, vert_to, time, time_to_live):
        self.edges[(vert_from, vert_to)]["connections"] = {
                "activation_time" : time,
                "time_to_live"    : time_to_live
            }

    def clear_obsolete_connections (cur_time):
        for ek,edge in self.edges.items():
            # make a new list of connections with only the connections that should be active (the time has not exceeded their lifetime)
            # TODO possible fencepost error here
            edge["connections"] = [con for ec,con in edge["connections"].items() if con["activation_time"] + con["time_to_live"] > cur_time]
                

if __name__ == '__main__':
    topology = Topology('topology.txt')
    print topology.vertices, topology.edges
    # TODO test adding and removing connections
