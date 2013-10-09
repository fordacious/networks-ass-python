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

    def add_connection (self, vert_from, vert_to, time, time_to_live):
        self.edges[(vert_from, vert_to)]["connections"].append( {
                "activation_time" : time,
                "time_to_live"    : time_to_live
            } )

    # returns whether or not a connection path is valid with current state
    def valid_connection_path (path):
        #TODO
        pass

    # adds connections along a path
    def add_connection_path (self, path, time, time_to_live):
        if len(path) == 2:
            self.add_connection(path[0], path[1], time, time_to_live)
        else:
            self.add_connection(path[0], path[1], time, time_to_live)
            self.add_connection_path(path[1:], time, time_to_live)

    def clear_obsolete_connections (self, cur_time):
        for ek,edge in self.edges.items():
            # make a new list of connections with only the connections that should be active (the time has not exceeded their lifetime)
            # TODO possible fencepost error here
            edge["connections"] = [con for con in edge["connections"] if con["activation_time"] + con["time_to_live"] > cur_time]
                

if __name__ == '__main__':
    topology = Topology('topology.txt')
    print topology.vertices, topology.edges
    # TODO test adding and removing connections
    '''
    0.221267 B F 0.973490
    1.379235 K D 2.095500
    1.670436 D E 1.856995
    2.286279 F L 39.597595
    2.487471 O H 6.599911
    2.634504 E M 22.582966
    '''
    print "TESTING CONNECTIONS"
    topology.clear_obsolete_connections(0)
    topology.add_connection_path(['B', 'C', 'D', 'F'], 0.221267, 1.973490)
    print topology.edges[('B','C')]
    print topology.edges[('C','D')]
    print topology.edges[('D','F')]
    topology.clear_obsolete_connections(1.379235)
    topology.add_connection_path(['K', 'N', 'O', 'F', 'D'], 1.379235, 2.095500)
    print topology.edges[('B','C')]
    print topology.edges[('C','D')]
    print topology.edges[('D','F')]
    topology.clear_obsolete_connections(1.670436)
    topology.add_connection_path(['D','E'], 1.670436, 1.856995)
    print topology.edges[('B','C')]
    print topology.edges[('C','D')]
    print topology.edges[('D','F')]
    topology.clear_obsolete_connections(2.286279)
    topology.add_connection_path(['F', 'O', 'N', 'M', 'L'], 2.286279, 39.597595)
    print topology.edges[('N','M')]
    print topology.edges[('C','D')]
    print topology.edges[('D','F')]
    topology.clear_obsolete_connections(2.487471)
    topology.add_connection_path(['O', 'G', 'H'], 2.487471, 6.599911)
    print topology.edges[('B','C')]
    print topology.edges[('O','G')]
    print topology.edges[('D','F')]
    topology.clear_obsolete_connections(2.634504)
    topology.add_connection_path(['E', 'F', 'O', 'N', 'M'], 2.634504, 22.582966)
    print topology.edges[('O','N')]
    print topology.edges[('C','D')]
    print topology.edges[('D','F')]
