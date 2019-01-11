<?php
/**
 * Stop Collection
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Stop_Collection {

    /**
     * The id of this truck route
     *
     * @var int
     */
    public $route_id;

    /**
     * The id of the truck assigned to this route
     *
     * @var int
     */
    public $truck_id;

    /**
     * The id of the driver assigned to this route
     *
     * @var int
     */
    public $driver_id;

    /**
     * The total time of this truck route in seconds
     *
     * @var int
     */
    public $truck_seconds = 0;

    /**
     * The total distance of this truck route in meters
     *
     * @var int
     */
    public $truck_meters = 0;

    /**
     * The total time of this truck route in hours and minutes as a string
     *
     * @var string
     */
    public $truck_time;

    /**
     * The total distance of this truck route in miles as a string
     *
     * @var string
     */
    public $truck_distance;

    /**
     * the url to the map of this truck route
     *
     * @var string
     */
    public $map_url;

    /**
     * Creates and Populates Stop Model
     *
     * @param array $map model attributes
     *
     * @return Stop_Model
     */
    public function create_model($map) {
        $model = new Stop_Model();
        $model->populate($map);

        return $model;
    }

    /**
     * Stop_Collection constructor.
     *
     * @param null $dao the dao to use
     */
    public function __construct($dao = null) {
        $this->dao = $dao ?: new Route_Planner_DAO();
    }

    /**
     * Load all the order data for a given agent and date
     *
     * @param string $agent_name the agent to pull orders for
     * @param string $date       the date to pull orders for
     *
     * @return bool success
     */
    public function load_order_data($agent_name, $date) {
        $orders = $this->dao->get_order_data($agent_name, $date);
        if ($orders) {
            $this->populate($orders);

            return true;
        } else {
            return false;
        }
    }

    /**
     * Load the distances for this collection of stops
     *
     * @return void
     */
    public function load_distances() {
        foreach ($this as $model) {
            $model->set_distances($this);
        }
    }

    /**
     * Initialize the pheromone strengths for this collection of stops
     *
     * @param int $beta   the relative importance of closeness
     * @param int $length the length of the initial path
     *
     * @return float the initial pheromone value
     */
    public function initialize_pheromones($beta, $length) {
        $pheromones        = [];
        $initial_pheromone = 1 / ($this->count() * $length);
        foreach ($this as $model) {
            $pheromones[$model->id] = $initial_pheromone;
        }
        foreach ($this as $model) {
            $pheromones_dup = $pheromones;
            // remove the pheromone referring to the current stop
            unset($pheromones_dup[$model->id]);
            $model->pheromones = $pheromones_dup;
            $model->initialize_attractiveness($beta);
        }

        return $initial_pheromone;
    }

    /**
     * Initialize the closeness measures for this collection of stops
     *
     * @param string $optimize_by whether we're using time or distance
     *
     * @return void
     */
    public function initialize_closeness($optimize_by) {
        foreach ($this as $model) {
            $model->set_closeness($optimize_by);
        }
    }

    /**
     * Set values in this collection from the given array
     *
     * @param $map array of values
     *
     * @return void
     */
    public function set_values($map) {
        foreach (array_keys(get_object_vars($this)) as $key) {
            if (isset($map[$key])) {
                $this->$key = $map[$key];
            }
        }
    }

    /**
     * Load all the deliveries for this truck
     *
     * @return void
     */
    public function load_delivery_stops() {
        $stops = $this->dao->get_deliveries($this->route_id);
        $this->populate($stops);
    }

    /**
     * Build the map url for this truck route
     *
     * @param string $depot_address the address of the depot we're using
     *
     * @return void;
     */
    function build_map_url($depot_address) {
        $url_part_1 = 'https://maps.googleapis.com/maps/api/staticmap?';
        $size       = 'size=550x300';
        $markers    = '&markers=' . 'color:blue%7C' . urlencode($depot_address);
        $label      = 'A';
        foreach ($this as $stop) {
            $markers = $markers . '&markers=' . 'label:' . $label . '%7C' . urlencode($stop->full_address);
            $label++;
        }
        $parameters    = $size . $markers;
        $key           = '&key=AIzaSyBAFEbAHnhuQVeFfxCSWeuaUazHPaN2K5A';
        $url           = $url_part_1 . $parameters . $key;
        $this->map_url = $url;
    }

    /**
     * Set the sequence letters for the stops this truck makes
     *
     * @return void
     */
    public function set_sequence_letters() {
        $letter = 'A';
        foreach ($this as $stop) {
            $stop->sequence_letter = $letter;
            $letter++;
        }
    }
}