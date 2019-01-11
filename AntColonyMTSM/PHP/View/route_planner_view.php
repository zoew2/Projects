<?php
/**
 * Route_Planner View
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Route_Planner_View {

    /**
     * The model to build this view for
     *
     * @var Route_Planner_Model
     */
    public $route_planner_model;

    /**
     * return the datepicker component
     *
     * @return Nested_Data
     */
    public function delivery_datepicker_component() {
        $datepicker_view = new Datepicker_View();
        $datepicker_view->has_timepicker = false;
        return $datepicker_view->get_nested_view();
    }

    /**
     * The name of the template for this view
     * @return string
     */
    protected function template_name() {
        return 'transportation/route_planner';
    }

    /**
     * The js view
     *
     * @return string
     */
    protected function tungsten_view_module() {
        return 'route_planner_view';
    }

    /**
     * The js model
     *
     * @return string
     */
    protected function tungsten_model_module() {
        return 'route_planner_model';
    }

}