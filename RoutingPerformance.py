#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford


import sys
from collections import defaultdict

class Workload(object):
    '''
    Our datastructure that defines our workload.
    '''
    def __init__(self, workload_file):
        self.work_units = []
        self.current_index = 0
        self.parse(workload_file)

    def parse(self, topology_file):
        fin = open(topology_file, 'rU')
        for line in fin:
            time_activated, vert_from, vert_to, time_to_live = line.split()
            self.work_units.append({
                    "time_activated" : time_activated, 
                    "vert_from"      : vert_from, 
                    "vert_to"        : vert_to, 
                    "time_to_live"   : time_to_live
                })
        self.current_index = self.work_units[0]

    def begin (self):
        self.current_index = -1
        return self.next()

    # move time, set current work unit
    # returns None when done
    def next (self):
        self.current_index += 1
        if self.current_index < len(self.work_units):
            return self.work_units[self.current_index]
        return None

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

    # weight = propogation delay
    def create_edge (self, weight, capacity):
        return {
                "weight"      : weight, 
                "capacity"    : capacity,
                "connections" : []
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
    def valid_connection_path (self, path):
        if len(path) == 2:
            return len(self.edges[(path[0], path[1])]["connections"]) < int(self.edges[(path[0], path[1])]["capacity"])
        return len(self.edges[(path[0], path[1])]["connections"]) < int(self.edges[(path[0], path[1])]["capacity"]) and self.valid_connection_path(path[1:])

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
                

class Routing(object):
    '''
    Base class for all routing protocls, accepts a schema, parses it.
    '''
    def __init__(self, topology):
        self.topology        = topology
        self.num_vc_requests = 0.0
        self.num_blocked     = 0.0

    def run (self, workload):
        
        current_work_unit = workload.begin()
        while current_work_unit != None:
            
            path = self.get_path(current_work_unit)

            current_time = current_work_unit["time_activated"]

            self.topology.clear_obsolete_connections(current_time)

            if topology.valid_connection_path(path):
                topology.add_connection_path(path, time, current_work_unit["time_to_live"])
            else:
                self.num_blocked += 1
            
            current_work_unit = workload.next()

    # actually runs dijkstras
    # returns the path
    # can early exit once we have the value from the source to destination
    def get_path (self, current_work_unit):
        pass

    def cost (self, from_vert, to_vert ):
        return self.topology.weights[(from_vert, to_vert)][0]

    # safely prints things the way we want
    def __safeDivPrint (self, num, den = 1):
        if den == 0:
            return 0
        val = num / den
        if val == int(val):
            return int(val)
        return val

    def output (self):
        print 'total number of virtual circuit requests: {0}'.format(self.__safeDivPrint(self.num_vc_requests))
        print 'number of successfully routed requests: {0}'.format(self.__safeDivPrint(self.num_vc_requests - self.num_blocked))
        print 'percentage of successfully routed request: {0}'.format(self.__safeDivPrint(((self.num_vc_requests - self.num_blocked) * 100.0) , self.num_vc_requests))
        print 'number of blocked requests: {0}'.format(self.__safeDivPrint(self.num_blocked))
        print 'percentage of blocked requests: {0}'.format(self.__safeDivPrint((self.num_blocked * 100.0) , self.num_vc_requests))


class LeastLoadedPath(Routing):
    # ratio of current number of active vc connections to capacity of link
    def cost (self):
        return (len(self.topology.connections[(from_vert, to_vert)]["connections"]) * 1.0) / self.topology.connections[(from_vert, to_vert)]["capacity"]

class ShortestHopPath(Routing):
    # all hops are equal cost
    def cost (self):
        return 1

class ShortestDelayPath(Routing):
    # cost if the propogation delay of the link
    def cost (self):
        return self.topology.connections[(from_vert, to_vert)]["weight"]


def main():
    return NotImplemented

if __name__ == "__main__":
    main()
