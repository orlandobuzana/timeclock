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


    // $("#from-job").datepicker({
    //     'autoclose': true
    //     ,'orientation': 'top'
    //     ,'endDate': new Date()
    //     ,'format': 'yyyy-mm-dd'
    //     ,'pickTime': false
    // })
    // .on('changeDate', function(ev) {
    //     $('#to-job').datepicker('setStartDate', ev.date);    
    // });

    // $("#to-job").datepicker({
    //     'autoclose': true
    //     ,'orientation': 'top'
    //     ,'endDate': new Date()
    //     ,'format': 'yyyy-mm-dd'
    //     ,'pickTime': false
    // })
    // .on('changeDate', function(ev) {
    //     $('#from-job').datepicker('setEndDate', ev.date);    
    // });
});
