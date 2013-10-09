#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford

class Routing(object):
    '''
    Base class for all routing protocls, accepts a schema, parses it.
    '''
    def __init__(self, topology):
        self.topology = topology
        self.num_vc_requests = 0.0
        self.num_blocked = 0.0

    def run (self, workload):
        visited = {}
        path = {}
        candidates = set(self.topology.verticies)

        while candidates:
            min_vert = None
            for candidate in candidates:
                if candidate in visited:
                    if min_vert is None:
                        min_vert = candidate
                    elif visited[candidate] < visited[min_vert]:
                        min_vert = candidate

            if min_vert is None:
                break

            # Updates the path.
            for edge in self.topology.edges[min_vert]:
                cost = current_cost + self.cost(min_vert, edge)
                if edge not in visited or cost < visited[edge]:
                    visited[edge] = weight
                    path[edge]    = min_vert
	
    def cost (self, from_vert, to_vert ):
        return self.topology.weights[(from_vert, to_vert)][0]

    def output (self):
        print 'total number of virtual circuit requests: {0}'.format(self.num_vc_requests)
        print 'number of successfully routed requests: {0}'.format(self.num_vc_requests - self.num_blocked)
        print 'percentage of successfully routed request: {0}'.format(((self.num_vc_requests - self.num_blocked) * 100) / self.num_vc_requests)
        print 'number of blocked requests: {0}'.format(self.num_blocked)
        print 'percentage of blocked requests: {0}'.format((self.num_blocked * 100) / self.num_vc_requests)

if __name__ == "__main__":
    routingSim = Routing(dict())
    routingSim.num_vc_requests = 200
    routingSim.num_blocked = 100
    routingSim.output()
