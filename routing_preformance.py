#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# Lachlan Ford

import sys
import routing
from topology import Topology

# Dispatcher for all of the algorithms
dispatcher = {
        'SHP': routing.ShortestHopPath,
        'SDP': routing.ShortestDelayPath,
        'LLP': routing.LeastLoadedPath
}

def main():
    '''
    Parses the arguments and dispatches the correct routing algorithm.
    '''
    if len(sys.argv) < 4:
        print('routing_preformance.py algorithm topology_file workload_file')
        sys.exit()
    name = sys.argv[1].upper()
    topology_file = sys.argv[2]
    workload_file = sys.argv[3]

    routing_algorithm = dispatcher[name](topology_file)
    routing_algorithm.run(workload_file)
    print routing_algorithm.output()

if __name__ == '__main__':
    main()
