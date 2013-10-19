$(function(){
	$('select').chosen({
		disable_search_threshold: 10
	});
	$(".datetime").datetimepicker({
        format: "dd MM yyyy - hh:ii",
        linkField: "mirror_field",
        linkFormat: "yyyy-mm-dd hh:ii"
    });
});