#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>

class Workload(object):
    '''
    Defines a pythonic object that allows us to interact with the
    workload that is assigned.
    '''
    def __init__(self, workload_file):
        self.load = []
        self.parse(workload_file)

    def parse(self, workload_file)
        fin = open(workload_file, 'rU')
        for line in fin:
            arrival, src, dest, duration = line.split()
            load.append({'arrival': arrival, 'source': src,
                'destination': dest, 'duration': duration}
