package pacman.controllers.zoe_winkworth;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
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
 * then she uses A* to find the closest path to a ghost 
 * and runs straight to her death. 
 *
 */
public class AStar_Controller extends Controller<MOVE>{

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

		//pick the closest ghost at current index
		GHOST closestGhost = getClosestGhost(game);
		for(MOVE m: possibleMoves){

			Game gameCopy = game.copy(); 
			gameCopy.advanceGame(m, ghosts.getMove(gameCopy, timeDue)); 
			
			int tempDistToGhost = astar(new AStar_Node(gameCopy, 1, ghostDist(gameCopy, closestGhost)), closestGhost);
			if(tempDistToGhost < distToGhost){
				distToGhost = tempDistToGhost;
				deadliestMove = m;
			}
		}

		//if there is no ghost in sight, pace back and forth.
		if(game.getGhostLairTime(GHOST.BLINKY) > 0){
			return pace(game);
		}
		else {
			return deadliestMove;
		}
	}

	/**
	 * Gets the distance from pacman to the given ghost
	 * @param game
	 * 		the given game state
	 * @param ghost
	 * 		the given ghost
	 * @return the shortest distance to the ghost
	 */
	private int ghostDist(Game game, GHOST ghost) {
		int pacmanNode = game.getPacmanCurrentNodeIndex();
		int ghostNode = game.getGhostCurrentNodeIndex(ghost);
		return game.getShortestPathDistance(ghostNode, pacmanNode, game.getGhostLastMoveMade(ghost));
	}

	/**
	 * Finds the A* closest path to the given ghost,
	 * only searches up to 100 moves
	 * 
	 * @param rootGameState
	 * 		the given root game state
	 * @param ghost
	 * 		the closest ghost to look for
	 * @return the shortest distance to the ghost
	 */
	public int astar(AStar_Node rootGameState, GHOST ghost){
		int distToGhost = Integer.MAX_VALUE;

		Stack<AStar_Node> open = new Stack<AStar_Node>();
		List<AStar_Node> closed = new ArrayList<AStar_Node>();
		open.add(rootGameState);

		while(!open.isEmpty()){
			Collections.sort(open);
			AStar_Node current = open.pop();
			closed.add(current);
			Game game = current.gameState;
			int pacmanNode = game.getPacmanCurrentNodeIndex();
			int ghostNode = game.getGhostCurrentNodeIndex(ghost);
		
			if(current.f < distToGhost){
				distToGhost = current.f;
			}
			if(pacmanNode == ghostNode){
				break;
			}
			if(current.g < 100){
				for(MOVE m: game.getPossibleMoves(game.getPacmanCurrentNodeIndex())){
					Game gameCopy = current.gameState.copy();
					gameCopy.advanceGame(m, ghosts.getMove(gameCopy, 0));
					AStar_Node child = new AStar_Node(gameCopy, current.g + 1, ghostDist(gameCopy, ghost));	
					if(!closed.contains(child) && !open.contains(child)){
						open.add(child);
					}
					else if(!closed.contains(child) && open.contains(child)){
						AStar_Node a = getSame(child, open);
						if(current.f < a.f){
							a.setH(current.h);
							a.setG(current.g);
						}
					}
				}
			}
		}
		return distToGhost;
	}

	/**
	 * Gets a node equivalent to the given node from the given list
	 * 
	 * @param child
	 * 		the node to find an equivalent for
	 * @param open
	 * 		the list of nodes to search through
	 * @return
	 */
	private AStar_Node getSame(AStar_Node child, List<AStar_Node> open) {
		AStar_Node same = null;
		for(AStar_Node a: open){
			if(child.equals(a)){
				same = a;
			}
		}
		return same;
	}

	/**
	 * For a given gameState,
	 * for each ghost,
	 * finds the closest ghost to pacman
	 * 
	 * @param game
	 * 		the given game state
	 * @return the closest ghost
	 */
	private GHOST getClosestGhost(Game game){
		int dist = Integer.MAX_VALUE;
		GHOST ghost = null;

		GHOST[] allGhosts = Constants.GHOST.values();

		for (GHOST g: allGhosts){
			int tempDist = ghostDist(game, g);
			if(tempDist < dist){
				dist = tempDist;
				ghost = g;
			}
		}
		return ghost;
	}

	/**
	 * This method returns moves allowing Ms. Pacman
	 * to pace back and forth if she can't see any ghosts
	 * 
	 * @param game
	 * 		the given game
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
