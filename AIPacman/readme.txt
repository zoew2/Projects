These are controllers developed for the Pacman AI projects developed at UC Berkeley. (http://inst.eecs.berkeley
.edu/~cs188/pacman/home.html)

Whenever it is Ms. Pacman’s turn to move in the game, the getMove() method in this class is called and gives the game
board the move that Ms. Pacman chooses to make that turn in order to get her closer to her goal. The framework for this
game allows us the ability to make a copy of the game and make hypothetical moves in this copy in order to see how the
game would turn out; much like a human player would anticipate future possible moves when chosing a move to make.
However, in this framework, we know exactly how the ghosts will move, so we don’t need to guess how a given move will
effect the outcome of the game. But we have a time limit to provide our move to the game framework, so we need to be
more efficient than simply trying every single possible combination of moves to see which leads to our desired outcome
the quickest. Instead, we can use algorithms to search through all the possible moves with more efficiency.

For all of my controllers, as opposed to optimizing the score or longevity of Ms. Pac-Man, I implemented a suicidal Ms.
Pac-Man who attempts to move towards the closest ghost as quickly as possible. I made this choice for several reasons.
Firstly, the goal state is very clear. Maximizing the score is a somewhat more ambiguous goals since it is never easy
to assess what the true maximum is and whether or not that maximum is reached. In addition, a ‘good’ strategy is often
subjective and it may not always be clear after an algorithm has been executed whether the score achieved was indeed
the optimum score, and even if it is, whether the strategy used was ‘good’ or not. Conversely, with a suicidal
controller it is easy to visually assess whether an algorithm is successful or not since it is usually obvious to
an observer where Ms. Pac-Man should move in order to cross paths with a ghost.

The only obstacle to this approach is that, within the framework, the ghosts do not exit their lair immediately, so for
many algorithms, they are not ‘visible’. To combat this, all of my algorithms make use of a method which causes Ms.
Pac-Man to pace back and forth until the ghosts exit the lair. The exact implementation of when the pace method is
evoked differs between some algorithms and will be discussed along with their implementation details.
