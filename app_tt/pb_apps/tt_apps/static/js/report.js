function showBugReportForm() {
	
	if ($("#button_bug_report").hasClass("active")) {
		$("#button_bug_report").removeClass("active");
		cancelSubReport();
	} else {
		$("#bug_report_form").css("display", "table");
		$("#bug_report_div").show();
		$("#button_bug_report").addClass("active");
	}
}

function cancelSubReport() {
	document.getElementById("bug_report_form").reset();
	$("#bug_report_div").hide();
}

function erase_bug_report_div() {
	$("#bug_report_div").hide();
	document.getElementById("bug_report_form").reset();
}
