$(function() {
	"use strict";

	var Shift = function(vars) {
		var __this = this;	
		var shiftUrl = "/timeclock/shifts/";

		this.id = ko.observable();
		this.time_in = ko.observable();
		this.time_out = ko.observable();
		this.hours = ko.observable();
		this.employee = ko.observable();

		this.updating = ko.observable(false);
		this.shiftToEdit = ko.observable();	

		this.init = function(vars) {
			vars = vars || {};

			this.rebuild(vars);
		}.bind(this);

		this.rebuild = function(vars) {
			vars = vars || {};

			if (vars.hasOwnProperty('id'))
				this.id(vars.id);
			if (vars.hasOwnProperty('time_in'))
				this.time_in(vars.time_in);
			if (vars.hasOwnProperty('time_out'))
				this.time_out(vars.time_out);
			if (vars.hasOwnProperty('hours'))
				this.hours(vars.hours);
			if (vars.hasOwnProperty('employee'))
				this.employee(vars.employee);

		}.bind(this);

		this.summary = function() {
			window.location = "/timeclock/summary/" + this.id();
		}.bind(this);

		this.editShift = function() {
			var data = this.toDict();
			var editShift = new Shift(data);
			this.shiftToEdit(editShift);		

			this.updating(true);
		}.bind(this);

		this.cancelEdit = function() {
			this.updating(false);
		}.bind(this);

		this.bindInputs = function(e) {
			var timeInInput = $(e).find('.time-in-input');
			var timeOutInput = $(e).find('.time-out-input');

			$(timeInInput).datetimepicker({
				 format: 'mm/dd/yyyy hh:ii:ss'
				,autoclose: true
				,todayHighlight: true
				,endDate: $(timeOutInput).val()
			})
		    .on('changeDate', function(ev) {
		        $(timeOutInput).datetimepicker('setStartDate', $(ev.target).val());
		    });

			$(timeOutInput).datetimepicker({
				 format: 'mm/dd/yyyy hh:ii:ss'
				,autoclose: true
				,todayHighlight: true
				,startDate: $(timeInInput).val()
			})
		    .on('changeDate', function(ev) {
		        $(timeInInput).datetimepicker('setEndDate', $(ev.target).val());
		    });

		}.bind(this)

		this.update = function() {
			var url = shiftUrl;
			var requestType = "POST";
			var data = this.shiftToEdit().toDict();
			var csrf = $('input[name="csrfmiddlewaretoken"]').val();

			if(data.id) {
				url += data.id + "/";
				requestType = "PUT";
			}

			return $.ajax({
				 url: url
                ,dataType: 'json'
                ,type: requestType
                ,beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                }
                ,data: JSON.stringify(data)
			})
			.done(function() {
				$(window).trigger('shift-updated');
			})
			.fail(function(resp) {
		        alert(resp.responseText);
			});
		}.bind(this);

		this.deleteWarning = function() {
			$('#delete-warning #delete-shift-btn').off('click').on('click', function() {
				__this.deleteShift();
				$('#delete-warning').modal('hide');
			});
			$('#delete-warning').modal()
		}.bind(this);

		this.deleteShift = function() {
			if (!this.id())
				return $.Deferred().reject().promise();

			var url = shiftUrl + this.id() + "/";
			var requestType = "DELETE";
			var csrf = $('input[name="csrfmiddlewaretoken"]').val();

			return $.ajax({
				 url: url
                ,dataType: 'json'
                ,type: requestType
                ,beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrf);
                }
			})
			.done(function() {
				$(window).trigger('shift-updated');
			})
			.fail(function(resp) {
		        alert(resp.responseText);
			});
		}.bind(this);

		this.toDict = function() {
			return {
				 'id':       this.id()
				,'time_in':  this.time_in()
				,'time_out': this.time_out()
				,'hours':    this.hours()
				,'employee': this.employee()
			}
		}.bind(this);

		this.init(vars);
	}

	$.fn.Shift = Shift;
})