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
