<?php
/**
 * Route Planner Dao
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Route_Planner_DAO {

    /**
     * Get all the orders for a given agent on a given date
     *
     * @param string $agent_name the agent to pull orders for
     * @param string $date       the date to pull orders for
     *
     * @return array|mixed the orders
     */
    public function get_order_data($agent_name, $date) {
        $sql = 'SELECT    OrID as id,
                      OrAddress1 as address_1,
                      OrAddress2 as address_2,
                      OrCity as city,
                      OrState as state,
                      OrZip as zip,
                      OrExpectedDate as order_expected_date,
					            OrStatusID
            FROM       tblOrder   WITH (NOLOCK)
            INNER JOIN tblplAgent WITH (NOLOCK)
			      ON OrAgentID = AgID
            WHERE     AgName = :agent_name
			      AND       OrStatusID = 1
			      AND       OrExpectedDate = :date
            ORDER BY  OrID DESC';

        $statement = PDO::new_statement('TRNS', $sql, PDO::CACHE_TIME_ONE_DAY);
        $statement->bindValue(':agent_name', $agent_name, PDO::PARAM_INT);
        $statement->bindValue(':date', $date, PDO::PARAM_STR);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Get all the agents in the database
     *
     * @return array|mixed the agent names
     */
    public function get_all_agents() {
        $sql = 'SELECT    AgName as name
            FROM      tblplAgent WITH (NOLOCK)
            ORDER BY  AgID ASC';

        $statement = PDO::new_statement('TRNS', $sql, PDO::CACHE_TIME_ONE_DAY);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Gets all agent data for a given agent
     *
     * @param string $agent_name the agent to pull data for
     *
     * @return array|mixed agent data
     */
    public function get_agent_data($agent_name) {
        $sql = 'SELECT    AgID as id,
                      AgAddress1 as address_1,
                      AgAddress2 as address_2,
                      AgCity as city,
                      AgState as state,
                      AgZip as zip
            FROM      tblplAgent WITH (NOLOCK)
            WHERE AgName = :agent_name
            ORDER BY  AgID ASC';

        $statement = PDO::new_statement('TRNS', $sql, PDO::CACHE_TIME_ONE_DAY);
        $statement->bindValue(':agent_name', $agent_name, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Get a distance measure between two stops
     *
     * @param int $stop_from id of 'from' stop
     * @param int $stop_to   id of 'to' stop
     *
     * @return array|bool|mixed distance
     */
    public function get_distances($stop_from, $stop_to) {
        $sql = 'SELECT    DistTo as stop_to,
                      DistSeconds as seconds,
                      DistMeters as meters
            FROM      tblDistances WITH (NOLOCK)
            WHERE     DistFrom = :stop_from
            AND     DistTo = :stop_to
            ORDER BY  DistSeconds ASC';

        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':stop_from', $stop_from, PDO::PARAM_INT);
        $statement->bindValue(':stop_to', $stop_to, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Save a distance measure between two stops
     *
     * @param int $from     id of 'from' stop
     * @param int $to       id of 'to' stop
     * @param int $duration time between stops
     * @param int $distance distance between stops
     *
     * @return array|mixed
     */
    public function save_distances($from, $to, $duration, $distance) {
        $sql       = 'INSERT INTO tblDistances(
                      DistFrom,
                      DistTo,
                      DistSeconds,
					            DistMeters
              )VALUES (
                      :from,
                      :to,
                      :duration,
                      :distance)';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':from', $from, PDO::PARAM_INT);
        $statement->bindValue(':to', $to, PDO::PARAM_INT);
        $statement->bindValue(':duration', $duration, PDO::PARAM_INT);
        $statement->bindValue(':distance', $distance, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Get saved routes for a given date
     *
     * @param string $date the date to pull routes from
     *
     * @return array|mixed
     */
    public function get_routes($date) {
        $sql       = 'SELECT RoID as route_id,
                   RoTrID as truck_id,
                   RoDrID as driver_id,
                   RoTime as truck_seconds,
                   RoDistance as truck_meters,
                   AgName as agent_name
            FROM tblRoute WITH (NOLOCK)
			      INNER JOIN tblplAgent WITH (NOLOCK)
			      ON RoAgID = AgID
            WHERE RoDate = :date
            ORDER BY RoID ASC';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':date', $date, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Save route in the database
     *
     * @param int    $agent_id  the id of the agent for this route
     * @param int    $truck_id  the id of the truck assigned to this route
     * @param int    $driver_id the id of the driver assigned to this route
     * @param string $date      the date of this route
     * @param int    $time      the total time for this route
     * @param int    $distance  the total distance for this route
     *
     * @return array|mixed
     */
    public function save_route($agent_id, $truck_id, $driver_id, $date, $time, $distance) {
        $sql       = 'INSERT INTO tblRoute(
                      RoTrID,
                      RoDrID,
                      RoDate,
                      RoTime,
                      RoDistance,
                      RoAgID
              )VALUES (
                      :truck_id,
                      :driver_id,
                      :date,
                      :time,
                      :distance,
                      :agent_id)';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':truck_id', $truck_id, PDO::PARAM_INT);
        $statement->bindValue(':driver_id', $driver_id, PDO::PARAM_INT);
        $statement->bindValue(':date', $date, PDO::PARAM_STR);
        $statement->bindValue(':time', $time, PDO::PARAM_INT);
        $statement->bindValue(':distance', $distance, PDO::PARAM_INT);
        $statement->bindValue(':agent_id', $agent_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Delete route in the database
     *
     * @param int $route_id the route id to delete
     *
     * @return array|mixed
     */
    public function delete_route($route_id) {
        $sql       = 'DELETE FROM tblRoute
            WHERE RoID = :route_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Delete deliveries from a given route
     *
     * @param int $route_id the id of the route to delete orders for
     *
     * @return array|mixed
     */
    public function delete_deliveries($route_id) {
        $sql       = 'DELETE FROM tblDelivery
            WHERE DelRoID = :route_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Get the route id for a truck and driver on a given date
     *
     * @param int    $truck_id  the id of the truck
     * @param int    $driver_id the id of the driver
     * @param string $date      the date of the route
     *
     * @return array|bool|mixed the route id
     */
    public function get_route_id($truck_id, $driver_id, $date) {
        $sql       = 'SELECT RoID as route_id
            FROM tblRoute WITH (NOLOCK)
            WHERE RoTrID = :truck_id
            AND RoDrID = :driver_id
            AND RoDate = :date';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':truck_id', $truck_id, PDO::PARAM_INT);
        $statement->bindValue(':driver_id', $driver_id, PDO::PARAM_INT);
        $statement->bindValue(':date', $date, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Save a delivery in the database
     *
     * @param int    $order_id     the id for this order
     * @param int    $route_id     the route id for this delivery
     * @param string $date         the date for this route
     * @param int    $sequence_num the sequence number for this delivery
     *
     * @return array|mixed
     */
    public function save_delivery($order_id, $route_id, $date, $sequence_num) {
        $sql       = 'INSERT INTO tblDelivery(
                    DelOrID,
		                DelRoID,
		                DelDateTime,
		                DelSeq,
		                DelStatus
              )VALUES (
                      :order_id,
		                  :route_id,
		                  :route_date,
		                  :sequence_num,
		                  2)';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':order_id', $order_id, PDO::PARAM_INT);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);
        $statement->bindValue(':route_date', $date, PDO::PARAM_INT);
        $statement->bindValue(':sequence_num', $sequence_num, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetch() : [];
    }

    /**
     * Get all the deliveries for a given route id
     *
     * @param int $route_id the id of the route
     *
     * @return array|mixed the deliveries
     */
    public function get_deliveries($route_id) {
        $sql = 'SELECT DelOrID as id,
                   OrAddress1 as address_1,
                   OrAddress2 as address_2,
                   OrCity as city,
                   OrState as state,
                   OrZip as zip,
                   DelDateTime as date,
	                 DelSeq as sequence_num
           FROM       tblDelivery WITH (NOLOCK)
           INNER JOIN tblOrder    WITH (NOLOCK)
           ON DelOrID = OrID
           WHERE DelRoID = :route_id
           ORDER BY  id DESC';

        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Get all the trucks in the database
     *
     * @return array|mixed the truck ids
     */
    public function get_all_trucks() {
        $sql = 'SELECT TrID as truck_id
           FROM tblTruckInventory WITH (NOLOCK)
           WHERE TrAvailable = 1';

        $statement = PDO::new_statement('TRNS', $sql);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Get all the drivers in the database
     *
     * @return array|mixed the driver ids
     */
    public function get_all_drivers() {
        $sql       = 'SELECT DrID as driver_id
            FROM tblDriver WITH (NOLOCK)
            WHERE DrAvailable = 1';
        $statement = PDO::new_statement('TRNS', $sql);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Set the given driver to unavailable
     *
     * @param int $driver_id the driver to update
     *
     * @return array|mixed
     */
    public function set_driver_unavailable($driver_id) {
        $sql       = 'UPDATE tblDriver
            SET DrAvailable = 0
            WHERE DrID = :driver_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':driver_id', $driver_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Set the given truck to unavailable
     *
     * @param int $truck_id the id of the truck to update
     *
     * @return array|mixed
     */
    public function set_truck_unavailable($truck_id) {
        $sql       = 'UPDATE tblTruckInventory
            SET TrAvailable = 0
            WHERE TrID = :truck_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':truck_id', $truck_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Set the given driver to available
     *
     * @param int $route_id the id of the route the driver was assigned to
     *
     * @return array|mixed
     */
    public function set_driver_available($route_id) {
        $sql       = 'UPDATE tblDriver
            SET DrAvailable = 1
            FROM tblDriver
            INNER JOIN tblRoute
            ON RoDrID = DrID
            WHERE RoID = :route_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }

    /**
     * Set the given truck to available
     *
     * @param int $route_id the id of the route the truck was assigned to
     *
     * @return array|mixed
     */
    public function set_truck_available($route_id) {
        $sql       = 'UPDATE tblTruckInventory
            SET TrAvailable = 1
            FROM tblTruckInventory
            INNER JOIN tblRoute
            ON RoDrID = TrID
            WHERE RoID = :route_id';
        $statement = PDO::new_statement('TRNS', $sql);
        $statement->bindValue(':route_id', $route_id, PDO::PARAM_INT);

        return $statement->execute() ? $statement->fetchAll() : [];
    }
}