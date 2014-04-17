function showBugReportForm() {
	$("#bug_report_form").css("display", "table");
	$("#bug_report_div").show();
}

function cancelSubReport() {
	document.getElementById("bug_report_form").reset();
	$("#bug_report_div").hide();
}

function erase_bug_report_div() {
	$("#bug_report_div").hide();
	document.getElementById("bug_report_form").reset();
}
