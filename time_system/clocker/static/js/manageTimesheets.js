$(function() {
    "use strict";

    var Timesheets = $.fn.Timesheets;

    var ManageTimesheets = function(vars) {

        var timesheets = new Timesheets();
            
        this.timesheetList = ko.computed(function() {
            return timesheets.timesheetList() ? timesheets.timesheetList : [];
        }, this);

        var init = function(vars) {
            vars = vars || {};

            timesheets.refresh();
        }.bind(this);

        init(vars);
    };

    $.fn.ManageTimesheets = ManageTimesheets;
});