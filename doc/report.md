# Comp3331 - Networking Assignment #

## Algorithm ##
We were able to reduce all of the variations of routing: Least Loaded Path,
Shortest Hop Path and Shortest Delay Path into formulation of Djikstras
algorithm with different cost functions.

* **Least Loaded Path**: The cost function is equivalent to the ratio
  of the current number of active connections to the capcity of the link.
* **Shortest Hop Path**: Treat all edges of equal weight, this finds the
  shortest path by number of hops only as each hop costs one it will attempt
  to minimize this cost thus satisfiying the goal.
* **Shortest Delay Path**: Treats each edges weight as its propigation delay
  to this end it will find the path with the minimumtotal delay propigation.
