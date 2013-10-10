#!/usr/bin/env python

from routing import Routing

class ShortestDelayPath(Routing):
    # cost if the propogation delay of the link
    def cost (self):
        return self.topology.connections[(from_vert, to_vert)]["weight"]
