package pacman.controllers.zoe_winkworth;

import pacman.game.Constants;
import pacman.game.Game;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;

/**
 * @author Zoe
 *
 * A representation of a node for Knn
 */
public class Knn_Node {
	
	int pacman;
	int blinky;
	int inky;
	int pinky;
	int sue;
	int dist;
	int time;
	int score;
	
	/**
	 * A constructor for this node
	 * 
	 * @param pacman
	 * 		the current index of pacman
	 * @param blinky
	 * 		the current index of blinky
	 * @param inky
	 * 		the current index of inky
	 * @param pinky
	 * 		the current index of pinky
	 * @param sue
	 * 		the current index of sue
	 * @param dist
	 * 		the path distance from pacman to the closest ghost
	 * @param time
	 * 		the current level time
	 * @param score
	 * 		the current score
	 */
	 public Knn_Node(int pacman, int blinky, int inky, int pinky, int sue, int dist, int time, int score){
		this.pacman = pacman;
		this.blinky = blinky;
		this.inky = inky;
		this.pinky = pinky;
		this.sue = sue;
		this.dist = dist;
		this.time = time;
		this.score = score;
	}
	
	/**
	 * A constructor for this node
	 * 
	 * @param gameState
	 * 		the current game state
	 */
	public Knn_Node(Game gameState){
		this.pacman = gameState.getPacmanCurrentNodeIndex();
		this.blinky = gameState.getGhostCurrentNodeIndex(GHOST.BLINKY);
		this.inky = gameState.getGhostCurrentNodeIndex(GHOST.INKY);
		this.pinky = gameState.getGhostCurrentNodeIndex(GHOST.PINKY);
		this.sue = gameState.getGhostCurrentNodeIndex(GHOST.SUE);
		this.dist = getClosestGhost(gameState);
		this.time = gameState.getCurrentLevelTime();
		this.score = gameState.getScore();
	}
	
	/**
	 * For a given gameState,
	 * for each ghost, determines whether the shortest path distance
	 * is the shortest seen yet.
	 * 
	 * a.k.a. finds the closest ghost
	 * 
	 * @param gameState
	 * 		the given game state
	 * @return the shortest path distance to a ghost
	 */
	private int getClosestGhost(Game gameState){
		int current = gameState.getPacmanCurrentNodeIndex();
		int dist = Integer.MAX_VALUE;

		GHOST[] allGhosts = Constants.GHOST.values();

		for (GHOST g: allGhosts){
			int gCurrent = gameState.getGhostCurrentNodeIndex(g);
			MOVE gLastMove = gameState.getGhostLastMoveMade(g);
			int tempDist = gameState.getShortestPathDistance(gCurrent, current, gLastMove);
			if(tempDist < dist){
				dist = tempDist;
			}
		}
		return dist;
	}
	
	/**
	 * Calculates the distance between this node and a given node
	 * 
	 * @param n
	 * 		the given node
	 * @return the distance measure
	 */
	public Integer getDistance(Knn_Node n) {
	int pacmanDist = (Math.abs(this.pacman - n.pacman))^2;
	int blinkyDist = (Math.abs(this.blinky - n.blinky))^2;
	int inkyDist = (Math.abs(this.inky - n.inky))^2;
	int pinkyDist = (Math.abs(this.pinky - n.pinky))^2;
	int sueDist = (Math.abs(this.sue - n.sue))^2;
	int distDist = (Math.abs(this.dist - n.dist))^2;
	int timeDist = (Math.abs(this.time - n.time))^2;
	int scoreDist = (Math.abs(this.score - n.score))^2;
	double avgDist = Math.sqrt((pacmanDist + blinkyDist + inkyDist + pinkyDist + sueDist + distDist + timeDist + scoreDist));
	return (int) avgDist;
	}
}
