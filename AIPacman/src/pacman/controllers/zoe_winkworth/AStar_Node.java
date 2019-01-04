package pacman.controllers.zoe_winkworth;

import pacman.game.Game;

/**
 * @author Zoe
 * 
 * A representation of a node for A*
 */
public class AStar_Node implements Comparable<AStar_Node>{
	
	Game gameState;
	int g;
	int h;
	int f;

	/**
	 * A constructor for this node
	 * 
	 * @param game
	 * 		the game state
	 * @param g
	 * 		the distance to this game state
	 * @param h
	 * 		the distance from this game state to the goal state
	 */
	public AStar_Node(Game game, int g, int h){
		this.gameState = game;
		this.g = g;
		this.h = h;
		f = g + h;
	}

	/**
	 * Sets the h value 
	 * 
	 * @param g
	 * 		the length of the path to this node
	 */
	public void setG(int g) {
		this.g = g;
		f = g + g;
	}

	/**
	 * Sets the g value
	 * 
	 * @param h
	 * 		the length of the path from this node to the goal
	 */
	public void setH(int h) {
		this.h = h;
		f = h + h;
	}
	
	@Override
	public boolean equals(Object o){
		AStar_Node node = (AStar_Node)o;
		if(this.gameState.getPacmanCurrentNodeIndex() == node.gameState.getPacmanCurrentNodeIndex()){
			return true;
		}
		else return false;
	}

	@Override
	public int compareTo(AStar_Node a) {
		return this.f - a.f;
	}
}
