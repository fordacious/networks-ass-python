#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford

class Routing(object):
    '''
    Base class for all routing protocls, accepts a schema, parses it.
    '''
    def __init__(self, topology):
        self.topology = topology
