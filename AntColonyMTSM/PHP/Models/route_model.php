<?php
/**
 * Route Model
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Route_Model {

    /**
     * The address of the depot used for this route
     *
     * @var string
     */
    public $depot_address;

    /**
     * The id of the depot used for this route
     *
     * @var int
     */
    public $depot_id;

    /**
     * An array of stop collections representing each truck used for this route
     *
     * @var Stop_Collection[]
     */
    public $trucks = [];

    /**
     * The current truck being constructed for this route
     *
     * @var Stop_Collection
     */
    public $current_truck;

    /**
     * An array of stop ids in the order that this route visits them
     *
     * (a stop id is either an order id or an agent id)
     *
     * @var array
     */
    public $sequence = [];

    /**
     * The date we are constructing this route for
     *
     * @var string
     */
    public $date;

    /**
     * The total time this route takes in seconds
     *
     * @var int
     */
    public $total_seconds = 0;

    /**
     * The total distance this route covers in meters
     *
     * @var int
     */
    public $total_meters = 0;

    /**
     * Whichever total we are optimizing
     *
     * @var int
     */
    public $total_optimized = 0;

    /**
     * The total time this route takes as a string in hours and minutes
     *
     * @var string
     */
    public $total_time;

    /**
     * The total distance this route covers as a string in miles
     *
     * @var string
     */
    public $total_distance;

    /**
     * The measure to optimize by
     * (either 'seconds' or 'meters')
     *
     * @var string
     */
    public $optimize_by;

    /**
     * Is this route valid?
     *
     * @var bool
     */
    public $is_valid = false;

    /**
     * Route_Model constructor.
     *
     * @param null $dao
     */
    public function __construct($dao = null) {
        parent::__construct($dao);
        $this->dao = $dao ?: new Route_Planner_DAO();
    }

    /**
     * Set the total time and distance strings
     *
     * @return void
     */
    public function set_totals() {
        $this->total_time     = $this->seconds_to_hours($this->total_seconds);
        $this->total_distance = $this->meters_to_miles($this->total_meters);
        if (!empty($this->trucks)) {
            foreach ($this->trucks as $truck) {
                $truck->truck_time     = $this->seconds_to_hours($truck->truck_seconds);
                $truck->truck_distance = $this->meters_to_miles($truck->truck_meters);
            }
        }
    }

    /**
     * Convert seconds to hours and minutes and put them in a string
     *
     * @param int $seconds the seconds to convert
     *
     * @return string the hours and minutes
     */
    public function seconds_to_hours($seconds) {
        $hr_min = '';
        $hours  = intval($seconds / 3600);
        if ($hours > 0) {
            if ($hours === 1) {
                $hr_min .= $hours . 'hr ';
            } else {
                $hr_min .= $hours . 'hrs ';
            }
        }
        $seconds = $seconds - ($hours * 3600);
        $minutes = intval($seconds / 60);
        if ($minutes > 0) {
            if ($minutes === 1) {
                $hr_min .= $minutes . 'min';
            } else {
                $hr_min .= $minutes . 'mins';
            }
        }

        return $hr_min;
    }

    /**
     * Convert meters to miles and put them in a string
     *
     * @param int $meters the meters to convert
     *
     * @return string the miles
     */
    public function meters_to_miles($meters) {
        $miles = intval($meters * 0.000621371);
        if ($miles === 1) {
            return $miles . ' mile';
        } else {
            return $miles . ' miles';
        }
    }

    /**
     * Add time and distance elapsed since last depot visit to route totals,
     * set time and distance elapsed since last depot visit to truck totals,
     * add the current truck to the array of trucks in this route
     * and create a new, empty truck to set as the current truck
     *
     * @param int $distance distance covered since last depot visit
     * @param int $time     time passed since last depot visit
     *
     * @return void
     */
    public function visit_depot($distance, $time) {
        if ($this->optimize_by === 'seconds') {
            $this->total_optimized += $time;
        } else if ($this->optimize_by === 'meters') {
            $this->total_optimized += $distance;
        }
        $this->total_seconds += $time;
        $this->total_meters += $distance;
        if (!empty($this->current_truck)) {
            $this->current_truck->truck_seconds  = $time;
            $this->current_truck->truck_distance = $distance;
            $this->trucks[]                      = $this->current_truck;
        }
        $this->current_truck = new Stop_Collection();
    }

    /**
     * Add a stop to the current truck
     *
     * @param Stop_Model $stop the stop to add
     *
     * @return void
     */
    public function add_stop($stop) {
        $stop->sequence_num            = $this->current_truck->count() + 1;
        $this->current_truck->models[] = $stop;

    }

    /**
     * Checks if this route is valid given the problem constraints
     *
     * @param int $capacity   capacity limit for a truck
     * @param int $time_limit time limit for a truck
     *
     * @return bool is this a valid route?
     */
    public function check_valid($capacity, $time_limit) {
        foreach ($this->trucks as $truck) {
            if (count($truck->models) > $capacity || $truck->truck_seconds > $time_limit) {
                $this->is_valid = false;
            } else {
                $this->is_valid = true;
            }
        }

        return $this->is_valid;
    }

    /**
     * Given another route model, check if it is a better route than this route
     * and return the best route
     *
     * @param  Route_Model $route the given route
     *
     * @return Route_Model the best route
     */
    public function return_best($route) {
        if ($this->total_optimized < $route->total_optimized) {
            return $this;
        } else {
            return $route;
        }
    }

    /**
     * Loads this route model and populates all the trucks and stops for each truck
     *
     * @param string $date the date this route is for
     *
     * @return void
     */
    public function load_route($date) {
        $rows        = $this->dao->get_routes($date);
        $depot       = $this->dao->get_agent_data($rows[0]['agent_name'])[0];
        $depot_model = new Stop_Model();
        $depot_model->populate($depot);
        $this->depot_address = $depot_model->full_address;
        $this->depot_id      = $depot_model->id;
        foreach ($rows as $row) {
            $truck = new Stop_Collection();
            $truck->set_values($row);
            $truck->load_delivery_stops();
            $this->trucks[] = $truck;
        }
    }

    /**
     * Save this route in the database
     *
     * @param array $trucks     the truck routes for this route
     * @param array $driver_ids the ids of drivers used on this route
     * @param array $truck_ids  the ids of trucks used for this route
     *
     * @return void
     */
    public function save_routes($trucks, $driver_ids, $truck_ids) {
        foreach ($trucks as $i => $truck) {
            $truck_id  = $driver_ids[$i];
            $driver_id = $truck_ids[$i];
            $this->dao->save_route(
                $this->depot_id,
                $truck_id,
                $driver_id,
                $this->date,
                $truck['truck_seconds'],
                $truck['truck_meters']
            );
            $this->dao->set_driver_unavailable($driver_id);
            $this->dao->set_truck_unavailable($truck_id);
            $route_id = $this->dao->get_route_id($truck_id, $driver_id, $this->date)['route_id'];
            foreach ($truck['models'] as $stop) {
                $this->dao->save_delivery($stop['id'], $route_id, $this->date, $stop['sequence_num']);
            }
        }
    }

    /**
     * Delete the given truck routes
     *
     * @param array $route_ids route ids for each truck route
     *
     * @return void
     */
    public function delete_route($route_ids) {
        foreach ($route_ids as $route_id) {
            $this->dao->set_driver_available($route_id);
            $this->dao->set_truck_available($route_id);
            $this->dao->delete_route($route_id);
            $this->dao->delete_deliveries($route_id);
        }
    }

    /**
     * Set the map urls for each truck route
     *
     * @return void
     */
    public function set_map_urls() {
        foreach ($this->trucks as $i => $truck) {
            $truck->build_map_url($this->depot_address);
        }
    }

    /**
     * Set sequence letters for each truck route
     *
     * @return void
     */
    public function set_sequence_letters() {
        foreach ($this->trucks as $i => $truck) {
            $truck->set_sequence_letters();
        }
    }
}