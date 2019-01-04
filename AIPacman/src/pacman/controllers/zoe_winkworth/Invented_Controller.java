package pacman.controllers.zoe_winkworth;

import java.util.ArrayList;
import java.util.List;

import pacman.controllers.Controller;
import pacman.controllers.examples.StarterGhosts;
import pacman.game.Constants;
import pacman.game.Constants.DM;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

public class Invented_Controller extends Controller<MOVE>{
	
	public static StarterGhosts ghosts = new StarterGhosts();
	
	/**
	 * Overrides the getMove method to return a move
	 * that moves Ms. Pacman closer to a ghost
	 */
	@Override
	public MOVE getMove(Game game,long timeDue){
		
		//only consider possible moves
		MOVE[] possibleMoves = game.getPossibleMoves(game.getPacmanCurrentNodeIndex());

		int pathLength = Integer.MAX_VALUE;
		MOVE deadliestMove = null;

		for(MOVE m: possibleMoves){

			Game gameCopy = game.copy(); 
			gameCopy.advanceGame(m, ghosts.getMove(gameCopy, timeDue)); 
			
			List<MOVE> path = getPath(gameCopy);
			int pathDist = path.size();
			if(pathDist < pathLength){
				pathLength = pathDist;
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
	
	/***
	 * Gets the path to the closest ghost
	 * 
	 * @param game
	 * 		the current game state
	 * @return a list of moves corresponding to the path
	 */
	public List<MOVE> getPath(Game game){
		
		List<MOVE> path = new ArrayList<MOVE>();
		
		while(!game.gameOver()){
			
			GHOST ghost = getClosestGhost(game);
			int pacmanIndex = game.getPacmanCurrentNodeIndex();
			int ghostIndex = game.getGhostCurrentNodeIndex(ghost);
			MOVE moveMade = game.getPacmanLastMoveMade();
			MOVE move = game.getApproximateNextMoveTowardsTarget(pacmanIndex, ghostIndex, moveMade, DM.PATH);
			path.add(move);
			game.advanceGame(move, ghosts.getMove(game, 0)); 
		}
		return path;
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
