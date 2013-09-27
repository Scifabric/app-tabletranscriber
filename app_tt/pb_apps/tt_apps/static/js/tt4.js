	$('body').on('contextmenu', '#canvas-container', function(e) {
		return false;
	});

	var DEFAULT_ZOOM_DELTA = 0.5;
	var MAX_X = Number.MAX_VALUE;
	var MAX_Y = Number.MAX_VALUE;
	var MIN_X = 0;
	var MIN_Y = 0;

	var stage;
	var linesLayer;
	var selectionLayer;
	var imageLayer;
	var img_url;
	var origStageMaxX;
	var origStageMaxY;

	var cells;
	var cellsIterator;

	var segWidth;
	var unhighlightColor;
	var highlightColor;

	var shiftOnCanvas;

	function initVariables() {
		cells = new Array();
		cellsIterator = new CellsIterator(cells);

		shiftOnCanvas = 1.5;
		segWidth = 2.5;
		unhighlightColor = "#E6663A";
		highlightColor = "#339ACD";
	}

	// Cell class definition
	function Cell() {
		this.segments = new Array();
		this.transcription = "Some value";
	}

	Cell.prototype.getTranscription = function() {
		return this.transcription;
	}

	Cell.prototype.setTranscription = function(newTranscription) {
		this.transcription = newTranscription;
	}

	Cell.prototype.addSegment = function(segment) {
		this.segments.push(segment);
	}

	Cell.prototype.getSegments = function() {
		return this.segments;
	}

	Cell.prototype.getSegmentAtPosition = function(posSeg) {
		for (var i = 0; i < this.segments.length; i++) {
			var segment = this.segments[i];
			if (segment.equalsSegmentPosition(posSeg)) {
				return segment;
			}
		}
		return undefined;
	}

	Cell.prototype.setStroke = function(color) {
		for (var i = 0; i < this.segments.length; i++) {
			this.segments[i].setStroke(color);
		}
	}

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

		return [minX, minY, maxX, maxY]
	}

	Cell.prototype.isPosInCell = function(posX, posY) {
		var borders = this.getBorders();
		var minX = borders[0];
		var minY = borders[1];
		var maxX = borders[2];
		var maxY = borders[3];
		
		return (posX >= minX && posX <= maxX) && (posY >= minY && posY <= maxY);
	}

	function CellsIterator(cells) {
		this.cells = cells;
		this.actualIndex = 0;
	}

	CellsIterator.prototype.next = function() {
		var nextIndex = this.actualIndex + 1;
		this.actualIndex =  nextIndex < this.cells.length ? nextIndex : 0;
		return this.actual();
	}

	CellsIterator.prototype.previous = function() {
		var previousIndex = this.actualIndex - 1;
		this.actualIndex =  previousIndex >= 0 ? previousIndex : (this.cells.length - 1);
		return this.actual();
	}

	CellsIterator.prototype.actual = function() {
		return this.cells[this.actualIndex];
	}

	CellsIterator.prototype.updateActualIndex = function(newIndex) {
		this.actualIndex = newIndex;
	}

	Kinetic.Line.prototype.equalsSegmentPosition = function(segPos) {
		var points = this.getPoints();
		return points[0].x == segPos[0].x && points[0].y == segPos[0].y && 
			points[1].x == segPos[1].x && points[1].y == segPos[1].y;
	}

	function zoomCanvas(isZoomIn, zoomDelta) {
		var actualScale = stage.getScale();

		var newScaleX = isZoomIn ?
			actualScale.x + zoomDelta : actualScale.x - zoomDelta;
		var newScaleY = isZoomIn ?
				actualScale.y + zoomDelta : actualScale.y - zoomDelta;

		if (newScaleX <= 0 || newScaleY <= 0) return;

		var newCanvasWidth = origStageMaxX * newScaleX;
		var newCanvasHeight = origStageMaxY * newScaleY;

		stage.setScale([newScaleX, newScaleY]);
		stage.setWidth(newCanvasWidth);
		stage.setHeight(newCanvasHeight);
		stage.draw();
	}

	function handleZoomOutToolEvent() {
		var isZoomIn = false;
		zoomCanvas(isZoomIn, DEFAULT_ZOOM_DELTA);
		focusCell(cellsIterator.actual());
	}

	function handleZoomInToolEvent() {
		var isZoomIn = true;
		zoomCanvas(isZoomIn, DEFAULT_ZOOM_DELTA);
		focusCell(cellsIterator.actual());
	}

	function createTableViewer(taskInfo) {
		initVariables();

		img_url = taskInfo.link;

		var tableMaxX = taskInfo.maxX;
		var tableMaxY = taskInfo.maxY;
		origStageMaxX = tableMaxX + (2 * shiftOnCanvas);
		origStageMaxY = tableMaxY + (2 * shiftOnCanvas);

		if (typeof stage != "undefined") {
			$(".kineticjs-content").remove();
		}

		stage = new Kinetic.Stage({
			container : 'canvas-container',
			width : origStageMaxX,
			height : origStageMaxY,
			scale : 1,
		});

		stage.on('click', function(evt) {
			handleMouseClickEvent(evt);     
		});

		linesLayer = new Kinetic.Layer();
		selectionLayer = new Kinetic.Layer();
		imageLayer = new Kinetic.Layer();

		var imageObj = new Image();
		imageObj.src = taskInfo.img_url;

		imageObj.onload = function() {
			var table = new Kinetic.Image({
				x : shiftOnCanvas,
				y : shiftOnCanvas,
				image : imageObj,
				width : tableMaxX,
				height : tableMaxY
			});

			imageLayer.add(table);
			table.moveToBottom();

			stage.add(imageLayer);
			stage.add(linesLayer);
			stage.add(selectionLayer);

			loadGrid(taskInfo);
		};
	}

	function loadGrid(taskInfo) {

		var isLastAnswer = typeof taskInfo.last_answer != "undefined";
		var taskInfoCells = isLastAnswer ? $.parseJSON(taskInfo.last_answer).cells : taskInfo.cells;

		for (var i = 0; i < taskInfoCells.length; i++) {
			
			var arr;
			if (isLastAnswer) {
				arr = taskInfoCells[i].coords;
			} else {
				arr = taskInfoCells[i];
			}

			var leftX = arr[0] + shiftOnCanvas;
			var upperY = arr[1] + shiftOnCanvas;
			var rightX = arr[2] + shiftOnCanvas;
			var bottomY = arr[3] + shiftOnCanvas;

			var cellLines = new Array();
			cellLines.push([{'x': leftX, 'y': upperY}, {'x': rightX, 'y': upperY}]);
			cellLines.push([{'x': leftX, 'y': upperY}, {'x': leftX, 'y': bottomY}]);
			cellLines.push([{'x': leftX, 'y': bottomY}, {'x': rightX, 'y': bottomY}]);
			cellLines.push([{'x': rightX, 'y': upperY}, {'x': rightX, 'y': bottomY}]);

			var cell = createCell(cellLines);
			if (isLastAnswer) {
				cell.setTranscription(taskInfoCells[i].val);
			}
			cells.push(cell);
		}

		selectCell(cellsIterator.actual());
		linesLayer.draw();
	}

	function createCell(cellLines) {
		var cell = new Cell();

		for (var i = 0; i < cellLines.length; i++) {
			var segment = findSegment(cellLines[i]);

			if (typeof segment == "undefined") {
				segment = createSegment(cellLines[i]);
				linesLayer.add(segment);
			}
			cell.addSegment(segment);
		}
		return cell;
	}

	function createSegment(posLine) {
		var kineticLine = new Kinetic.Line({
			points : posLine,
			stroke : unhighlightColor,
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
		if (typeof evt.keyCode != "undefined" && evt.keyCode == 13) {
			handleSaveCellEvent();
		}
	};

	function handlePreviousCellEvent() {
		selectCell(cellsIterator.previous());
	}

	function handleNextCellEvent() {
		selectCell(cellsIterator.next());
	}

	function handleSaveCellEvent() {
		var actualCell = cellsIterator.actual();
		actualCell.setTranscription($("#edition-field").val());

		selectCell(cellsIterator.next());
	}

	function selectCell(cell) {
		highlightCell(cell);
		focusCell(cell);
		updateTranscriptionField(cell);
	}

	function highlightCell(cell) {
		unhighlightSelectedCell();

		var cellSegs = cell.getSegments();
		for (var i = 0; i < cellSegs.length; i++) {
			var selectionSeg = createSegment(cellSegs[i].getPoints());

			selectionSeg.setStroke(highlightColor);
			selectionLayer.add(selectionSeg);
		}
		selectionLayer.draw();
	}

	function unhighlightSelectedCell() {
		selectionLayer.destroyChildren();
	}

	function focusCell(cell) {
		var cellBorders = cell.getBorders();
		var scaledCenterX = cellBorders[0] * stage.getScale().x;
		var scaledCenterY = cellBorders[1] * stage.getScale().y;

		var shiftX = $("#table-viewer").width()*0.22;
		var shiftY = $("#table-viewer").height()*0.22;

		$("#table-viewer").animate({scrollLeft: scaledCenterX - shiftX, scrollTop: scaledCenterY - shiftY});
	}

	function updateTranscriptionField(cell) {
		$("#transcription-field").text(cell.getTranscription());
		$("#edition-field").val(cell.getTranscription());
		$("#edition-field").focus();
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
		for (var i = 0; i < cells.length; i++) {
			var cell = cells[i];
			if (cell.isPosInCell(posX, posY)) {
				return i;
			}
		}
		return -1;
	}

	function getCompleteTranscriptionAnswer() {
		var cellsToSave = new Array();

		for (var i = 0; i < cells.length; i++) {
			var cell = cells[i];
			var borders = cell.getBorders();
			cellsToSave.push({'coords': [borders[0] - shiftOnCanvas, borders[1] - shiftOnCanvas,
							borders[2] - shiftOnCanvas, borders[3] - shiftOnCanvas], 'val': cell.getTranscription()});
		}
		return JSON.stringify({'cells' : cellsToSave});
	}

	function clearCanvas() {
		stage.removeChildren();
		stage.remove();
	}
