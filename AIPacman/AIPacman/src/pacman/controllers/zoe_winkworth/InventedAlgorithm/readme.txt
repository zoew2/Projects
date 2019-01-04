Since many of the issues I faced in implementing the assigned algorithms were due to using built in methods in
unconventional or unintended ways, I decided to take a more basic and straightforward approach for my algorithmic
invention. Since there exists in the framework a built in method getApproximateNextMoveTowardsTarget I decided to
leverage that. For each move possible to Ms. Pac-Man from the current index, I advanced the game state by taking the
next move towards the closest ghost according to the built-in method, and returned the resultant paths. I then compared
the length of paths and directed Ms. Pac-Man to take the move that would result in the shortest path.

As might be suspected, this algorithm is extremely successful and efficient. It takes about the same amount of time as
the depth-first search algorithm and does not have any issues with indecision or interpreting being next to a ghost as
being distance zero from a ghost.
