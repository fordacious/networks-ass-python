#!/usr/bin/env python

from routing import Routing

class LeastLoadedPath(Routing):
    pass

    def cost (self):
        return self.topology.connections[(from_vert, to_vert)]
