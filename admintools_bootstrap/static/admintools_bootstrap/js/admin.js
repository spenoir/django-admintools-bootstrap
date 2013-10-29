$(function(){
	$('select').chosen({
		disable_search_threshold: 10,
		width: "100%",
		height: "34px"
	});

	$(".form_datetime").datetimepicker({
        format: "dd MM yyyy",
        linkField: "id_submit_date_1",
        linkFormat: "hh:ii",
		pickerPosition: "bottom-left",
		autoclose: true,
        todayBtn: true
    });
});