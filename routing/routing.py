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
	
    def output (self):
        print 'total number of virtual circuit requests: {0}'.format(num_vc_requests)
        print 'number of successfully routed requests: {0}'.format(num_vc_requests - num_blocked)
        print 'percentage of successfully routed request: {0}'.format((num_vc_requests - num_blocked) * 100.0 / num_vs_requests)
        print 'number of blocked requests: {0}'.format(num_blocked)num_vc_requests - num_blocked
        print 'percentage of blocked requests: {0}'.format(num_blocked * 100.0 / num_vc_requests)
