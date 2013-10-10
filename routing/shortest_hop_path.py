#!/usr/bin/env python

from routing import Routing

class ShortestHopPath(Routing):
    # all hops are equal cost
    def cost (self):
        return 1
