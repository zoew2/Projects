package pacman.controllers.zoe_winkworth;

import pacman.game.Constants.MOVE;
import pacman.game.Game;

/**
 * @author Zoe
 * 
 * A representation of an individual in a population
 */
public class Individual implements Comparable<Individual>{
	
	Game gameState;
	int fitness;
	MOVE firstMove;
	int dist;
	int moves;
	
	public Individual(Game game, MOVE firstMove, int dist, int moves){
		this.gameState = game;
		this.firstMove = firstMove;
		this.fitness = dist + moves;
	}

	@Override
	public int compareTo(Individual i) {
		return this.fitness - i.fitness;
	}
}
