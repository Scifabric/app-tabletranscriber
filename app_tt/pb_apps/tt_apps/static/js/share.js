$('body').on('contextmenu', '#share-canvas-container', function(e) {
	return false;
});

$('body').on('mouseup', function(e) {
	handleMouseUpEvent(e);
});

/*$("#share-canvas-container").popover({
	"trigger" : "manual",
	"placement" : "right"
});*/

var isShareActive = false;
var shareStage;
var shareArea;
var selectionLayer;
var APP_ID = "697196073638750";
//var APP_ID = "715128605186409";
var taskId;
var currentUserId;
var SHARE_HELP_ENABLED_MESSAGE = "Clique e arraste o mouse sobre uma área da tabela para compartilhar";
var SHARE_HELP_DISABLED_MESSAGE = "Compartilhe algo interessante da página abaixo";
var oldMessage = "";

function initSharer(tId, userId) {
	taskId = tId;
	currentUserId = userId;

	if (typeof FB == "undefined") {
		FB.init({appId: APP_ID, status: true, cookie: true});	
	}
}

function share() {
	if (isShareActive) {
		disableShare();
	} else {
		enableShare();
	}
}

function enableShare() {
	isShareActive = true;
	$("#button_share").addClass('active');
	document.body.style.cursor = "crosshair";
	createShareStage(true);
	
	oldMessage = $("#image-container").attr("data-original-title");
	$("#image-container").attr("data-original-title", SHARE_HELP_ENABLED_MESSAGE);
	$("#image-container").popover("show");
	//$("#share-canvas-container").popover("show");
	
	$("#button_share").attr("data-original-title", SHARE_HELP_ENABLED_MESSAGE);
	$("#button_share").trigger("mouseover");
}

function disableShare() {
	isShareActive = false;
	$("#button_share").removeClass('active');
	document.body.style.cursor = "default";
	shareStage.destroy();
	shareArea = undefined;
	$("#share-menu").hide();
	//$("#share-canvas-container").popover("hide");
	
/*	if ($("#image-container").attr("data-original-title") == "") {
		$("#image-container").popover("hide");
	} else {*/
	$("#image-container").attr("data-original-title", oldMessage);
	$("#image-container").popover("show");
	//}

	$("#button_share").attr("data-original-title", SHARE_HELP_DISABLED_MESSAGE);
	$("#button_share").trigger("mouseover");
	$("#button_share").trigger("mouseout");
}

function createShareStage(addEventHandlers) {
	shareStage = new Kinetic.Stage({
		container: 'share-canvas-container',
		width: 550,
		height: 700
	});

	selectionLayer = new Kinetic.Layer();
	shareStage.add(selectionLayer);

	if (!addEventHandlers) return;

	shareStage.on("mousedown", function(evt) {
		if (evt.which != 1) return;

		if (typeof shareArea != 'undefined') {
			removeShareArea();
		} else {
			shareArea = createShareArea(this.getMousePosition());
			selectionLayer.add(shareArea);
			selectionLayer.draw();
		}
		$("#share-menu").hide();
	});

	shareStage.on("mousemove", function(evt) {
		document.body.style.cursor = "crosshair";

		if (evt.which != 1 || $("#share-menu").is(":visible") ||
				typeof shareArea == "undefined") return;

		var mousePos = this.getMousePosition();

		var newX = mousePos.x;
		var newY = mousePos.y;

		var pos = shareArea.getAbsolutePosition();

		var deltaX = newX - pos.x;
		var deltaY = newY - pos.y;

		shareArea.setWidth(deltaX);
		shareArea.setHeight(deltaY);
		selectionLayer.draw();
	});
}

function createStageAndSetFocusArea(shareAreaInitX, shareAreaInitY, shareAreaFinalX, shareAreaFinalY) {
	createShareStage(false);
	createFocusArea(shareAreaInitX, shareAreaInitY, shareAreaFinalX, shareAreaFinalY);
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

function handleMouseUpEvent(evt) {
	if (evt.which != 1 || typeof shareArea == 'undefined') return;

	var pos = shareArea.getAbsolutePosition();

	var mousePosX = getMousePosX(evt);
	var mousePosY = getMousePosY(evt);
	var deltaX = mousePosX - pos.x;
	var deltaY = mousePosY - pos.y;

	if (deltaX == 0 || deltaY == 0) return;

	if (!$("#share-menu").is(":visible")) {
		var shareAreaInitX = pos.x;
		var shareAreaInitY = pos.y;
		var shareAreaFinalX = pos.x + shareArea.getWidth();
		var shareAreaFinalY = pos.y + shareArea.getHeight();
		createFocusArea(shareAreaInitX, shareAreaInitY, shareAreaFinalX, shareAreaFinalY);

		$("#share-menu").css("top", shareAreaFinalY - 20);
		$("#share-menu").css("left", shareAreaFinalX - 10);
		document.body.style.cursor = "pointer";
		$("#share-menu").show();
	}
}

function createFocusArea(shareAreaInitX, shareAreaInitY, shareAreaFinalX, shareAreaFinalY) {

	if (shareAreaInitX > shareAreaFinalX) {
		var tmp = shareAreaInitX;
		shareAreaInitX = shareAreaFinalX;
		shareAreaFinalX = tmp;
	} 

	if (shareAreaInitY > shareAreaFinalY) {
		var tmp = shareAreaInitY;
		shareAreaInitY = shareAreaFinalY;
		shareAreaFinalY = tmp;
	}

	var shareStageWidth = shareStage.getWidth();
	var shareStageHeight = shareStage.getHeight();
	var shareAreaWidth = Math.abs(shareAreaFinalX - shareAreaInitX);
	var shareAreaHeight = Math.abs(shareAreaFinalY - shareAreaInitY);

	var leftRect = new Kinetic.Rect({
		x: 0,
		y: 0,
		width: shareAreaInitX,
		height: shareStageHeight,
		fill: '#000',
		opacity: 0.6
	});

	var topRect = new Kinetic.Rect({
		x: shareAreaInitX,
		y: 0,
		width: shareAreaWidth,
		height: shareAreaInitY,
		fill: '#000',
		opacity: 0.6
	});

	var rightRect = new Kinetic.Rect({
		x: shareAreaFinalX,
		y: 0,
		width: shareStageWidth - shareAreaFinalX,
		height: shareStageHeight,
		fill: '#000',
		opacity: 0.6
	});

	var bottomRect = new Kinetic.Rect({
		x: shareAreaInitX,
		y: shareAreaFinalY,
		width: shareAreaWidth,
		height: shareStageHeight - shareAreaFinalY,
		fill: '#000',
		opacity: 0.6
	});

	selectionLayer.add(leftRect);
	selectionLayer.add(topRect);
	selectionLayer.add(rightRect);
	selectionLayer.add(bottomRect);
	selectionLayer.draw();
}

function createShareArea(mousePos) {
	var shareArea = new Kinetic.Rect({
		x: mousePos.x,
		y: mousePos.y,
		width: 0,
		height: 0,
		fillEnabled: false,
		stroke: 'black',
		dashArray: [2],
		strokeWidth: 2
	});
	return shareArea;
}

function getShareAreaBorders() {
	var pos = shareArea.getAbsolutePosition();
	return [pos.x, pos.y, pos.x + shareArea.getWidth(), pos.y + shareArea.getHeight()];
}

function shareOnFacebook() {

	var shareAreaBorders = getShareAreaBorders();

	var factInfo = {'task_id' : taskId, 'user_id': currentUserId, 'left_pos': shareAreaBorders[0], 'top_pos': shareAreaBorders[1], 'right_pos': shareAreaBorders[2], 'bottom_pos': shareAreaBorders[3]};
	var callback = function(factId) {
		showFacebookSharer(factId, factInfo);
	};

	saveFactInfo(factInfo, callback);
	removeShareArea();
	$("#share-menu").hide();
}

function showFacebookSharer(factId, factInfo) {

	var factLink = "http://" + window.location.host + '/mb/api/fact/' + factId;
	console.log(factLink);

	FB.ui({
		method: 'feed',
		link: factLink,
	}, function(response) {
		if (typeof response != undefined && response == null) return;

		saveFactInfo($.extend(factInfo, {'id': factId, 'post_id': response['post_id']}));
	});
}

function saveFactInfo(factInfo, callback) {
	$.ajax({
		type: 'POST',
		url:    '/mb/api/save_fact',
		contentType: 'application/json',
		data: JSON.stringify(factInfo),
		success: callback
	});
}

function removeShareArea() {
	shareArea = undefined;
	selectionLayer.removeChildren();
	selectionLayer.draw();
}
