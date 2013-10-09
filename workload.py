#!/usr/bin/env python

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

if __name__ == '__main__':
    workload = Workload('workload.txt')
    # test itteration
    current_work_unit = workload.begin()
    while current_work_unit != None:
        print current_work_unit
        current_work_unit = workload.next()
