<?php
/**
 * Stop Model
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Stop_Model {

    /**
     * The first line of the address
     *
     * @var string
     */
    public $address_1;

    /**
     * The second line of the address
     *
     * @var string
     */
    public $address_2;

    /**
     * The city for the address
     *
     * @var string
     */
    public $city;

    /**
     * The state for the address
     *
     * @var string
     */
    public $state;

    /**
     * The zip code for the address
     *
     * @var string
     */
    public $zip;

    /**
     * The full address of this stop
     *
     * @var string
     */
    public $full_address;

    /**
     * Is this stop available to be visited?
     *
     * @var bool
     */
    public $available = true;

    /**
     * ID to identify this stop (either order id or agent id)
     *
     * @var string
     */
    public $id;

    /**
     * Array of distances from this stop to all others in meters
     *
     * @var array
     */
    public $meters = [];

    /**
     * Array of closeness from this stop to all others in meters
     * (closeness = 1 / distance where distance is either seconds or meters depending on what we're optimizing)
     *
     * @var array
     */
    public $closeness = [];

    /**
     * Array of times from this stop to all others in seconds
     *
     * @var array
     */
    public $seconds = [];

    /**
     * Array of pheromone strength for the path from this stop to all others
     *
     * @var array
     */
    public $pheromones;

    /**
     * Array of attractiveness of all other stops
     * (attractiveness is calculated using distance and pheromones)
     *
     * @var array
     */
    public $attractiveness;

    /**
     * This stop's sequence number in it's truck
     *
     * @var int
     */
    public $sequence_num;

    /**
     * Is this stop a depot?
     *
     * @var bool
     */
    public $is_depot = false;

    /**
     * Stop_Model constructor.
     *
     * @param null $dao the dao to use
     */
    public function __construct($dao = null) {
        parent::__construct($dao);
        $this->dao = $dao ?: new Route_Planner_DAO();
    }

    /**
     * Populates this model with data
     *
     * @param array $map
     *
     * @return Stop_Model
     */
    public function populate($map) {
        parent::populate($map);
        $this->full_address = $this->address_1 .
            ' ' . $this->address_2 .
            ' ' . $this->city .
            ' ' . $this->state .
            ' ' . $this->zip;

        return $this;
    }

    /**
     * Set the distances array
     *
     * @param Stop_Collection $stops
     *
     * @return void
     */
    public function set_distances($stops) {
        foreach ($stops as $stop) {
            if ($stop->id !== $this->id) {
                $distance = $this->dao->get_distances($this->id, $stop->id);
                if ($distance) {
                    $this->meters[$distance['stop_to']]  = $distance['meters'];
                    $this->seconds[$distance['stop_to']] = $distance['seconds'];
                } else {
                    $url      = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
                        . urlencode($this->full_address)
                        . "&destinations="
                        . urlencode($stop->full_address)
                        . "&key=AIzaSyDUi5F0omWCqjn7NnA1qrY9lTpVTyC3GO8";
                    $response = json_decode(file_get_contents($url))->rows[0]->elements[0];
                    $distance = $response->distance->value;
                    $duration = $response->duration->value;
                    $this->dao->save_distances($this->id, $stop->id, $duration, $distance);
                    $this->meters[$stop->id]  = $duration;
                    $this->seconds[$stop->id] = $distance;
                }
            }
        }
    }

    /**
     * Decrease the pheromone strength at this stop
     *
     * @param float $p      how fast the pheromone fades
     * @param int   $beta   how important closeness is over pheromone strength
     * @param int   $id     the id of the stop to increase for
     * @param int   $length the length of the shortest path
     *
     * @return void
     */
    public function increase_pheromone($p, $beta, $id, $length) {
        $pheromone_trail           = (1 - $p) * $this->pheromones[$id] + ($p / $length);
        $this->pheromones[$id]     = $pheromone_trail;
        $this->attractiveness[$id] = $this->pheromones[$id] * pow($this->closeness[$id], $beta);
    }

    /**
     * Decrease the pheromone strength at this stop
     *
     * @param float $p                 how fast the pheromone fades
     * @param int   $beta              how important closeness is over pheromone strength
     * @param int   $id                the id of the stop to increase for
     * @param float $initial_pheromone the initial pheromone value
     */
    public function decrease_pheromone($p, $beta, $id, $initial_pheromone) {
        $pheromone_trail = (1 - $p) * $this->pheromones[$id] + ($p * $initial_pheromone);
        if ($pheromone_trail !== 0) {
            $this->pheromones[$id]     = $pheromone_trail;
            $this->attractiveness[$id] = $this->pheromones[$id] * pow($this->closeness[$id], $beta);
        }
    }

    /**
     * Initialize the atractiveness array
     *
     * @param int $beta how important closeness is over pheromone strength
     */
    public function initialize_attractiveness($beta) {
        foreach ($this->pheromones as $id => $pheromone) {
            $this->attractiveness[$id] = $pheromone * pow($this->closeness[$id], $beta);
        }
    }

    /**
     * Set the closeness array
     *
     * @param string $optimize_by whether we're optimizing by time or distance
     */
    public function set_closeness($optimize_by) {
        $distances = [];
        if ($optimize_by === 'seconds') {
            $distances = $this->seconds;
        } else if ($optimize_by === 'meters') {
            $distances = $this->meters;
        }
        foreach ($distances as $id => $distance) {
            if ($distance === '0') {
                $this->closeness[$id] = 1;
            } else {
                $this->closeness[$id] = 1 / $distance;
            }
        }
    }
}