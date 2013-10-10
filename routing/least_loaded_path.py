#!/usr/bin/env python

from routing import Routing

class LeastLoadedPath(Routing):

    # ratio of current number of active vc connections to capacity of link
    def cost (self):
        return (len(self.topology.connections[(from_vert, to_vert)]["connections"]) * 1.0) / self.topology.connections[(from_vert, to_vert)]["capacity"]
