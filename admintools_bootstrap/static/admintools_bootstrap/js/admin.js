$(function(){
	$('select:not([name="action"])').chosen({
		disable_search_threshold: 10,
		width: "97%",
		height: "34px"
	});

    $('select[name="action"]').chosen({
		disable_search_threshold: 10
	});

	$(".form_datetime").datetimepicker({
        format: "dd M yyyy",
        linkField: "id_submit_date_1",
        linkFormat: "hh:ii",
		pickerPosition: "bottom-right",
		autoclose: true,
        todayBtn: true
    });
});