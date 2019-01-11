<?php
/**
 * Ant Model
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Ant_Model {

    /**
     * The current stop this ant is visiting
     *
     * @var Stop_Model
     */
    public $current_stop;

    /**
     * The id of the last stop this ant visited
     *
     * @var int
     */
    public $last_stop_id = null;

    /**
     * Current distance since last depot visit
     *
     * @var int
     */
    public $distance = 0;

    /**
     * Current time since last depot visit
     *
     * @var int
     */
    public $time = 0;

    /**
     * Current capacity since last depot visit
     *
     * @var int
     */
    public $capacity = 0;

    /**
     * Number of times this ant has visited the depot
     *
     * @var int
     */
    public $depot_visited_count = 0;

    /**
     * The route this ant has built so far
     *
     * @var Route_Model
     */
    public $route;

    /**
     * Has this ant finished finding a route
     *
     * @var bool
     */
    public $done = false;

    /**
     * An array of all the stop ids and whether or not they are available for this ant to visit
     *
     * @var array
     */
    public $availabilities;

    /**
     * Has this ant fount a valid route?
     *
     * @var bool
     */
    public $valid_route = false;

    /**
     * Set the id of the last stop this ant visited
     *
     * @param int $last_stop_id
     *
     * @return void
     */
    public function set_last($last_stop_id) {
        $this->last_stop_id = $last_stop_id;
    }

    /**
     * Set the current stop this ant is visiting
     *
     * @param Stop_Model $current_stop
     *
     * @return void
     */
    public function set_current($current_stop) {
        $this->current_stop = $current_stop;
    }

    /**
     * Increases the current time, distance and capacity since last depot visit
     *
     * @param int $time     time since last depot visit
     * @param int $distance distance since last depot visit
     *
     * @return void
     */
    public function increase_counters($time, $distance) {
        $this->time += $time;
        $this->distance += $distance;
        $this->capacity += 1;
    }

    /**
     * Reset all counters
     *
     * @return void
     */
    public function reset_counters() {
        $this->time     = 0;
        $this->distance = 0;
        $this->capacity = 0;
    }

    /**
     * Increase the depot_visited_count
     *
     * @return void
     */
    public function visit_depot() {
        $this->depot_visited_count += 1;
    }

    /**
     * Check if this ant has a valid route given the problem constraints
     *
     * @param int $capacity   the capacity of a truck
     * @param int $time_limit the time limit for a truck
     *
     * @return bool does this ant have a valid route
     */
    public function check_valid($capacity, $time_limit) {
        $this->valid_route = $this->route->check_valid($capacity, $time_limit);

        return $this->valid_route;
    }
}