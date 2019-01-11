/**
 * Route Planner Tungsten View
 *
 * @author    Tami Gabriely
 * @author    Zoe Winkworth
 */

define('route_planner_view', [
    'wf_tungsten_view_base'
], function(BaseView) {
    'use strict';

    var RoutePlannerView = BaseView.extend({
        childViews: {
            'js-stop': BaseView
        },
        events: {
            'click .js-generate-routes': 'generateRoutes',
            'click .js-save-route': 'saveRoute',
            'keyup .js-truck-count': 'updateTruckCount',
            'change .js-agent-name': 'updateAgentName',
            'change .js-optimize-by': 'updateOptimizeBy',
            'click .js-datepicker-popout': 'updateDate',
            'click .js-expand-row': 'expandRow',
            'change .js-truck-id': 'updateTruckId',
            'change .js-driver-id': 'updateDriverId'
        },
        /**
         * handles click of generate routes button
         * calls model's generate routes function
         */
        generateRoutes: function (e) {
            e.preventDefault();
            this.model.generateRoutes();
        },
        /**
         * handles click of save route button
         * calls model's save route function
         */
        saveRoute: function (e) {
            e.preventDefault();
            this.model.saveRoute();
        },
        /**
         * sets truck count to user's input
         * if 0 entered, sets truck_count_0 to true to display error message
         * if something other than a number is added, display invalid truck count error
         */
        updateTruckCount: function (e) {
            var truckCount =  e.currentTarget.value;
            // if user deleted their input, go back to default
            if (truckCount === ''){
                truckCount = this.model.get('truck_count_default');
            }
            // check that truck count is a valid number
            var re = new RegExp('^[0-9]+$');
            if (re.test(truckCount)) {
                this.model.set('truck_count', truckCount);
                this.model.set('truck_count_invalid', false);
            } else {
                this.model.set('truck_count_invalid', true);
            }

            if (truckCount === '0') {
                this.model.set('truck_count_0', true);
            } else {
                this.model.set('truck_count_0', false);
            }
        },
        /**
         * sets agent's name to user's input
         */
        updateAgentName: function (e) {
            this.model.set('agent_name', e.currentTarget.value);
        },
        /**
         * sets optimize by to time or distance based on user input
         */
        updateOptimizeBy: function (e) {
            this.model.set('optimize_by', e.currentTarget.value);
        },
        /**
         * triggers model's update date if user changed date in datepicker
         */
        updateDate: function () {
            this.model.updateDate();
        },
        /**
         * adds user's selection of truck ID to the array of truck IDs
         */
        updateTruckId: function (e) {
            var id = e.currentTarget.value;
            var trucks = this.model.get('truck_ids');
            trucks.push(id);
            this.model.set('truck_ids', trucks);
        },
        /**
         * adds user's selection of driver ID to the array of driver IDs
         */
        updateDriverId: function (e) {
            var id = e.currentTarget.value;
            var drivers = this.model.get('driver_ids');
            drivers.push(id);
            this.model.set('driver_ids',drivers);
        },
        /**
         * make rows collapsible
         */
        expandRow: function () {
            var parentRow = $(this).parent('tr');
            var detailsRow = this.$el.find('.js-detail-row');
            if (detailsRow.hasClass('hidden')) {
                detailsRow.removeClass('hidden');
                parentRow.removeClass('table_row_collapsed').addClass('table_row_expanded');
            } else {
                parentRow.removeClass('table_row_expanded').addClass('table_row_collapsed');
                detailsRow.addClass('hidden');
            }
        }
    }, {
        debugName: 'RoutePlannerView'
    });
    return RoutePlannerView;
});