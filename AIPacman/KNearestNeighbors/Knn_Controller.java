package pacman.controllers.zoe_winkworth;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import pacman.controllers.Controller;
import pacman.game.Constants;
import pacman.game.Constants.GHOST;
import pacman.game.Constants.MOVE;
import pacman.game.Game;

public class Knn_Controller extends Controller<MOVE>{
	
	public static Map<MOVE, List<Knn_Node>> training = new HashMap<MOVE, List<Knn_Node>>();
	
	/**
	 * Reads the training data from the text file
	 */
	public static void readDataFile() {
		File file = new File("data.txt");

	    try {

	        Scanner sc = new Scanner(file);

	        while (sc.hasNextLine()) {
	            String[] line = sc.nextLine().split(",");
	            int pacman = Integer.parseInt(line[0]);
	            int blinky = Integer.parseInt(line[1]);
	            int inky = Integer.parseInt(line[2]);
	            int pinky = Integer.parseInt(line[3]);
	            int sue = Integer.parseInt(line[4]);
	            int dist = Integer.parseInt(line[5]);
	            int time = Integer.parseInt(line[6]);
	            int score = Integer.parseInt(line[7]);
	            String m = line[8];
	            MOVE move = getEnum(m);
	            training.get(move).add(new Knn_Node(pacman, blinky, inky, pinky, sue, dist, time, score));
	        }
	        sc.close();
	    } 
	    catch (FileNotFoundException e) {
	        e.printStackTrace();
	    }
	}

	/**
	 * Gets the enum MOVE value corresponding to a string
	 * 
	 * @param move
	 * 		the string value of the move
	 * @return the enum value of the move
	 */
	private static MOVE getEnum(String move) {
		MOVE m = null;
		if(move.equals("RIGHT")){
			m = MOVE.RIGHT;
		}
		else if(move.equals("LEFT")){
			m = MOVE.LEFT;
		}
		else if(move.equals("UP")){
			m = MOVE.UP;
		}
		else if(move.equals("DOWN")){
			m = MOVE.DOWN;
		}
		else if(move.equals("NEUTRAL")){
			m = MOVE.NEUTRAL;
		}
		return m;
	}

	/**
	 * Overrides the getMove method to return a move
	 * that moves Ms. Pacman closer to a ghost
	 */
	@Override
	public MOVE getMove(Game game, long timeDue) {
		for(MOVE m: Constants.MOVE.values()){
			training.put(m, new ArrayList<Knn_Node>());
		}
		readDataFile();
		List<MOVE> neighbors = knn(game, 10);
		if(game.getGhostLairTime(GHOST.SUE) > 0){
			return pace(game);
		}
		else {
			return mostFrequent(neighbors);
		}
	}

	/**
	 * Finds the most frequent move in a list of moves
	 * 
	 * @param neighbors
	 * 		the list of the moves of the nearest neighbors
	 * @return the most frequent move
	 */
	private MOVE mostFrequent(List<MOVE> neighbors) {
		int[] counter = new int[5];
		Arrays.fill(counter, 0);
		List<MOVE> moveToInt = new ArrayList<MOVE>();
		moveToInt.addAll(Arrays.asList(Constants.MOVE.values()));
		for(MOVE m: neighbors){
			int move = moveToInt.indexOf(m);
			counter[move] += 1;
		}
		MOVE best = null;
		int biggest = 0;
		for(int i = 0; i < 5; i++){
			if(counter[i] > biggest){
				biggest = counter[i];
				best = moveToInt.get(i);
			}
		}
		return best;
	}

	/**
	 * Finds the k nearest neighbors to the current game state
	 * 
	 * @param game
	 * 		the current game state
	 * @param k
	 * 		the number of nearest neighbors to find
	 * @return a list of the moves corresponding to the k nearest neighbors
	 */
	private List<MOVE> knn(Game game, int k) {
		Knn_Node current = new Knn_Node(game);
		Map<Integer, MOVE> distanceMap = new HashMap<Integer, MOVE>();
		List<Integer> distances = new ArrayList<Integer>();
		for(MOVE m: game.getPossibleMoves(game.getPacmanCurrentNodeIndex())){
			for(Knn_Node n: training.get(m)){
				int dist = current.getDistance(n);
				distanceMap.put(dist, m);
				distances.add(dist);
			}
		}
		Collections.sort(distances);
		List<MOVE> neighbors = new ArrayList<MOVE>();
		for(int i = 0; i < k; i++){
			neighbors.add(distanceMap.get(distances.get(i)));
		}
		
		return neighbors;
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
