package pacman.controllers.zoe_winkworth;

import pacman.game.Game;

/**
 * @author Amy Hoover
 * 
 * This representation of a Node was written by
 * Amy Hoover.
 */
public class DFS_Node 
{
    Game gameState;
    int depth;
    
    public DFS_Node(Game game, int depth)
    {
        this.gameState = game;
        this.depth = depth;
    }
}
