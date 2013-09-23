count = 0;
spinner = new Throbber({
	color : 'black',
	size : 90
});

function createTable(cells) {
	var table = null;

	if (last_answer != undefined) {
		table = last_answer.table; // first task_run we don't have last_answer
	}

	jQuery(function() {

		if (table != undefined && table != "NoTable") {
			jQuery('#jQuerySheet').sheet({
				buildSheet : jQuery.sheet.makeTable.json(table, true),
				calcOff : true,
				menu : " ",
				lockFormulas : true,
				resizable : false,
				boxModelCorrection : 2,
				cellSelectModel : 'excel',
				newColumnWidth : 130,
				colMargin : 38,
				autoFiller : false,
				minSize : {
					rows : 6,
					cols : 4
				},
				forceColWidthsOnStartup : false
			});

		} else {

			
			jQuery('#jQuerySheet').sheet({
				buildSheet : '4x6',
				calcOff : true,
				resizable : false,
				menu : " ",
				lockFormulas : true,
				boxModelCorrection : 2,
				cellSelectModel : 'excel',
				newColumnWidth : 130,
				colMargin : 38,
				autoFiller : false,
				minSize : {
					rows : 6,
					cols : 4
				},
				forceColWidthsOnStartup : false

			});

		}

	});

}

function quitEdition() {
	jQuery.sheet.instance[count].evt.cellEditDone(); // Event to finish edit
	jQuery.sheet.instance[count].evt.cellEditAbandon(); // Event to exit
														// celledit
}

function viewer(path) {
	$("#viewer-container").iviewer({

		src : path,
		update_on_resize : false,
		zoom_animation : false,
		mousewheel : true,
		zoom_max : 250,
		zoom_min : 100,
		initCallback : function() {
			var object = this;
			$("#in").click(function() {
				object.zoom_by(1);
			});
			$("#out").click(function() {
				object.zoom_by(-1);
			});
			$("#fit").click(function() {
				object.fit();
			});
			$("#orig").click(function() {
				object.set_zoom(100);
			});
			$("#update").click(function() {
				object.update_container_info();
			});
		},
		onMouseMove : function(ev, coords) {
		},
		onStartDrag : function(ev, coords) {
			return true;
		}, // this image will not be dragged
		onDrag : function(ev, coords) {
		},
		onStartLoad : function() {
			$("#throbber").show();
			spinner.start();
		},
		onFinishLoad : function() {
			spinner.stop();
			$("#throbber").hide();
		}
	});

	$("#viewer-container").iviewer('loadImage', path);
	$("#viewer-container").iviewer('update_container_info');

}

function submitTask(complete, answer) {

	// Get the task-id
	var taskid = $("#task-id").text();
	var table = answer;

	if (answer != 'NoTable') {

		// Quit Table Edition
		quitEdition();
		table = JSON.stringify(jQuery.sheet.instance[count].exportSheet.json());
		jQuery.sheet.instance[count].kill();
		count++;

	}

	answer = {
		"complete" : complete,
		"table" : table
	};

	// Save the task
	submit(answer, taskid);

}

function submit(answer, taskid) {
	pybossa.saveTask(taskid, answer).done(function(data) {
		// Uncoment next line for debugging purposes
		// FadeIn & Out the success div feedback
		$("#success").fadeIn();
		setTimeout(function() {
			$("#success").fadeOut();
		}, 1000);
		// Load a new task
		pybossa.newTask("tt-transcribe").done(function(data) {
			loadData(data);
		});
	});
}
