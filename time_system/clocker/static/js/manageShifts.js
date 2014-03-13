$(function() {
	"use strict";

	var ManageShifts = function(vars) {
		var __this = this;
		var ShiftList = $.fn.ShiftList;
		var employeeUrl = "/timeclock/employees/";

		this.shiftList = ko.observable();
		this.employees = ko.observableArray();
		this.selectedEmployee = ko.observable();
		this.managingEmployee = ko.observable();

		this.managingSelf = ko.computed(function() {
			var selectedEmp = this.selectedEmployee();
			var managingEmp = this.managingEmployee();
			var managing = false;

			if (selectedEmp && managingEmp && selectedEmp.id == managingEmp.id)		
				managing = true;

			return managing;
		}.bind(this));

		this.init = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('managingEmployee'))
				this.managingEmployee(vars.managingEmployee);

			var startingPage = 1;
			var shiftListData = {
				'per_page': 25
			};

			this.shiftList(new ShiftList(shiftListData));
			this.selectedEmployee.subscribe(function(employee) {
				__this.shiftList().reload(startingPage, employee.id);
			})

			loadEmployees();

			//TODO: this will change once I get more time to do something more proper
			$(window).on('shift-updated', function() {
				__this.shiftList().reload(__this.shiftList().currentPage(), __this.selectedEmployee().id);
			});

			//setInputBindings();
		}

		//Checks if the shift table should add a blank row to seperate groups of shifts by day
		this.shouldAddSeperator = function(index, nextIndex) {

			if (index >= this.shiftList().shifts().length || nextIndex >= this.shiftList().shifts().length)
				return false;
			
			var currentDate = new Date(this.shiftList().shifts()[index].time_in());
			var nextDate = new Date(this.shiftList().shifts()[nextIndex].time_in());

			if (currentDate.getDate() !== nextDate.getDate()) {
				console.log('true');
				return true;
			}

			return false;
		}.bind(this)



		function loadEmployees() {
			$.get(employeeUrl, function(resp) {
				$.each(resp.employees, function(i, emp) {
					__this.employees.push(emp);	
					if (emp.id === __this.managingEmployee().id)
						__this.selectedEmployee(emp);
				});
			});
		};

		this.init(vars);
	}	

	$.fn.ManageShifts = ManageShifts;
});