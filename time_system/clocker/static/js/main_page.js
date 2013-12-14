$(function() {
    $('#statusBtn').button().click(function() {
        console.log('submitting form');
        console.log($(this).parent('form.clocker-form'));
        $(this).closest('form.clocker-form').submit();
    });


    $("#from").datetimepicker({
         autoclose:   true
        ,format:      'mm/dd/yyyy'
        ,minView:     2
    })
    .on('changeDate', function(ev) {
        $('#to').datetimepicker('setStartDate', $(ev.target).val());
    });

    $("#to").datetimepicker({
         autoclose:   true
        ,format:      'mm/dd/yyyy'
        ,minView:     2
    })
    .on('changeDate', function(ev) {
        $('#from').datetimepicker('setEndDate', $(ev.target).val());
    });


    var fromJob = $("#from-job");
    var toJob = $("#to-job");

    $(fromJob).datetimepicker({
         autoclose:   true
        ,format:      'mm/dd/yyyy'
        ,minView:     2
        ,endDate:     $(fromJob).val()
    })
    .on('changeDate', function(ev) {
        $('#to-job').datetimepicker('setStartDate', $(ev.target).val());
    });

    $(toJob).datetimepicker({
         autoclose:   true
        ,format:      'mm/dd/yyyy'
        ,minView:     2
        ,startDate:   $(fromJob).val()
    })
    .on('changeDate', function(ev) {
        $('#from-job').datetimepicker('setEndDate', $(ev.target).val());
    });
});
