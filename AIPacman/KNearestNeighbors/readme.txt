I used score, time, distance to closest ghost, index of pacman and the indexes of all the ghosts as features for my
k-nearest neighbors algorithm. I used data from 5000 moves in my depth-first search algorithm as training data since
that was my most successful algorithm to date. As a distance function I simply took the average of the differences
between all features since weighting features did not appear to have a significant effect. Since the training data for
this algorithm is based on depth-first search, where the controller did not search for moves until the last ghost left
the lair, I chose for Ms. Pac-Man to wait for the last ghost to exit in this algorithm as well.

This algorithm was probably the worst of all the algorithms I implemented. While it was generally successful, Ms.
Pac-Man exhibited some similar indicision behavior as the A* pathfinding algorithm, although to a lesser degree, and
she sometimes moved directly away from ghosts even when she was not close enough for the distance to be interpreted as
zero as with the evolutionary algorithm. And, in fact, as k increased, these indecision behaviors and wrong direction
movements increased also and ocurred for more prolonged periods of time.
