/**
 * 
 */
package pacman.controllers.zoe_winkworth;

import java.util.Stack;

import pacman.controllers.Controller;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Constants;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

/**
 * @author Zoe
 * 
 * Suicidal Ms.Pacman paces back and forth until a ghost comes close enough
 * then she uses DFS to find the closest path to a ghost 
 * and runs straight to her death. 
 *
 */
public class DFS_Controller extends Controller<MOVE>{

	public static StarterGhosts ghosts = new StarterGhosts();

	/**
	 * Overrides the getMove method to return a move
	 * that moves Ms. Pacman closer to a ghost
	 */
	@Override
	public MOVE getMove(Game game,long timeDue){

		//only consider possible moves
		MOVE[] possibleMoves = game.getPossibleMoves(game.getPacmanCurrentNodeIndex());
		
		int distToGhost = Integer.MAX_VALUE;
		MOVE deadliestMove = null;
		
		//run DFS on each of the branches resulting from possible moves from this node
		for(MOVE m: possibleMoves){

			Game gameCopy = game.copy(); 
			gameCopy.advanceGame(m, ghosts.getMove(gameCopy, timeDue)); 
			int tempDistToGhost = dfs(new DFS_Node(gameCopy, 0), 10);

			if(tempDistToGhost < distToGhost){
				distToGhost = tempDistToGhost;
				deadliestMove = m;
			}
		}

		//if there is no ghost in site, pace back and forth.
		if(game.getGhostLairTime(GHOST.SUE) > 0){
			return pace(game);
		}
		else {
			System.out.println(game.getPacmanCurrentNodeIndex() + "," + game.getGhostCurrentNodeIndex(GHOST.BLINKY) + ","
					+ game.getGhostCurrentNodeIndex(GHOST.INKY) + "," + game.getGhostCurrentNodeIndex(GHOST.PINKY) + "," 
					+ game.getGhostCurrentNodeIndex(GHOST.SUE) + "," + distToGhost + ","
					+ game.getCurrentLevelTime() + "," + game.getScore() + "," + deadliestMove);
			return deadliestMove;
		}
	}

	/**
	 * Performs depth-first search on the given root game state
	 * up to the given maximum depth and looks for the
	 * shortest path to a ghost.
	 * 
	 * @param rootGameState
	 * 		the given root game state
	 * @param maxDepth
	 * 		the maximum depth to search
	 * @return the shortest distance to a ghost
	 */
	public int dfs(DFS_Node rootGameState, int maxDepth)
	{
		int distToGhost = Integer.MAX_VALUE;

		Stack<DFS_Node> stack = new Stack<DFS_Node>();
		stack.push(rootGameState);

		while(!stack.isEmpty()){
			DFS_Node current = stack.pop();
			Game game = current.gameState;
			//the total distance to a ghost is the distance from this node, AND the moves to get here
			int tempDist = getClosestGhost(game) + current.depth;
			if (tempDist < distToGhost){
				distToGhost = tempDist;
			}
			if(current.depth < maxDepth){
				//make sure we're only considering possible moves
				for(MOVE m: game.getPossibleMoves(game.getPacmanCurrentNodeIndex())){
					Game gameCopy = current.gameState.copy();
					gameCopy.advanceGame(m, ghosts.getMove(gameCopy, 0));
					DFS_Node node = new DFS_Node(gameCopy, current.depth+1);
					stack.push(node);
				}
			}
		}
		return distToGhost;
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
	 * This method returns moves allowing Ms. Pacman
	 * to pace back and forth if she can't see any ghosts
	 * 
	 * @param game
	 * 		the given game state
	 * @return a MOVE (either RIGHT or LEFT)
	 */
	private MOVE pace(Game game){
		if(game.getCurrentLevelTime() < 5){
			return MOVE.LEFT;
		}
		if(game.getCurrentLevelTime() == 5){
			return MOVE.RIGHT;
		}
		else if(game.getCurrentLevelTime() % 20 == 0){
			if(game.getPacmanLastMoveMade() == MOVE.LEFT){
				return MOVE.RIGHT;
			}
			else return MOVE.LEFT;
		}
		else{
			return game.getPacmanLastMoveMade();
		}
	}
}