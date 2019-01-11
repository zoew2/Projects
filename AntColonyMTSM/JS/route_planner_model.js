/**
 * Route Planner Tungsten Model
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */

define('route_planner_model', [
    'wf_model_base'
], function(BaseModel) {
    'use strict';

    var RoutePlannerModel = BaseModel.extend({
        defaults: {
            date: null,
            truck_count_default: '5',
            truck_ids: [],
            driver_ids: []
        },
        /**
         * sets initial parameters to defaults
         */
        postInitialize: function() {
            this.getAgents();
            this.set('truck_count', this.get('truck_count_default'));
            this.set('agent_name', 'Airport Courier Service');
            this.set('optimize_by', 'seconds');
            // set date to the date shown in the datepicker, should be today's date
            this.updateDate();
        },
        /**
         * get the agents' names
         */
        getAgents: function () {
            this.fetch({
                url: '/a/transportation/route_planner/get_agents',
                method: 'GET',
                dataType: 'json'
            }).done(function() {
            });
        },
        /**
         * sets the date to formatted date from the datepicker component
         */
        updateDate: function () {
            this.set('date', this.getDeep('delivery_datepicker_component:formatted'));
        },
        /**
         * if number of trucks is valid, fetch the routes from the route planner
         * passes in the current values for truck count, agent name, optimize by, and date.
         */
        generateRoutes: function () {
            if (this.get('truck_count') !== '0'){
                var self = this;
                this.fetch({
                    url: '/a/transportation/route_planner/generate_routes',
                    method: 'GET',
                    data: {
                        truck_count: self.get('truck_count'),
                        agent_name: self.get('agent_name'),
                        optimize_by: self.get('optimize_by'),
                        date: self.get('date')
                    },
                    dataType: 'json'
                }).done(function(response) {
                    if (!response.errors) {
                        self.set('route_generated', true);
                    } else {
                        self.set('route_generated', false);
                    }
                });
            }
        },
        /**
         * saves the route to the database
         */
        saveRoute: function () {
            var self = this;
            this.fetch({
                url: '/a/transportation/route_planner/save_route',
                method: 'POST',
                data: {
                    agent_id: self.getDeep('route:depot_id'),
                    date: self.get('date'),
                    trucks: self.getDeep('route:trucks'),
                    driver_ids: self.get('driver_ids'),
                    truck_ids: self.get('truck_ids')
                },
                dataType: 'json'
            }).fail(function() {
                self.set('success', 'Success!');
            });
        }
    }, {
        debugName: 'RoutePlannerModel'
    });
    return RoutePlannerModel;
});