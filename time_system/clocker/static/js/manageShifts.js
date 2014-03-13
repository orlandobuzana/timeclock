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
				$.bbq.pushState({'emp': employee.id}, '', 0);
			})


			//TODO: this will change once I get more time to do something more proper
			$(window).on('shift-updated', function() {
				__this.shiftList().reload(__this.shiftList().currentPage(), __this.selectedEmployee().id);
			});

			$(window).on('hashchange', hashchangeHandler);
			return loadEmployees().then(function() {
				$(window).trigger('hashchange');
			});
			//setInputBindings();
		}

		var hashchangeHandler = function(e) {
			var frags = $.deparam(e.fragment, true);
			console.log(frags);
			if (frags.hasOwnProperty('emp')) {
				var empId = frags.emp;
				$.each(__this.employees(), function(i, emp) {
					if (empId === emp.id) {
						__this.selectedEmployee(emp);
						return false;
					}
				})
			}
		}.bind(this);

		//Checks if the shift table should add a blank row to seperate groups of shifts by day
		this.shouldAddSeperator = function(index, nextIndex) {

			if (index >= this.shiftList().shifts().length || nextIndex >= this.shiftList().shifts().length)
				return false;
			
			var currentDate = new Date(this.shiftList().shifts()[index].time_in());
			var nextDate = new Date(this.shiftList().shifts()[nextIndex].time_in());

			if (currentDate.getDate() !== nextDate.getDate())
				return true;

			return false;
		}.bind(this)



		function loadEmployees() {
			return $.get(employeeUrl, function(resp) {
				$.each(resp.employees, function(i, emp) {
					__this.employees.push(emp);	
					// if (emp.id === __this.managingEmployee().id)
					// 	__this.selectedEmployee(emp);
				});
			});
		};

		function setInputBindings() {
			$('input.icon-input').on('input', function() {
				var currentVal = $(this).val();
				if (currentVal === "" && !$(this).is(':focus'))
					$(this).removeClass('icon-input-hide');	
				else
					$(this).addClass('icon-input-hide');	
			})
			.focus(function() { $(this).addClass('icon-input-hide'); })
			.focusout(function() { 
				if ($(this).val() === "")
					$(this).removeClass('icon-input-hide'); 
			}).trigger('input');

			$('.date-input').bootstrapDP({
		         'autoclose': true
		        ,'orientation': 'top'
		        ,'format': 'yyyy-mm-dd'
			}).on('hide', function(e) {
				$(e.target).trigger('input');
			});

			$('.time-input').timepicker({
				 'showMeridian': false	
				,'showSeconds': true
				,'defaultTime': false
				,'minuteStep': 1
			})
			.on("show.timepicker", function(e){
				$(e.target).val(e.time.value);
			})
			.on("changeTime.timepicker", function(e) {
				if (e.time.value === "")
					$(e.target).val("0:00:00");
				else
					$(e.target).val(e.time.value);
			}).val("");
		}
	}	

	$.fn.ManageShifts = ManageShifts;
});