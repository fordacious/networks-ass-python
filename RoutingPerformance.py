#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford

import sys
from collections import defaultdict

class Workload(object):
    def __init__(self, workload_file):
        self.work_units = []
        self.parse(workload_file)

    def parse(self, topology_file):
        fin = open(topology_file, 'rU')
        for line in fin:
            time_activated, vert_from, vert_to, time_to_live = line.split()
            self.work_units.append({
                    "time_activated" : float(time_activated), 
                    "vert_from"      : vert_from, 
                    "vert_to"        : vert_to, 
                    "time_to_live"   : float(time_to_live)
                })

    def __iter__(self):
        for e in self.work_units:
            yield e
        raise StopIteration

class Topology(object):
    def __init__(self, topology_file):
        self.vertices = set()
        self.edges = {}
        self.parse(topology_file)
        self.cache = {}

    def parse(self, topology_file):
        fin = open(topology_file, 'rU')
        for line in fin:
            vert_from, vert_to, delay, conns = line.split()
            self.add_vertex(vert_from)
            self.add_vertex(vert_to)
            self.add_edge(vert_from, vert_to, delay, conns)

    def create_edge (self, weight, capacity):
        return {
                "weight"      : float(weight),  # Propigation Delay
                "capacity"    : capacity,
                "connections" : []
            }

    def add_vertex(self, value):
        self.vertices.add(value)

    def get_vertices_from(self, vertex):
        if vertex in self.cache:
            return self.cache[vertex]
        self.cache[vertex] =  [k[0] for k,v in self.edges.items() if k[1] == vertex]
        return self.cache[vertex]

    def add_edge(self, vert_from, vert_to, weight, capacity):
        new_edge = self.create_edge(weight, capacity)
        self.edges[(vert_from, vert_to)] = new_edge
        self.edges[(vert_to, vert_from)] = new_edge

    def add_connection (self, vert_from, vert_to, time, time_to_live):
        self.edges[(vert_from, vert_to)]["connections"].append( {
                "activation_time" : float(time),
                "time_to_live"    : float(time_to_live)
         } )

    def valid_connection_path (self, path):
        '''
        Returns whether or not a connection path is valid with the current
        state.
        '''
        if path == None: return 
        edge = self.edges[(path[0], path[1])]
        cons, cap = len(edge["connections"]), int(edge["capacity"])
        if len(path) == 2: return cons < cap
        return (cons < cap) and self.valid_connection_path(path[1:])

    def add_connection_path (self, path, time, time_to_live):
        ''' Adds a connection along a path '''
        if len(path) == 2:
            self.add_connection(path[0], path[1], time, time_to_live)
        else:
            self.add_connection(path[0], path[1], time, time_to_live)
            self.add_connection_path(path[1:], time, time_to_live)

    def clear_obsolete_connections (self, cur_time):
        for ek,edge in self.edges.items():
            edge["connections"] = [con for con in edge["connections"] if con["activation_time"] + con["time_to_live"] > float(cur_time)]
                

class Routing(object):
    '''
    Base class for all routing protocols, accepts a schema, parses it.
    '''
    def __init__(self, topology):
        self.topology        = topology
        self.num_vc_requests = 0.0
        self.num_blocked     = 0.0
        self.num_hops_avg    = 0.0
        self.delay_avg       = 0.0


    def run (self, workload):
        for unit in workload:
            self.num_vc_requests += 1
            path = self.get_path(unit)
            current_time = unit["time_activated"]
            self.topology.clear_obsolete_connections(current_time)

            if self.topology.valid_connection_path(path):
                self.topology.add_connection_path(path, current_time, unit["time_to_live"])
            else:
                self.num_blocked += 1

    def djikstra(self, vert_start):
        visited_vertices = {vert_start: 0}
        total_path = {}
        
        candidates = set(self.topology.vertices)
        
        filter_lambda = lambda e: e in visited_vertices
        sorted_lambda = lambda e: visited_vertices[e]

        visited = set(visited_vertices.keys())
        while candidates:
            #visited = filter(filter_lambda, candidates)
            #visited.sort(key=sorted_lambda)
            minimum_vertex = min(visited, key=sorted_lambda) if visited else None
            if not minimum_vertex: break

            candidates.remove(minimum_vertex)
            if minimum_vertex in visited: visited.remove(minimum_vertex)
            visit_cost = visited_vertices[minimum_vertex]

            for adjacent_vertex in self.topology.get_vertices_from(minimum_vertex):
                cost = visit_cost + self.cost((minimum_vertex, adjacent_vertex))
                if adjacent_vertex not in visited_vertices or cost < visited_vertices[adjacent_vertex]:
                    visited_vertices[adjacent_vertex] = cost
                    if adjacent_vertex in candidates: visited.add(adjacent_vertex)
                    total_path[adjacent_vertex] = minimum_vertex
        return total_path 

    def get_path (self, unit):
        vert_start, vert_end = unit['vert_from'], unit['vert_to']
        paths = self.djikstra(vert_start)
        path = [vert_end]
       
        while vert_end != vert_start:
            if vert_end in paths:
                path.append(paths[vert_end])
                vert_end = paths[vert_end]
            else:
                return None

        path.reverse()
        self.num_hops_avg += len(path)

        total_delay = 0.0
        for i in xrange(0, len(path)):
            if (i + 1) == len(path): break
            total_delay += self.topology.edges[path[i], path[i+1]]["weight"]
        self.delay_avg += total_delay

        return path

    def cost (self, edge):
        return self.topology.weights[edge][0]

    # safely prints things the way we want
    def safe_print (self, num, den = 1):
        if den == 0:
            return 0
        val = num / den
        if val == int(val):
            return int(val)
        return val

    def output (self):
        print 'total number of virtual circuit requests: {0}'.format(self.safe_print(self.num_vc_requests))
        print 'number of successfully routed requests: {0}'.format(self.safe_print(self.num_vc_requests - self.num_blocked))
        print 'percentage of successfully routed request: {0}'.format(self.safe_print(((self.num_vc_requests - self.num_blocked) * 100.0) , self.num_vc_requests))
        print 'number of blocked requests: {0}'.format(self.safe_print(self.num_blocked))
        print 'percentage of blocked requests: {0}'.format(self.safe_print((self.num_blocked * 100.0) , self.num_vc_requests))
        print 'average number of hops per circuit: {0}'.format(self.safe_print(self.num_hops_avg/self.num_vc_requests))
        print 'average cumulative propagation delay per circuit: {0}'.format(self.safe_print(self.delay_avg/self.num_vc_requests))


class LeastLoadedPath(Routing):
    '''
    Least Loaded Path is equivalent to the ratio of the current number of
    active connections to the capacity of the link. We define our cost by
    this ratio.
    '''
    def cost (self, edge):
        conns = float(len(self.topology.edges[edge]["connections"]))
        capacity = float(self.topology.edges[edge]["capacity"])
        return conns / capacity


class ShortestHopPath(Routing):
    '''
    Shortest hop path, treats all edges of equal weight, finding the shortest
    number of total hops. To this ends we can simply set the cost of each
    edge to 1 and the shortest number of hops will be found.
    '''
    def cost (self, edge):
        return 1

class ShortestDelayPath(Routing):
    '''
    Shortest Delay Path is looking at the cost of the propogation delay of
    the link, if we simply use the defined weight of each edge we find the
    shortest delay path.
    '''
    def cost (self, edge):
        return self.topology.edges[edge]["weight"]


def main():
    if (len(sys.argv) < 4): return
    
    dispatcher = {
            'SHP': ShortestHopPath,
            'SDP': ShortestDelayPath,
            'LLP': LeastLoadedPath
    }

    algorithm_name, topology_file, workload_file = sys.argv[1:4]
    topology = Topology(topology_file)
    workload = Workload(workload_file)

    routing = dispatcher[algorithm_name.upper()](topology)
    routing.run(workload)
    routing.output()

if __name__ == "__main__":
    main()
