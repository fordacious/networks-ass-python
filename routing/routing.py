#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford

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
        
        '''
        path = {}
        candidates = []

        source = []

        # make tuple with cost
        for candidate in self.topology.verticies:
            candidates.append((candidate, INFINITY))

        candidates.sort(lambda x, y : 1 if cost(x[0]) > cost(y[0]) else -1)

<<<<<<< HEAD
        while len(candidates):
            # take min node and remove from candidates
            min_node = candidates[0][0]
            candidates = candidates[1:]

            
=======
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
>>>>>>> b53a1debfe0b55f287efed7372feb36d5b5fe3b1

            # Updates the path.
            for edge in self.topology.edges[min_vert]:
                cost = current_cost + self.cost(min_vert, edge)
                if edge not in visited or cost < visited[edge]:
                    visited[edge] = weight
                    path[edge]    = min_vert
	
        # TODO if path not valid, add to blocked
        '''

    # actually runs dijkstras
    # returns the path
    # can early exit once we have the value from the source to destination
    def get_path (self, current_work_unit):
        # TODO
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

if __name__ == "__main__":
    routingSim = Routing(dict())
    routingSim.num_vc_requests = 200
    routingSim.num_blocked = 100
    routingSim.output()
