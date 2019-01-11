<?php
/**
 * Route_Planner Model
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Route_Planner_Model {

    /**
     * The best route found so far
     *
     * @var  Route_Model
     */
    public $best_route;

    /**
     * Collection of Stops
     *
     * @var Stop_Collection
     */
    public $stops;

    /**
     * Number of trucks available
     *
     * @var int
     */
    public $truck_count;

    /**
     * initial value of the pheromones
     *
     * @var float
     */
    public $initial_pheromone;

    /**
     * Rate of pheromone evaporation
     *
     * @var float
     */
    public $p;

    /**
     * Relative importance of distance
     *
     * @var int
     */
    public $beta;

    /**
     * Relative importance of exploration vs exploitation
     *
     * @var float
     */
    public $q;

    /**
     * number of times to run both ant colonies
     *
     * @var int
     */
    public $limit;

    /**
     * The capacity of a truck
     *
     * @var int
     */
    public $capacity = 10;

    /**
     * time limit for each truck
     *
     * @var int
     */
    public $time_limit = 21600;

    /**
     * @param float                         $q     relative importance of exploration vs exploitation
     * @param float                         $p     rate of pheromone evaporation
     * @param int                           $beta  relative importance of distance
     * @param int                           $limit number of times to run both ant colonies
     * @param null|Base_DAO $dao   dao to use
     */
    public function __construct($q, $p, $beta, $limit, $dao = null) {
        parent::__construct($dao);
        $this->dao           = $dao ?: new Route_Planner_DAO();
        $this->p             = $p;
        $this->q             = $q;
        $this->beta          = $beta;
        $this->limit         = $limit;
        $this->error_message = 'no errors!';
    }

    /**
     * Load the data into this model
     *
     * @param string $agent_name
     * @param string $optimize_by
     * @param string $date
     *
     * @return bool successful
     */
    public function load_data($agent_name, $optimize_by, $date) {
        $route             = new Route_Model();
        $depot             = $this->dao->get_agent_data($agent_name)[0];
        $depot['is_depot'] = true;
        $stops             = new Stop_Collection();
        if (!$stops->load_order_data($agent_name, $date)) {
            $route->add_error('no orders', $route->no_orders_message);
            $this->best_route = $route;

            return false;
        }
        $stops->append_model($depot);
        $stops->load_distances();
        $stops->initialize_closeness($optimize_by);
        $this->stops          = $stops;
        $route->optimize_by   = $optimize_by;
        $route->date          = $date;
        $route->depot_address = $this->stops->search('is_depot', true)->full_address;
        $route->depot_id      = $depot['id'];
        $this->best_route     = $route;

        return true;
    }

    /**
     * Generate routes
     *
     * @return bool success
     */
    public function generate_routes() {
        $trucks = $this->truck_count;
        $this->get_initial_solution();
        $distance_graph = $this->stops;
        $trucks_graph   = $this->stops;
        $counter        = 0;
        while ($counter < $this->limit) {

            $distance_solution = $this->run_ants($distance_graph, $trucks);

            $trucks_solution = null;
            //if we only have 1 truck we can only optimize time
            if ($trucks > 1) {
                $trucks_solution = $this->run_ants($trucks_graph, $trucks - 1);
            }

            $best_solution = $this->best_route;
            //if the current best route is not valid, don't compare it to our options
            if (!$this->best_route->is_valid) {
                if (empty($trucks_solution)) {
                    if (!empty($distance_solution)) {
                        $best_solution = $distance_solution;
                    }
                } else if (empty($distance_solution)) {
                    $best_solution = $trucks_solution;
                } else {
                    $best_solution = $trucks_solution->return_best($distance_solution);
                }
                //if we have a valid solution, only pick a new solution if it's better than our current one
            } else {
                if (empty($trucks_solution)) {
                    if (!empty($distance_solution)) {
                        $best_solution = $distance_solution->return_best($this->best_route);
                    }
                } else if (empty($distance_solution)) {
                    $best_solution = $trucks_solution->return_best($this->best_route);
                } else {
                    $best_solution = $trucks_solution->return_best($distance_solution)->return_best($this->best_route);
                }
            }

            if ($best_solution === $trucks_solution) {
                $trucks--;
            }

            $this->best_route = $best_solution;
            $this->global_update_pheromones($distance_graph, $this->best_route->sequence);
            $counter++;
        }
        if (!$this->best_route->is_valid) {
            $this->error_message = Route_Planner_Controller::NO_SOLUTION_MESSAGE;

            return false;
        } else {
            return true;
        }
    }

    /**
     * Get the initial solution
     */
    public function get_initial_solution() {
        $depot_visited = 0;
        $current_node  = $this->stops->search('is_depot', true);
        $distance      = 0;
        $time          = 0;
        while (!empty($this->stops->search('available', true))) {
            $this->best_route->sequence[] = $current_node->id;
            //update availability
            if ($current_node->is_depot) {
                $depot_visited += 1;
                if ($depot_visited === $this->truck_count) {
                    $current_node->available = false;
                }
            } else {
                $this->best_route->add_stop($current_node);
                $current_node->available = false;
            }
            $next_node = null;
            //pick the next node to visit
            foreach ($current_node->closeness as $i => $d) {
                $node = $this->stops->search('id', $i);
                //if this node exists and is available, pick it as the next node to visit
                if (!empty($node) && $node->available) {
                    $next_node = $node;
                    break;
                }
            }
            //if there is no next node, we're done
            if (empty($next_node)) {
                //if we didn't end on a depot, return to the depot
                if (!$current_node->is_depot) {
                    $next_node = $this->stops->search('is_depot', true);
                } else {
                    break;
                }
            }
            //update values for this path
            $distance += $current_node->meters[$next_node->id];
            $time += $current_node->seconds[$next_node->id];

            //if this is a depot, update values for journey leg and reset counters
            if ($current_node->is_depot) {
                $this->best_route->visit_depot($distance, $time);
                $distance = 0;
                $time     = 0;
            }
            $current_node = $next_node;
        }
        $this->best_route->check_valid($this->capacity, $this->time_limit);

        //initialize pheromones based on this solution
        $pheromones              = $this->stops->initialize_pheromones(
            $this->beta,
            count($this->best_route->sequence)
        );
        $this->initial_pheromone = $pheromones;
    }

    /**
     * Run an ant colony on the given graph with the given number of trucks
     *
     * @param Stop_Collection $graph  the graph to run on
     * @param int                                              $trucks the number of trucks to use
     *
     * @return Route_Model | null the best route found
     */
    public function run_ants($graph, $trucks) {
        //initialize ants
        $ant_count      = 1;
        $availabilities = array_fill_keys($graph->values_for_key('id'), true);
        $current_stop   = $graph->search('is_depot', true);
        $ants           = new Ant_Collection($ant_count, $current_stop, $availabilities);

        //run while there are active ants
        while (!empty($ants->search('done', false))) {
            //for each ant make one move
            foreach ($ants as $ant) {
                if ($ant->done === false) {
                    $current_stop           = $ant->current_stop;
                    $ant->route->sequence[] = $current_stop->id;
                    //update availability for this node
                    if ($current_stop->is_depot) {
                        $ant->visit_depot();
                        if ($ant->depot_visited_count === $trucks + 1) {
                            $ant->availabilities[$current_stop->id] = false;
                        }
                    } else {
                        $ant->route->add_stop($current_stop);
                        $ant->availabilities[$current_stop->id] = false;
                    }
                    //choose the next node
                    $next_node = $this->choose_next($graph, $ant->availabilities, $current_stop);
                    //if choose next returns null, we have visited all customers
                    if (empty($next_node)) {
                        //if we didn't end on a depot, return to the depot if possible
                        if (!$current_stop->is_depot && $ant->depot_visited_count < $trucks + 1) {
                            $next_node = $graph->search('is_depot', true);
                        } else {
                            $ant->route->visit_depot($ant->distance, $ant->time);
                            $ant->done = true;
                        }
                    }

                    if (!empty($next_node)) {
                        //if we don't have the time or capacity to make another stop, return to the depot
                        if (!$current_stop->is_depot && !$next_node->is_depot) {
                            $depot_id      = $graph->search('is_depot', true)->id;
                            $time_to_depot = $ant->time + $current_stop->seconds[$next_node->id] +
                                $next_node->seconds[$depot_id];
                            $one_more      = $time_to_depot < $this->time_limit || $ant->capacity !== $this->capacity;
                            if (!$one_more) {
                                $next_node = $graph->search('is_depot', true);
                            }
                        }
                        if ($ant->current_stop->is_depot) {
                            $ant->route->visit_depot($ant->distance, $ant->time);
                            $ant->reset_counters();
                        }
                        $time     = $current_stop->seconds[$next_node->id];
                        $distance = $current_stop->meters[$next_node->id];
                        $ant->increase_counters($time, $distance);
                        $ant->set_last($current_stop->id);
                        $ant->set_current($next_node);
                    }
                }
            }
            //for each move made, update the pheromones
            foreach ($ants as $ant) {
                if (!empty($ant->last_stop_id)) {
                    $this->local_update_pheromones($graph, $ant->last_stop_id, $ant->current_stop->id);
                    if ($ant->done) {
                        $ant->last_stop_id = null;
                    }
                }
            }
        }
        //find the fastest solution the colony found
        $ants->check_valid($this->capacity, $this->time_limit);
        $possible_solutions = $ants->search_all('valid_solution', true);
        if ($possible_solutions->count() === 0) {
            return null;
        }
        $best_solution = $possible_solutions->get_first_model()->route;
        foreach ($possible_solutions as $ant) {
            $best_solution = $best_solution->return_best($ant->solution);
        }

        return $best_solution;
    }

    /**
     * increase the pheromones along the given sequence in the given graph
     *
     * @param Stop_Collection $graph    the graph to use
     * @param array                                            $sequence the sequence to increase
     */
    public function global_update_pheromones($graph, $sequence) {
        $from = $sequence[0];
        for ($i = 1; $i < count($sequence); $i++) {
            $to = $sequence[$i];
            $graph->search('id', $from)->increase_pheromone($this->p, $this->beta, $to, count($sequence));
            $from = $to;
        }
    }

    /**
     * Decrease the pheromones along the path between the two given stops in the given graph
     *
     * @param Stop_Collection $graph the graph to use
     * @param string                                           $from  the 'from' stop
     * @param string                                           $to    the 'to' stop
     */
    public function local_update_pheromones($graph, $from, $to) {
        $graph->search('id', $from)->decrease_pheromone($this->p, $this->beta, $to, $this->initial_pheromone);
    }

    /**
     * Choose the next node in the given graph from the given stop and availability array
     *
     * @param Stop_Collection $graph          the graph to use
     * @param array                                            $availabilities the availabilities to use
     * @param Stop_Model      $current_stop   the current stop
     *
     * @return null|Stop_Model the next stop to visit
     */
    public function choose_next($graph, $availabilities, $current_stop) {
        $available_stops   = $graph->models;
        $unavailable_stops = $graph->models;
        $available         = function ($model) use ($availabilities) {
            return $availabilities[$model->id];
        };
        $available_stops   = array_filter($available_stops, $available);
        if (empty($available_stops)) {
            return null;
        }
        $unavailable       = function ($model) use ($availabilities) {
            return !$availabilities[$model->id];
        };
        $unavailable_stops = array_filter($unavailable_stops, $unavailable);

        $attractivenesses = $current_stop->attractiveness;
        // remove probabilities for unavailable stops, since we won't be picking them
        foreach ($unavailable_stops as $unavailable_stop) {
            unset($attractivenesses[$unavailable_stop->id]);
        }
        if (empty($attractivenesses)) {
            return null;
        }

        $q_rand         = $this->float_rand(0, 1);
        $chosen_node_id = null;
        if ($q_rand < $this->q) {
            // get id of node with the highest attractiveness
            $chosen_node_id = array_search(max($attractivenesses), $attractivenesses);
        } else {
            // normalize attractiveness values to get probabilities
            $probabilities      = [];
            $attractiveness_sum = array_sum($attractivenesses);
            if ($attractiveness_sum != 0) {
                foreach ($attractivenesses as $i => $attractiveness) {
                    $probabilities[$i] = $attractiveness / $attractiveness_sum;
                }
            } else {
                $probabilities = $attractivenesses;
            }
            $probabilities_cumulative = [];
            $current_sum              = 0;
            foreach ($probabilities as $i => $probability) {
                $current_sum += $probabilities[$i];
                $probabilities_cumulative[$i] = $current_sum;
            }
            // this should be 1, but check just in case
            $probabilities_sum = array_sum($probabilities);
            $rand              = $this->float_rand(0, $probabilities_sum);
            // chooses a node with weighted randomness based on probabilities
            foreach ($probabilities_cumulative as $i => $probability) {
                if ($rand <= $probability) {
                    $chosen_node_id = $i;
                    break;
                }
            }
        }
        $chosen_node = $graph->search('id', $chosen_node_id);

        return $chosen_node;
    }

    /**
     * Generates a random float between the given numbers
     *
     * @param int $min the min number
     * @param int $max the max number
     *
     * @return float|int a random float
     */
    function float_rand($min = 0, $max = 1) {
        $decimals = 4;
        $scale    = pow(10, $decimals);
        \WF\Shared\Logging\Logger::use_logger('tami_test')->error('expiration', ['beans' => $scale]);

        return mt_rand($min * $scale, intval($max * $scale)) / $scale;
    }
}