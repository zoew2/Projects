In this controller, we have chosen to use an evolutionary algorithm, based on the idea of natural selection and
evolution in biology. We treat each position on the board as an individual with a ‘fitness’ score. This score tells us
how how close an individual is to our goal state. In our case, the goal is to find the shortest path to a ghost, so the
fitness score of a given position is the distance from Ms. Pacman to that position, added to the distance from that
position to a ghost. A ‘child’ of a given position is any position that is one move away from that position. So we
start with an initial population (this controller uses all the positions 3 moves away from Ms. Pacman), and ‘evolve’
the individual with the lowest fitness score (shortest path to a ghost) by adding all the individuals one move away
from the chosen individual to our population, and removing the same number of individuals with the highest fitness
scores in order to keep the population size steady. We continue this process until the individual with the lowest
fitness score is 0 moves away from a ghost, and then we choose the first move that we made from Ms. Pacman’s current
position to reach that position as our move for this turn.

In implementing an evolutionary algorithm, I treated game states as individuals in the population and created a
structure to store and compare fitness information about them. Each game state had multiple possible children, created
by advancing that game state by any of the possible moves from Ms. Pac-Man’s index at that game state. My initial
population was created from the great-grandchildren of the root node, or by advancing the game state in all possible
directions to a depth of three. For my fitness function, I used the total distance to the closest ghost at each game
state, including the number of moves from the root game state to the current one. The evolution strategy I chose was
elitism, so I chose one parent per iteration (the individual with the highest fitness), created all of its possible
children, and then killed the parent and enough of the lowest fitness individuals to keep the population size steady.
The closest ghost was found when each node was created instead of at the root node as with A* pathfinding since this
algorithm was much faster. Additionally, since this algorithm does not have to traverse the entire tree of possible
game states, I chose to have Ms. Pac-Man pace until the first ghost exited the lair. This algorithm performed much
worse than both depth-first search and A* pathfinding. While it was much quicker and on the whole was successful, at
times, when Ms. Pac-Man encounters a ghost, she moves away from the ghost in such a way that she appears to be leading
it but they are so close that the images are overlapping. This is because when Ms. Pac-Man and a ghost are that close,
the getShortestPathDistance method called on their indexes returns zero. This results in the algorithm finding that
moving away from a ghost is the best move since the ghost will follow and their distance will remain zero. Since the
getShortestPathDistance doesn’t consider moves in reverse, since I assume it was intended for ghosts and reversing is
an illegal move, this is not an issue when Ms. Pac-Man is approaching a ghost directly, only when their paths cross
at an intersection.