<?php
/**
 * Ant Collection
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Ant_Collection {

    /**
     * Creates and Populates Ant Model
     *
     * @param array $map model attributes
     *
     * @return Ant_Model
     */
    public function create_model($map) {
        $model = new Ant_Model();
        $model->populate($map);

        return $model;
    }

    /**
     * Constructor for Ant Collection
     *
     * @param int                                         $ant_count      the number of ants to create
     * @param Stop_Model                   $depot          the depot we are using
     * @param array                                       $availabilities stop ids where all stops are available
     */
    public function __construct($ant_count, $depot, $availabilities) {
        $this->models = [];
        foreach (range(1, $ant_count) as $i) {
            $model                   = $this->create_model([]);
            $model->current_stop     = $depot;
            $model->availabilities   = $availabilities;
            $solution                = new Route_Model;
            $solution->depot_address = $depot->full_address;
            $solution->depot_id      = $depot->id;
            $model->route            = $solution;
            $this->models[]          = $model;
        }
    }

    /**
     * Checks and sets whether each ant in the collection has a valid route
     *
     * @param int $capacity   the capacity limit for a truck
     * @param int $time_limit the time limit for a truck
     *
     * @return void
     */
    public function check_valid($capacity, $time_limit) {
        foreach ($this as $ant) {
            $ant->check_valid($capacity, $time_limit);
        }
    }
}