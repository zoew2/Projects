package pacman.controllers.zoe_winkworth;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

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
 * then she uses evolutionary computation to find the closest ghost 
 * and runs straight to her death. 
 *
 */
public class Evolutionary_Controller extends Controller<MOVE>{

	public static StarterGhosts ghosts = new StarterGhosts();

	/**
	 * Overrides the getMove method to return a move
	 * that moves Ms. Pacman closer to a ghost
	 */
	@Override
	public MOVE getMove(Game game,long timeDue){

		//only consider possible moves
		MOVE[] possibleMoves = game.getPossibleMoves(game.getPacmanCurrentNodeIndex());
		
		//create initial population of great-grandchildren
		List<Individual> population = new ArrayList<Individual>();
		for(MOVE m: possibleMoves){
			Game child = game.copy();
			child.advanceGame(m, ghosts.getMove(child, timeDue));
			for(MOVE o: child.getPossibleMoves(child.getPacmanCurrentNodeIndex())){
				Game grandChild = child.copy();
				grandChild.advanceGame(o, ghosts.getMove(grandChild, timeDue));
				for(MOVE v: grandChild.getPossibleMoves(grandChild.getPacmanCurrentNodeIndex())){
					Game greatGrandChild = grandChild.copy();
					greatGrandChild.advanceGame(v, ghosts.getMove(greatGrandChild, timeDue));
					GHOST ghost = getClosestGhost(greatGrandChild);
					int gIndex = greatGrandChild.getGhostCurrentNodeIndex(ghost);
					int pIndex = greatGrandChild.getPacmanCurrentNodeIndex();
					MOVE lastMove = greatGrandChild.getGhostLastMoveMade(ghost);
					int distToGhost = greatGrandChild.getShortestPathDistance(gIndex, pIndex, lastMove);
					population.add(new Individual(greatGrandChild, m, distToGhost, 3));
				}
			}
		}
		//evolve the population to find the best individual
		Individual best = evolve(population);

		//if there is no ghost in sight, pace back and forth.
		if(game.getGhostLairTime(GHOST.BLINKY) > 0){
			return pace(game);
		}
		else {
			return best.firstMove;
		}
	}

	public Individual evolve(List<Individual> population) {
		
		//evolve until we reach the goal state
		Collections.sort(population);
		while(population.get(0).dist > 0){
			
			//pick the individual with lowest fitness to be a parent
			Individual parent = population.get(0);
			
			//remove the parent from the population
			population.remove(0);
			Game game = parent.gameState;
			
			//create a list of the children of the parent
			List<Individual> children = new ArrayList<Individual>();
			for(MOVE m: game.getPossibleMoves(game.getPacmanCurrentNodeIndex())){
				game.advanceGame(m, ghosts.getMove(game, 0));
				GHOST ghost = getClosestGhost(game);
				int gIndex = game.getGhostCurrentNodeIndex(ghost);
				int pIndex = game.getPacmanCurrentNodeIndex();
				MOVE lastMove = game.getGhostLastMoveMade(ghost);
				int distToGhost = game.getShortestPathDistance(gIndex, pIndex, lastMove);
				children.add(new Individual(game, m, distToGhost, parent.moves + 1));
			}
			
			//remove enough members of the population to keep the population size steady
			int kill = children.size() - 1;
			for(int i = 0; i < kill; i++){
				population.remove(population.size() - 1);
			}
			
			//add the children to the population
			population.addAll(children);
			
			//sort the population so the lowest fitness members are first
			Collections.sort(population);
		}
		return population.get(0);
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
