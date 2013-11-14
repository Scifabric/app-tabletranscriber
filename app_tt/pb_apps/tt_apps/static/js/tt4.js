	$('body').on('contextmenu', '#canvas-table-container', function(e) {
		return false;
	});

	$('body').on('contextmenu', '#canvas-cell-container', function(e) {
		return false;
	});

	var DEFAULT_ZOOM_DELTA = 0.5;
	var MAX_TABLE_VIEWER_WIDTH = 515;
	var MAX_TABLE_VIEWER_HEIGHT = 600;

	var MAX_CELL_VIEWER_WIDTH = 400;
	var MAX_CELL_VIEWER_HEIGHT = 150;

	var MAX_X = Number.MAX_VALUE;
	var MAX_Y = Number.MAX_VALUE;
	var MIN_X = 0;
	var MIN_Y = 0;

	var tableViewerStage;
	var cellViewerStage;

	var unfixedLayer;
	var selectionLayer;
	var fixedLayer;
	var imageLayer;
	var img_url;
	var origTableStageMaxX;
	var origTableStageMaxY;

	var cells;
	var cellsIterator;

	var segWidth;
	var unfixedColor;
	var highlightColor;

	var shiftOnCanvas;
	var isEditing;

	function initVariables() {
		cells = new Array();
		cellsIterator = new CellsIterator(cells);
		isEditing = false;

		shiftOnCanvas = 1.2;
		segWidth = 2.2;
		unfixedColor = "#E93F2D";
		fixedColor = "#1BA038";
		highlightColor = "#339ACD";
	}

	// Cell class definition
	function Cell(computerTranscription, humanTranscription, lastAnswer, confidence, numOfConfirmations, enableEdit) {
		this.segments = new Array();
		this.computerTranscription = computerTranscription;
		this.humanTranscription = humanTranscription;
		this.lastAnswer = lastAnswer;
		this.confidence = confidence;
		this.fixed = !enableEdit ? true : false;
		this.enableEdit = enableEdit;
		this.rect = undefined;
		this.numberOfConfirmations = numOfConfirmations;
	}

	Cell.prototype.getNumberOfConfirmations = function() {
		return this.numberOfConfirmations;
	}

	Cell.prototype.setNumberOfConfirmations = function(newVal) {
		this.numberOfConfirmations = newVal;
	}

	Cell.prototype.increaseNumberOfConfirmation = function() {
		this.numberOfConfirmations++;
	}

	Cell.prototype.isEditEnabled = function() {
		return this.enableEdit;
	}

	Cell.prototype.isFixed = function() {
		return this.fixed;
	}

	Cell.prototype.setFixed = function(fixed) {
		this.fixed = fixed;
	}

	Cell.prototype.getConfidence = function() {
		return this.confidence;
	}

	Cell.prototype.getLastAnswer = function() {
		return this.lastAnswer;
	}

	Cell.prototype.getHumanTranscription = function() {
		return this.humanTranscription;
	};

	Cell.prototype.setHumanTranscription = function(newTranscription) {
		this.humanTranscription = newTranscription;
	};

	Cell.prototype.getComputerTranscription = function() {
		return this.computerTranscription;
	};

	Cell.prototype.setComputerTranscription = function(newTranscription) {
		this.computerTranscription = newTranscription;
	};

	Cell.prototype.addSegment = function(segment) {
		this.segments.push(segment);
	};

	Cell.prototype.getSegments = function() {
		return this.segments;
	};

	Cell.prototype.getSegmentAtPosition = function(posSeg) {
		for (var i = 0; i < this.segments.length; i++) {
			var segment = this.segments[i];
			if (segment.equalsSegmentPosition(posSeg)) {
				return segment;
			}
		}
		return undefined;
	};

	Cell.prototype.setStroke = function(color) {
		for (var i = 0; i < this.segments.length; i++) {
			this.segments[i].setStroke(color);
		}
	};

	Cell.prototype.getBorders = function() {
		var minX = MAX_X;
		var minY = MAX_Y;
		var maxX = MIN_X;
		var maxY = MIN_Y;

		for (var i = 0; i < this.segments.length; i++) {
			var segment = this.segments[i].getPoints();
			
			if (segment[0].x < minX) minX = segment[0].x;
			if (segment[0].y < minY) minY = segment[0].y;
			if (segment[1].x > maxX) maxX = segment[1].x;
			if (segment[1].y > maxY) maxY = segment[1].y;
		}

		return [minX, minY, maxX, maxY];
	};

	Cell.prototype.getWidth = function() {
		var cellBorders = this.getBorders();
		return cellBorders[2] - cellBorders[0];
	};

	Cell.prototype.getHeight = function() {
		var cellBorders = this.getBorders();
		return cellBorders[3] - cellBorders[1];
	};

	Cell.prototype.isPosInCell = function(posX, posY, scale) {
		var borders = this.getBorders();
		var minX = borders[0] * scale.x;
		var minY = borders[1] * scale.x;
		var maxX = borders[2] * scale.y;
		var maxY = borders[3] * scale.y;
		
		return (posX >= minX && posX <= maxX) && (posY >= minY && posY <= maxY);
	};

	Cell.prototype.createRectangle = function() {
		var borders = this.getBorders();
		var isFixed = this.isFixed();
		this.rect = new Kinetic.Rect({
					x: borders[0],
					y: borders[1],
					width: borders[2] - borders[0],
					height: borders[3] - borders[1],
					fillEnabled: true,
					fill: isFixed? fixedColor:unfixedColor,
					opacity: 0.25
				});
		return this.rect;	
	}

	Cell.prototype.setRectangleOpacity = function(value) {
		this.rect.setOpacity(value);
	}

	function CellsIterator(cells) {
		this.cells = cells;
		this.actualIndex = -1;
		this.previousIndex = -1;
	}

	CellsIterator.prototype.haveCellsToFix = function() {
		for (var i = 0; i < this.cells.length; i++) {
			if (!this.cells[i].isFixed()) return true;
		}
		return false;
	}

	CellsIterator.prototype.getNextIndex = function(actualIndex) {
		return actualIndex + 1 < this.cells.length ? actualIndex + 1 : 0;
	}

	CellsIterator.prototype.getPreviousIndex = function(actualIndex) {
		return actualIndex - 1 >= 0 ? actualIndex - 1 : (this.cells.length - 1);
	}

	CellsIterator.prototype.getPreviousCell = function() {
		return this.cells[this.previousIndex];
	}

	CellsIterator.prototype.next = function() {
		var computedNextIndex = this.getNextIndex(this.actualIndex);
		var loopSafe = 0;

		while (computedNextIndex != this.actualIndex) {

			if (!this.cells[computedNextIndex].isFixed()
				 || loopSafe > (cells.length-1)) break;

			computedNextIndex = this.getNextIndex(computedNextIndex);
			loopSafe++;
		}

		this.previousIndex = this.actualIndex;
		this.actualIndex = computedNextIndex;
		return this.actual();
	};

	CellsIterator.prototype.previous = function() {
		var computedPreviousIndex = this.getPreviousIndex(this.actualIndex);
		var loopSafe = 0;

		while (computedPreviousIndex != this.actualIndex) {

			if (!this.cells[computedPreviousIndex].isFixed()
				|| loopSafe > (cells.length-1)) break;

			computedPreviousIndex = this.getPreviousIndex(computedPreviousIndex);
		}

		this.previousIndex = this.actualIndex;
		this.actualIndex = computedPreviousIndex;
		return this.actual();
	};

	CellsIterator.prototype.actual = function() {
		return this.cells[this.actualIndex];
	};

	CellsIterator.prototype.updateActualIndex = function(newIndex) {
		this.previousIndex = this.actualIndex;
		this.actualIndex = newIndex;
	};

	Kinetic.Line.prototype.equalsSegmentPosition = function(segPos) {
		var points = this.getPoints();
		return points[0].x == segPos[0].x && points[0].y == segPos[0].y && 
			points[1].x == segPos[1].x && points[1].y == segPos[1].y;
	};

	function zoomCanvas(isZoomIn, zoomDelta) {
		var actualScale = tableViewerStage.getScale();

		var newScaleX = isZoomIn ?
			actualScale.x + zoomDelta : actualScale.x - zoomDelta;
		var newScaleY = isZoomIn ?
				actualScale.y + zoomDelta : actualScale.y - zoomDelta;

		if (newScaleX <= 0 || newScaleY <= 0) return;

		reScaleStage(tableViewerStage, newScaleX);
	}

	function reScaleStage(stage, scale) {
		var newCanvasWidth = origTableStageMaxX * scale;
		var newCanvasHeight = origTableStageMaxY * scale;

		stage.setScale(scale);
		stage.setWidth(newCanvasWidth);
		stage.setHeight(newCanvasHeight);
		stage.draw();
	}

	function handleZoomOutToolEvent() {
		var isZoomIn = false;
		zoomCanvas(isZoomIn, DEFAULT_ZOOM_DELTA);
		focusCell(cellsIterator.actual(), true);
	}

	function handleZoomInToolEvent() {
		var isZoomIn = true;
		zoomCanvas(isZoomIn, DEFAULT_ZOOM_DELTA);
		focusCell(cellsIterator.actual(), true);
	}

	function createTableViewer(taskInfo, minTableViewerWidth, minTableViewerHeight) {
		initVariables();

		img_url = taskInfo.link;

		var tableMaxX = taskInfo.maxX;
		var tableMaxY = taskInfo.maxY;
		origTableStageMaxX = tableMaxX + (2 * shiftOnCanvas);
		origTableStageMaxY = tableMaxY + (2 * shiftOnCanvas);
		
		var tableViewerWidth = origTableStageMaxX < minTableViewerWidth?
				 minTableViewerWidth: origTableStageMaxX;
		var tableViewerHeight = origTableStageMaxY < minTableViewerHeight?
				 minTableViewerHeight: origTableStageMaxY;
		
		tableViewerStage = new Kinetic.Stage({
			container : 'canvas-table-container',
			width : tableViewerWidth,
			height : tableViewerHeight,
			scale : 1
		});

		cellViewerStage = new Kinetic.Stage({
			container : 'canvas-cell-container',
			width : origTableStageMaxX,
			height : origTableStageMaxY,
			scale : 1
		});

		tableViewerStage.on('click', function(evt) {
			handleMouseClickEvent(evt);     
		});

		unfixedLayer = new Kinetic.Layer();
		selectionLayer = new Kinetic.Layer();
		fixedLayer = new Kinetic.Layer();
		imageLayer = new Kinetic.Layer();

		var imageObj = new Image();
		imageObj.src = taskInfo.img_url;

		imageObj.onload = function() {
			configureTableViewer(imageObj, tableMaxX, tableMaxY);
			loadGrid(taskInfo);
		};
	}
	
	function configureTableViewer(imageObj, tableMaxX, tableMaxY) {
		var table = new Kinetic.Image({
			x : shiftOnCanvas,
			y : shiftOnCanvas,
			image : imageObj,
			width : tableMaxX,
			height : tableMaxY
		});

		imageLayer.add(table);
		table.moveToBottom();

		tableViewerStage.add(imageLayer);
		tableViewerStage.add(unfixedLayer);
		tableViewerStage.add(fixedLayer);
		fixedLayer.moveToTop();
		tableViewerStage.add(selectionLayer);

		var tableStagePad = 15;
		var stageWidth = tableViewerStage.getWidth() + tableStagePad;
		var stageHeight = tableViewerStage.getHeight() + tableStagePad;
		var tableViewerWidth = stageWidth > MAX_TABLE_VIEWER_WIDTH ?
			 MAX_TABLE_VIEWER_WIDTH : stageWidth;
		var talbeViewerHeight = stageHeight > MAX_TABLE_VIEWER_HEIGHT ?
			 MAX_TABLE_VIEWER_HEIGHT : stageHeight;
		$("#table-viewer").width(tableViewerWidth);
		$("#table-viewer").height(talbeViewerHeight);
	}

	function updateCellViewerStage(cell) {
		cellViewerStage.destroyChildren();
		cellViewerStage.add(imageLayer.clone());

		var cellWidth = cell.getWidth();
		var cellHeight = cell.getHeight();

		var scale = getSuitableScale(cellWidth, cellHeight);

		var scaledCellWidth = cellWidth * scale;
		var scaledCellHeight = cellHeight * scale;

		reScaleStage(cellViewerStage, scale);

		var cellViewerWidth = scaledCellWidth > MAX_CELL_VIEWER_WIDTH ?
			 MAX_CELL_VIEWER_WIDTH : scaledCellWidth;
		var cellViewerHeight = scaledCellHeight > MAX_CELL_VIEWER_HEIGHT ?
			 MAX_CELL_VIEWER_HEIGHT : scaledCellHeight;

		$("#cell-viewer").width(cellViewerWidth);
		$("#cell-viewer").height(cellViewerHeight);
		$("#canvas-cell-container").width(cellViewerWidth);
		$("#canvas-cell-container").height(cellViewerHeight);
		focusCell(cell, false);
	}

	function getSuitableScale(cellWidth, cellHeight) {
		var scale = 1;

		var scaledWidth = cellWidth;
		var scaledHeight = cellHeight;
		var isZoomIn = cellWidth < MAX_CELL_VIEWER_WIDTH &&
				 cellHeight < MAX_CELL_VIEWER_HEIGHT;

		if (isZoomIn) {
			while (scaledWidth < MAX_CELL_VIEWER_WIDTH &&
					scaledHeight < MAX_CELL_VIEWER_HEIGHT) {
				scale += 0.1;
				scaledWidth = cellWidth * scale;
				scaledHeight = cellHeight * scale;
			}
		} else {
			while (scaledWidth > MAX_CELL_VIEWER_WIDTH ||
					scaledHeight > MAX_CELL_VIEWER_HEIGHT) {
				scale -= 0.1;
				scaledWidth = cellWidth * scale;
				scaledHeight = cellHeight * scale;
			}
		}
		return scale > 5 ? 5: scale;
	}

	function loadGrid(taskInfo) {

		var isLastAnswer = typeof taskInfo.last_answer != "undefined";
		var taskInfoCells = isLastAnswer ? $.parseJSON(taskInfo.last_answer).cells : taskInfo.cells;
		var computerValues = isLastAnswer ? $.parseJSON(taskInfo.last_answer).computer_values : taskInfo.values;
		var humanValues = isLastAnswer ? $.parseJSON(taskInfo.last_answer).human_values : undefined;
		var confidences = isLastAnswer ? $.parseJSON(taskInfo.last_answer).confidences : taskInfo.confidences;
		var numberOfConfirmations = isLastAnswer ? $.parseJSON(taskInfo.last_answer).num_of_confirmations : undefined;

		for (var i = 0; i < taskInfoCells.length; i++) {
			
			var arr = taskInfoCells[i];

			var leftX = arr[0] + shiftOnCanvas;
			var upperY = arr[1] + shiftOnCanvas;
			var rightX = arr[2] + shiftOnCanvas;
			var bottomY = arr[3] + shiftOnCanvas;

			var cellLines = new Array();
			cellLines.push([{'x': leftX, 'y': upperY}, {'x': rightX, 'y': upperY}]);
			cellLines.push([{'x': leftX, 'y': upperY}, {'x': leftX, 'y': bottomY}]);
			cellLines.push([{'x': leftX, 'y': bottomY}, {'x': rightX, 'y': bottomY}]);
			cellLines.push([{'x': rightX, 'y': upperY}, {'x': rightX, 'y': bottomY}]);

			var lastAnswer = isLastAnswer ? humanValues[i] : undefined;
			var numConfirmations = isLastAnswer ? numberOfConfirmations[i] : 0;
			var enableEdit = numConfirmations < 2;

			var cell = createCell(cellLines, computerValues[i], lastAnswer, confidences[i], numConfirmations, enableEdit);
			cells.push(cell);
		}

		createUnfixedLayer();
		createFixedLayer();
		redrawLinesLayer();

		selectCell(cellsIterator.next());
		updateTaskbarProgress();
	}

	function createUnfixedLayer() {
		createLinesLayer(false);
	}

	function createFixedLayer() {
		createLinesLayer(true);
	}

	function createLinesLayer(isFixedLayer) {
		for (var i = 0; i < cells.length; i++) {
			var cell = cells[i];
			addCellSegmentsToLayer(isFixedLayer, cell);
		}
	}

	function redrawLinesLayer() {
		fixedLayer.draw();
		unfixedLayer.draw();
	}

	function addCellSegmentsToLayer(isFixedLayer, cell) {

		if (isFixedLayer && !cell.isFixed() || !isFixedLayer && cell.isFixed()) return;

		var layer = isFixedLayer ? fixedLayer : unfixedLayer;
		var cellSegs = cell.getSegments();

		for (var i = 0; i < cellSegs.length; i++) {
			var seg = isFixedLayer?
				 createSegment(cellSegs[i].getPoints()) : cellSegs[i];

			var segColor = isFixedLayer? fixedColor : unfixedColor;
			seg.setStroke(segColor);

			if (!isSegInArray(seg, layer.getChildren())) {
				layer.add(seg);
			}
		}

		var cellRect = cell.createRectangle();
		layer.add(cellRect);
	}

	function isSegInArray(seg, arr) {
		var segPoints = seg.getPoints();
		for (var i = 0; i < arr.length; i++) {
			var otherSeg = arr[i];
			if (otherSeg.getClassName() == "Line" && otherSeg.equalsSegmentPosition(segPoints)) {
				return true;
			}
		}
		return false;
	}

	function createCell(cellLines, computerTranscription, humanTranscription, confidence, numOfConfirmations, enableEdit) {
		var cell;

		if (typeof humanTranscription != "undefined") {
			cell = new Cell(computerTranscription, humanTranscription, humanTranscription,
				 confidence, numOfConfirmations, enableEdit);
		} else {
			cell = new Cell(computerTranscription, undefined, undefined,
				 confidence, numOfConfirmations, enableEdit);
		}

		for (var i = 0; i < cellLines.length; i++) {
			var segment = findSegment(cellLines[i]);

			if (typeof segment == "undefined") {
				segment = createSegment(cellLines[i]);
			}
			cell.addSegment(segment);
		}
		return cell;
	}

	function createSegment(posLine) {
		var kineticLine = new Kinetic.Line({
			points : posLine,
			stroke : unfixedColor,
			strokeWidth : segWidth,
			draggable: false,
		});
		return kineticLine;
	}

	function findSegment(posSeg) {
		for (var i = 0; i < cells.length; i++) {
			var segment = cells[i].getSegmentAtPosition(posSeg);
			if (typeof segment != "undefined") {
				return segment;
			}
		}
		return undefined;
	}

	// Event Handling
	document.onkeydown = function (evt) { 
		if (typeof evt.keyCode == "undefined") return;

		if (evt.keyCode == 13) {
			handleSaveCellEvent();
			return;
		}

		if ($("#edition-field").is(":focus") &&
				(evt.keyCode == 35 || evt.keyCode == 36 || evt.keyCode == 38 || evt.keyCode == 40)) {
			isEditing = true;
		}

		if (isEditing) return;

		if (evt.keyCode == 37) {
			handlePreviousCellEvent();
			evt.preventDefault();
		} else if (evt.keyCode == 39) {
			handleNextCellEvent();
			evt.preventDefault();
		}
	};

	$("#edition-field").on("click", function() {
		isEditing = true;	
	});

	$("#edition-field").on("input", function() {
		isEditing = true;	
	});

	$("#edition-field").on("blur", function() {
		isEditing = false;	
	});

	function handlePreviousCellEvent() {
		selectCell(cellsIterator.previous());
	}

	function handleNextCellEvent() {
		selectCell(cellsIterator.next());
	}

	function handleSaveCellEvent() {
		var actualCell = cellsIterator.actual();
		var humanTranscription = $("#edition-field").val();

		var isFixed = actualCell.isFixed();
		if (!isFixed) {

			var isAnConfirmation = actualCell.getHumanTranscription() == humanTranscription;
			if (actualCell.getNumberOfConfirmations() == 0 || isAnConfirmation) {
				actualCell.increaseNumberOfConfirmation();
			} else {
				actualCell.setNumberOfConfirmations(1);
			}
			actualCell.setFixed(true);
			addCellSegmentsToLayer(true, actualCell);
			redrawLinesLayer();
		}
		actualCell.setHumanTranscription(humanTranscription);

		var nextCell = cellsIterator.next();
		if (nextCell.isFixed()) {
			unhighlightPreviousCell();
			$("#right-panel").hide();
		} else {
			selectCell(nextCell);
		}
		updateTaskbarProgress();
	}

	function updateTaskbarProgress() {
		var totalCell = cells.length;
		var nFixedCells = countFixedCells();
		var newPct = Math.round((nFixedCells * 100) / totalCell).toString() + "%";
		var currentPct = $("#task-bar-progress")[0].style.width;

        	if (newPct != currentPct) $("#task-bar-progress").tooltip('hide');

		$("#task-bar-progress").css("width", newPct);
		$("#task-bar-progress").attr("data-original-title", newPct.toString() + " completa!");
	}

	function handleTaskbarProgressChange() {
		var nFixedCells = countFixedCells();
		if (nFixedCells > 0) $('#task-bar-progress').tooltip('show');
	}

	function countFixedCells() {
		var count = 0;
		for (var i = 0; i < cells.length; i++) {
			if (cells[i].isFixed()) count++;
		}
		return count;
	}

	function selectCell(cell) {
		highlightCell(cell);
		focusCell(cell, true);
		updateRightPanel(cell);
	}

	function updateRightPanel(cell) {
		$("#right-panel").show();
		updateTranscriptionField(cell);
		updateCellViewerStage(cell);
	}

	function highlightCell(cell) {
		unhighlightPreviousCell();

		var cellSegs = cell.getSegments();
		for (var i = 0; i < cellSegs.length; i++) {
			var selectionSeg = createSegment(cellSegs[i].getPoints());

			selectionSeg.setStroke(highlightColor);
			selectionLayer.add(selectionSeg);
		}
		
		cell.setRectangleOpacity(0);
		if (cell.isFixed()) {
			fixedLayer.draw();
		} else {
			unfixedLayer.draw();
		}
		selectionLayer.draw();
	}

	function unhighlightPreviousCell() {

		var previousCell = cellsIterator.getPreviousCell();
		if (typeof previousCell == "undefined") return ;

		previousCell.setRectangleOpacity(0.25);
		if (previousCell.isFixed()) {
			fixedLayer.draw();
		} else {
			unfixedLayer.draw();
		}
		selectionLayer.destroyChildren();
		selectionLayer.draw();
	}

	function focusCell(cell, onTableViewer) {
		var cellBorders = cell.getBorders();

		if (onTableViewer) {
			viewer = $("#table-viewer");
			scale = tableViewerStage.getScale();
		} else {
			viewer = $("#canvas-cell-container");
			scale = cellViewerStage.getScale();
		}

		var scaledInitX = cellBorders[0] * scale.x;
		var scaledInitY = cellBorders[1] * scale.y;

		var scaledFinalX = cellBorders[2] * scale.x;
		var scaledFinalY = cellBorders[3] * scale.y;

		var shiftX = onTableViewer ? viewer.width()/2 + (scaledInitX - scaledFinalX)/2 : 0;
		var shiftY = onTableViewer ? viewer.height()/2  + (scaledInitY - scaledFinalY)/2 : 0;
		viewer.animate({scrollLeft: scaledInitX - shiftX, scrollTop: scaledInitY - shiftY}, 0);
	}

	function updateTranscriptionField(cell) {
		var pc_trancription_label = "O computador tem " + cell.confidence + "% de confiança na transcrição abaixo.";
		$("#pc-transcription-label").text(pc_trancription_label);
		$("#transcription-field").text(cell.getComputerTranscription());

		var lastAnswer = cell.getLastAnswer();
		if (typeof lastAnswer != "undefined" && cell.getNumberOfConfirmations() >= 1) {
			$("#human-transcription-field").text(lastAnswer);

			$("#human-transcription-field").show();
			$("#human-transcription-label").show();
		} else {
			$("#human-transcription-field").hide();
			$("#human-transcription-label").hide();
		}

		$("#edition-field").val(cell.getNumberOfConfirmations() == 0 ?
				 cell.getComputerTranscription() : cell.getHumanTranscription());
		$("#edition-field").blur();

		if (cell.isEditEnabled()) {
			$("#button-finished-transcription").show();
			$("#edition-field").removeAttr("disabled");
			$("#edition-field").focus();
			$("#edition-field").select();
		} else {
			$("#button-finished-transcription").hide();
			$("#edition-field").attr("disabled", "disabled");
		}
	}

	function handleMouseClickEvent(evt) {
		var mouseX = getMousePosX(evt);
		var mouseY = getMousePosY(evt);

		var cellIndex = findCell(mouseX, mouseY);

		if (cellIndex == -1) return;

		cellsIterator.updateActualIndex(cellIndex);
		selectCell(cellsIterator.actual());
	}

	function getMousePosX(evt) {
		var localEvt = typeof evt.originalEvent == "undefined" ? evt : evt.originalEvent;
		return (typeof localEvt.offsetX == "undefined") ? localEvt.layerX
				: localEvt.offsetX;
	}

	function getMousePosY(evt) {
		var localEvt = typeof evt.originalEvent == "undefined" ? evt : evt.originalEvent;
		return (typeof localEvt.offsetY == "undefined") ? localEvt.layerY
				: localEvt.offsetY;
	}

	function findCell(posX, posY) {
		var scale = tableViewerStage.getScale();
		for (var i = 0; i < cells.length; i++) {
			var cell = cells[i];
			if (cell.isPosInCell(posX, posY, scale)) {
				return i;
			}
		}
		return -1;
	}

	function getCompleteTranscriptionAnswer() {
		var cellsToSave = new Array();
		var computerValuesToSave = new Array();
		var humanValuesToSave = new Array();
		var confidencesToSave = new Array();
		var numberOfconfirmationsToSave = new Array();

		for (var i = 0; i < cells.length; i++) {
			var cell = cells[i];
			var borders = cell.getBorders();
			cellsToSave.push([borders[0] - shiftOnCanvas, borders[1] - shiftOnCanvas,
				borders[2] - shiftOnCanvas, borders[3] - shiftOnCanvas]);
			var incConfirmation = cell.getNumberOfConfirmations() + 1;

			computerValuesToSave.push(cell.getComputerTranscription());
			humanValuesToSave.push(typeof cell.getHumanTranscription() == "undefined" ? "" : cell.getHumanTranscription());
			confidencesToSave.push(cell.getConfidence());
			numberOfconfirmationsToSave.push(cell.getNumberOfConfirmations());
		}
		return JSON.stringify({'cells': cellsToSave, 'computer_values': computerValuesToSave,
			'human_values': humanValuesToSave, 'confidences': confidencesToSave, 'num_of_confirmations': numberOfconfirmationsToSave});
	}

	function clearCanvas() {
		tableViewerStage.destroy();
        	cellViewerStage.destroy();
	}
