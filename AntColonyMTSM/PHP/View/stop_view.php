<?php
/**
 * Stop View
 *
 * PHP version 5
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */
namespace AntColonyMTSM;

class Stop_View {

    /**
     * The name of the template for this view
     *
     * @return string
     */
    protected function template_name() {
        return '';
    }

    /**
     * the js view
     *
     * @return string
     */
    protected function tungsten_view_module() {
        return 'stop_view';
    }

    /**
     * the js model
     *
     * @return string
     */
    protected function tungsten_model_module() {
        return 'stop_model';
    }
}