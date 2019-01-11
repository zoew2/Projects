<?php
/**
 * Route_Planner Controller
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Route_Planner_Controller {

  /**
   * The error message for when no route is found
   *
   * @var string
   */
  const NO_SOLUTION_MESSAGE = 'No route found. Try adding trucks';

  /**
   * The error message for when no orders are found for the given date and agent name
   *
   * @var string
   */
  const NO_ORDERS_MESSAGE = 'No orders found for that date at this depot';

  /**
   * @var string enables frontend layout
   */
  protected $layout_name = 'admin_mainlayout';

  /**
   * pre_action()
   *
   * @return void
   */
  public function pre_action() {
      $this->section_name = 'Plan a Route!';
  }

  /**
   * Main landing page
   *
   * @return void
   */
  public function index() {
    $view          = new Route_Planner_View();
    $this->content = $view;
  }

  /**
  +   * End point for the generate routes button
  +   *
  +   * @return array response to js
  +   */
  public function generate_routes() {
      $dao = new Route_Planner_DAO();
      $truck_count = intval($this->request('truck_count'));
      $agent_name  = $this->request('agent_name');
      $optimize_by = $this->request('optimize_by');
      $date        = '2017-01-11';
      $route_planner_model              = new Route_Planner_Model(0.7, 0.5, 1.5, 10);
      $route_planner_model->truck_count = $truck_count;
      if ($route_planner_model->load_data($agent_name, $optimize_by, $date)) {
          $route_planner_model->generate_routes();
      }

    $route = $route_planner_model->best_route;
    $route->set_totals();

    $drivers = $dao->get_all_drivers();
    $trucks  = $dao->get_all_trucks();

    $solution               = [];
    $solution['route']      = $route;
    $solution['driver_ids'] = $drivers;
    $solution['truck_ids']  = $trucks;
    $solution['errors']     = $route->errors;

    return $this->content = $solution;
  }

  /**
  +   * End point for get saved routes button
  +   *
  +   * @return Route_Model the saved route
  +   */
  public function get_saved_routes() {
      $date = $this->request('date');
      $route_model = new Route_Model();
      $route_model->load_route($date);
      return $this->content = $route_model;
  }

  /**
  * End point for save button
  *
  * @return void
  */
  public function save_route() {
      $agent_id   = $this->request('agent_id');
      $date       = $this->request('date');
      $trucks     = $this->request('trucks');
      $driver_ids = $this->request('driver_ids');
      $truck_ids  = $this->request('truck_options');

      $route_model           = new Route_Model();
      $route_model->depot_id = $agent_id;
      $route_model->date     = $date;
      $route_model->save_routes($trucks, $driver_ids, $truck_ids);
  }

  /**
  +   * End point for delete button
  +   *
  +   * @return void
  +   */
  public function delete_route() {
      $route_ids = $this->request('route_ids');

      $route_model = new Route_Model();
      $route_model->delete_route($route_ids);
  }

  /**
   * End point to get agents for drop down
   *
   * @return mixed response for js
   */
  public function get_agents() {
      $dao = new Route_Planner_DAO();

      $agents = $dao->get_all_agents();

      $response['agents'] = $agents;

      return $this->content = $response;
  }
}