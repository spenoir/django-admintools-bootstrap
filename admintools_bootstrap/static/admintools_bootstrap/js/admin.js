$(function(){
		$('div:not(.action-wrapper) select').chosen({
		disable_search_threshold: 10,
		width: "97%",
		height: "34px"
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