function showBugReportForm() {
	$("#bug_report_form").css("display", "table");
	$("#bug_report_div").show();
}

function cancelSubmitReport() {
	$("#bug_report_div").hide();
	$("#bug_report_form").css("display", "none");
}