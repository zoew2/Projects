I utilized depth-first search by emulating a tree structure using copies of the game state as nodes and searching for
the game state where Ms. Pac-Man was closest to a ghost. The algorithm actually ran multiple depth-first searches with
each possible move from the current index as a root node and compared the results to find the move to make that would
lead to the node where Ms. Pac-Man was closest to a ghost. The distance to the closest ghost was calculated as each
node was inserted into the tree structure. Since this algorithm is limited in how far ahead it can look, I chose to
have Ms. Pac-Man pace until the last ghost exited the lair to give the ghosts a chance to get close enough for them to
have a significant effect on the algorithm.

Increasing the depth resulted in significant slowing of response time, with a depth higher than 10 slowing the game
down to a comical degree. However, even with an extremely low depth, this algorithm still performed well, suggesting
that a greedy algorithm that simply looks at distance to closest ghost would also be successful. Overall this algorithm
performed successfully, with no apparent issues other than speed at high depths.