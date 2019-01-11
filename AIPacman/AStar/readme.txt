To implement A* pathfinding, I created nodes to capture the h, g, and f score of each copy of the game state. Due to
the issues with speed at high depths I experienced with depth-first search, for this implementation, I found the ghost
closest to Ms. Pac-Man in the current game state, and used the distance to that ghost as the heuristic instead of
finding the closest ghost to Ms. Pac-Man at each advance of the game state. For my h score, I used the distance to
this ghost, and for my g score I used the number of game advancements or moves taken to any given game state. Since
this algorithm also has a depth limitation, I chose to have Ms. Pac-Man pace until the last ghost exited the lair again.

Overall, A* pathfinding performed relatively well, usually ending in the same amount of time as depth-first search.
However, with this algorithm, Ms. Pac-Man has clear moments of indecision where she flips back and forth from side to
side when there no clear best path to the closest ghost or the two best moves result in very similar paths. Despite
this, the algorithm still performs almost as well as depth-first search.