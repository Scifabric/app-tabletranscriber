                                                                                                                                                     /// <reference path="jquery-1.2.6-vsdoc.js" />
(function($) {

	$.fn.annotateImage = function(options) {
		///	<summary>
		///		Creates annotations on the given image.
		///     Images are loaded from the "getUrl" propety passed into the options.
		///	</summary>
		var opts = $.extend({}, $.fn.annotateImage.defaults, options);
		var image = this;

		this.image = this;
		
		this.mode = 'view';

		// Assign defaults
		this.getUrl = opts.getUrl;
		this.saveUrl = opts.saveUrl;
		this.deleteUrl = opts.deleteUrl;
		this.editable = opts.editable;
		this.useAjax = opts.useAjax;
		this.notes = opts.notes;
		this.clear = opts.clear;
        noteS = opts.notes;
		
		if(this.clear){
			$.fn.annotateImage.clear(this);
		}

		// Add the canvas
		this.canvas = $('<div class="image-annotate-canvas"><div class="image-annotate-view"></div><div class="image-annotate-edit"><div class="image-annotate-edit-area"></div></div></div>');
		this.canvas.children('.image-annotate-edit').hide();
		this.canvas.children('.image-annotate-view').hide();
		this.image.after(this.canvas);

		// Give the canvas and the container their size and background
		this.canvas.height(this.height());
		this.canvas.width(this.width());
		this.canvas.css('background-image', 'url("' + this.attr('src') + '")');
		this.canvas.children('.image-annotate-view, .image-annotate-edit').height(this.height());
		this.canvas.children('.image-annotate-view, .image-annotate-edit').width(this.width());

		// Add the behavior: hide/show the notes when hovering the picture
		this.canvas.hover(function() {
			if ($(this).children('.image-annotate-edit').css('display') == 'none') {
				$(this).children('.image-annotate-view').show();
			}
		}, function() {
			$(this).children('.image-annotate-view').hide();
		});

		this.canvas.children('.image-annotate-view').hover(function() {
			$(this).show();
		}, function() {
			$(this).hide();
		});

		// load the notes
		if (this.useAjax) {
			$.fn.annotateImage.ajaxLoad(this);
		} else {
			$.fn.annotateImage.load(this);
		}

		// Add the "Add a note" button
		if (this.editable) {/*
            this.button = $('<a class="image-annotate-add" id="image-annotate-add" href="#">Add Note</a>');
           this.button.click(function() {
                $.fn.annotateImage.add(image);
           });
            this.canvas.after(this.button);*/

			$.fn.annotateImage.mouseSelection(this);

		}

		// Hide the original
		this.hide();

		return this;
	};

	/**
	 * Plugin Defaults
	 **/
	$.fn.annotateImage.defaults = {
			getUrl: 'your-get.rails',
			saveUrl: 'your-save.rails',
			deleteUrl: 'your-delete.rails',
			editable: true,
			useAjax: true,
			clear: true,
			notes: new Array()
	};

	$.fn.annotateImage.clear = function(image) {
		///	<summary>
		///		Clears all existing annotations from the image.
		///	</summary>    
		$("#image-annotate-edit-form").remove();
		$(".image-annotate-canvas").remove();
		for (var i = 0; i < image.notes.length; i++) {
			image.notes[image.notes[i]].destroy();
		}
		image.notes = new Array();
		noteS = new Array();
	};

	$.fn.annotateImage.ajaxLoad = function(image) {
		///	<summary>
		///		Loads the annotations from the "getUrl" property passed in on the
		///     options object.
		///	</summary>
		$.getJSON(image.getUrl + '?ticks=' + $.fn.annotateImage.getTicks(), function(data) {
			image.notes = data;
			$.fn.annotateImage.load(image);
		});
	};

	$.fn.annotateImage.load = function(image) {
		///	<summary>
		///		Loads the annotations from the notes property passed in on the
		///     options object.
		///	</summary>
		for (var i = 0; i < image.notes.length; i++) {
			image.notes[image.notes[i]] = new $.fn.annotateView(image, image.notes[i]);
		}
	};

	$.fn.annotateImage.getTicks = function() {
		///	<summary>
		///		Gets a count og the ticks for the current date.
		///     This is used to ensure that URLs are always unique and not cached by the browser.
		///	</summary>        
		var now = new Date();
		return now.getTime();
	};

	$.fn.annotateImage.add = function(image, coords) {
		///	<summary>
		///		Adds a note to the image.
		///	</summary>        
		if (image.mode == 'view') {
			image.mode = 'edit';

			// Create/prepare the editable note elements
			var editable = new $.fn.annotateEdit(image,false,coords);

			$.fn.annotateImage.createSaveButton(editable, image);
			$.fn.annotateImage.createCancelButton(editable, image);
			
		}

	};

	$.fn.annotateImage.createSaveButton = function(editable, image, note) {
		///	<summary>
		///		Creates a Save button on the editable note.
		///	</summary>
		var ok = $('<a class="image-annotate-edit-ok">OK</a>');

		ok.click(function() {
			var form = $('#image-annotate-edit-form form');
			var text = {titulo : $('#titulo').val(), subtitulo: $('#subtitulo').val(), conteudo: $('#conteudo').val(), rodape: $('#rodape').val()};
			$.fn.annotateImage.appendPosition(form, editable);
			image.mode = 'view';

			// Save via AJAX
			if (image.useAjax) {
				$.ajax({
					url: image.saveUrl,
					data: form.serialize(),
					error: function(e) { alert("An error occured saving that note."); },
					success: function(data) {
						if (data.annotation_id != undefined) {
							editable.note.id = data.annotation_id;
						}
					},
					dataType: "json"
				});
			}

			// Add to canvas
			if (note) {
				note.resetPosition(editable, text);
			} else {
				editable.note.editable = true;
				editable.note.text = text;
				note = new $.fn.annotateView(image, editable.note);
				note.resetPosition(editable, text);
				image.notes.push(editable.note);
			}
			editable.destroy();
		});
		editable.form.append(ok);
	};

	$.fn.annotateImage.createCancelButton = function(editable, image) {
		///	<summary>
		///		Creates a Cancel button on the editable note.
		///	</summary>
		var cancel = $('<a class="image-annotate-edit-close">Cancel</a>');
		cancel.click(function() {
			editable.destroy();
			image.mode = 'view';
		});
		editable.form.append(cancel);
	};

	$.fn.annotateImage.saveAsHtml = function(image, target) {
		var element = $(target);
		var html = "";
		for (var i = 0; i < image.notes.length; i++) {
			html += $.fn.annotateImage.createHiddenField("text_" + i, image.notes[i].text);
			html += $.fn.annotateImage.createHiddenField("top_" + i, image.notes[i].top);
			html += $.fn.annotateImage.createHiddenField("left_" + i, image.notes[i].left);
			html += $.fn.annotateImage.createHiddenField("height_" + i, image.notes[i].height);
			html += $.fn.annotateImage.createHiddenField("width_" + i, image.notes[i].width);
		}
		element.html(html);
	};

	$.fn.annotateImage.createHiddenField = function(name, value) {
		return '&lt;input type="hidden" name="' + name + '" value="' + value + '" /&gt;<br />';
	};

	$.fn.annotateEdit = function(image, note, coords) {
		///	<summary>
		///		Defines an editable annotation area.
		///	</summary>
		this.image = image;

		if (note) {
			this.note = note;
		} else {
			var newNote = new Object();
			newNote.id = "new";
			newNote.top = coords.top;
			newNote.left = coords.left;
			newNote.width = coords.width;
			newNote.height = coords.height;
			newNote.text = {titulo: "",subtitulo: "",rodape: ""};
			this.note = newNote;
		}

		// Set area
		var area = image.canvas.children('.image-annotate-edit').children('.image-annotate-edit-area');
		this.area = area;
		this.area.css('height', this.note.height + 'px');
		this.area.css('width', this.note.width + 'px');
		this.area.css('left', this.note.left + 'px');
		this.area.css('top', this.note.top + 'px');

		// Show the edition canvas and hide the view canvas
		image.canvas.children('.image-annotate-view').hide();
		image.canvas.children('.image-annotate-edit').show();

		// Add the note (which we'll load with the form afterwards)
		var form = $('<div id="image-annotate-edit-form"><form>	Título: <textarea type="textarea" id="titulo" rows="0">' + this.note.text.titulo + '</textarea><br/>' + 
					 'Subtítulo: <textarea type="textarea" id="subtitulo">' + this.note.text.subtitulo + '</textarea><br/>' +
                     'Conteúdo: <select size="1" id="conteudo"><option value="economia">Economia</option> <option value="populacao">População/Demografia</option>'+ 
                     '<option value="Violência/Criminalidade">Violência/Criminalidade</option></select>' +
					 'Rodapé: <textarea type="textarea" id="rodape">' + this.note.text.rodape + '</textarea></form></div>');
		this.form = form;

		$('body').append(this.form);
		this.form.css('left', (this.area.offset().left + this.area.width() + 7) + 'px');
		this.form.css('top', parseInt(this.area.offset().top) + 'px');

		// Set the area as a draggable/resizable element contained in the image canvas.
		// Would be better to use the containment option for resizable but buggy
		area.resizable({
			handles: 'all',

			stop: function(e, ui) {
				form.css('left', (area.offset().left + area.width() + 7) + 'px');
				form.css('top', parseInt(area.offset().top) + 'px');
			}
		})
		.draggable({
			containment: image.canvas,
			drag: function(e, ui) {
				form.css('left', (area.offset().left + area.width() + 7) + 'px');
				form.css('top', parseInt(area.offset().top) + 'px');
			},
			stop: function(e, ui) {
				form.css('left', (area.offset().left + area.width() + 7) + 'px');
				form.css('top', parseInt(area.offset().top) + 'px');
			}
		});
		return this;
	};

	$.fn.annotateEdit.prototype.destroy = function() {
		///	<summary>
		///		Destroys an editable annotation area.
		///	</summary>        
		this.image.canvas.children('.image-annotate-edit').hide();
		this.area.resizable('destroy');
		this.area.draggable('destroy');
		this.area.css('height', '');
		this.area.css('width', '');
		this.area.css('left', '');
		this.area.css('top', '');
		this.form.remove();
	};

	$.fn.annotateView = function(image, note) {
		///	<summary>
		///		Defines a annotation area.
		///	</summary>
		this.image = image;
		this.note = note;

		this.editable = (note.editable && image.editable);

		// Add the area
		this.area = $('<div class="image-annotate-area' + (this.editable ? ' image-annotate-area-editable' : '') + '"><div></div></div>');
		image.canvas.children('.image-annotate-view').prepend(this.area);


		// Add the note
		this.form = $('<div class="image-annotate-note">' + note.text.titulo + '</div>');
		this.form.hide();
		image.canvas.children('.image-annotate-view').append(this.form);
		this.form.children('span.actions').hide();

		// Set the position and size of the note
		this.setPosition();

		// Add the behavior: hide/display the note when hovering the area
		var annotation = this;
		this.area.hover(function() {
			annotation.show();
		}, function() {
			annotation.hide();
		});

		// Edit a note feature
		if (this.editable) {
			var form = this;
			if(form.form){		
				this.area.click(function() {
					form.edit();
				});
			}
		}
	};

	$.fn.annotateView.prototype.setPosition = function() {
		///	<summary>
		///		Sets the position of an annotation.
		///	</summary>
		this.area.children('div').height((parseInt(this.note.height) - 2) + 'px');
		this.area.children('div').width((parseInt(this.note.width) - 2) + 'px');
		this.area.css('left', (this.note.left) + 'px');
		this.area.css('top', (this.note.top) + 'px');
		this.form.css('left', (this.note.left) + 'px');
		this.form.css('top', (parseInt(this.note.top) + parseInt(this.note.height) + 7) + 'px');
	};

	$.fn.annotateView.prototype.show = function() {
		///	<summary>
		///		Highlights the annotation
		///	</summary>
		this.form.fadeIn(250);
		if (!this.editable) {
			this.area.addClass('image-annotate-area-hover');
		} else {
			this.area.addClass('image-annotate-area-editable-hover');
		}
	};

	$.fn.annotateView.prototype.hide = function() {
		///	<summary>
		///		Removes the highlight from the annotation.
		///	</summary>      
		this.form.fadeOut(250);
		this.area.removeClass('image-annotate-area-hover');
		this.area.removeClass('image-annotate-area-editable-hover');
	};

	$.fn.annotateView.prototype.destroy = function() {
		///	<summary>
		///		Destroys the annotation.
		///	</summary>      
		this.area.remove();
		this.form.remove();
	};

	$.fn.annotateView.prototype.edit = function() {
		///	<summary>
		///		Edits the annotation.
		///	</summary>      

		if (this.image.mode == 'view') {
			this.image.mode = 'edit';
			var annotation = this;

			// Create/prepare the editable note elements
			var editable = new $.fn.annotateEdit(this.image, this.note);

			$.fn.annotateImage.createSaveButton(editable, this.image, annotation);

			// Add the delete button
			var del = $('<a class="image-annotate-edit-delete">Delete</a>');
			del.click(function() {
				var form = $('#image-annotate-edit-form form');

				$.fn.annotateImage.appendPosition(form, editable);

				if (annotation.image.useAjax) {
					$.ajax({
						url: annotation.image.deleteUrl,
						data: form.serialize(),
						error: function(e) { alert("An error occured deleting that note."); }
					});
				}

				annotation.image.mode = 'view';
				editable.destroy();
				annotation.destroy();
				noteS = $.fn.annotateImage.removeNote(noteS,annotation.note);
			});
			editable.form.append(del);

			$.fn.annotateImage.createCancelButton(editable, this.image);
		}
	};

	$.fn.annotateImage.appendPosition = function(form, editable) {
		///	<summary>
		///		Appends the annotations coordinates to the given form that is posted to the server.
		///	</summary>
		var areaFields = $('<input type="hidden" value="' + editable.area.height() + '" name="height"/>' +
				'<input type="hidden" value="' + editable.area.width() + '" name="width"/>' +
				'<input type="hidden" value="' + editable.area.position().top + '" name="top"/>' +
				'<input type="hidden" value="' + editable.area.position().left + '" name="left"/>' +
				'<input type="hidden" value="' + editable.note.id + '" name="id"/>');
		form.append(areaFields);
	};

	$.fn.annotateView.prototype.resetPosition = function(editable, text) {
		///	<summary>
		///		Sets the position of an annotation.
		///	</summary>
		this.form.html(text);
		this.form.hide();

		// Resize
		this.area.children('div').height(editable.area.height() + 'px');
		this.area.children('div').width((editable.area.width() - 2) + 'px');
		this.area.css('left', (editable.area.position().left) + 'px');
		this.area.css('top', (editable.area.position().top) + 'px');
		this.form.css('left', (editable.area.position().left) + 'px');
		this.form.css('top', (parseInt(editable.area.position().top) + parseInt(editable.area.height()) + 7) + 'px');

		// Save new position to note
		this.note.top = editable.area.position().top;
		this.note.left = editable.area.position().left;
		this.note.height = editable.area.height();
		this.note.width = editable.area.width();
		this.note.text = text;
		this.note.id = editable.note.id;
		this.editable = true;
	};

	/**
	 * <summary>
	 * 		Add a note with a mouse selection
	 */
	
	
	$.fn.annotateImage.mouseSelection = function(obj){
		cont = 0;
		intoNote = false;

		$("div.image-annotate-area-editable").live("mouseenter", function(){
			intoNote = true;
		}).live("mouseleave", function(){
			intoNote=false;
		}); 


		$("div.image-annotate-edit-area.ui-resizable.ui-draggable").live("mouseenter", function(){
			intoNote = true;
		}).live("mouseleave", function(){
			intoNote=false;
		});


		doSelect($(obj).parent());

		function doSelect(parent){

			var objOffset = parent.offset();
			offsetLeft = objOffset.left;
			offsetTop = objOffset.top;
			maxWidth = offsetLeft + parent.width();
			maxHeight = offsetTop + parent.height();
			x1 = 0; y1 = 0; x2 = 0; y2 = 0; width = 0; height = 0; selTop = 0; selLeft = 0;
			parent.unbind("mousedown").bind("mousedown",onMouseDown);				  

		}

		function onMouseDown(e){

			if(!intoNote){
				document.onselectstart = function(){ return false; };
				x1 = e.pageX - offsetLeft;
				y1 =  e.pageY - offsetTop;
				$(this).append("<div id='mark"+ cont +"' style='position: absolute; border: 1px inset; left: " + x1 + "px; top: " + y1 + "px;' ></div>");
				selectionDiv = $("#mark"+cont);
				$(document).mousemove(setSelection).one('mouseup',selectionEnd).unbind("mousedown");
			}
		}

		function setSelection(e){
			if(e.pageX < offsetLeft){
				x2 = 0;
			}
			else if(e.pageX > maxWidth){
				x2 = maxWidth - offsetLeft;
			}else{
				x2 = e.pageX-offsetLeft;
			}

			if(e.pageY < offsetTop){
				y2= 0;
			}else if(e.pageY > maxHeight){
				y2 = maxHeight-offsetTop;
			}else{
				y2 = e.pageY-offsetTop;
			}

			width = x2-x1;
			height = y2-y1;

			if(width < 0 && height < 0){
				selLeft = x2;
				selTop = y2;
				selectionDiv.css({'left': selLeft, 'top': selTop, 'width' : Math.abs(width), 'height' : Math.abs(height), 'cursor' : 'crosshair'}); 		  
			}else if(width < 0){
				selLeft = x2;
				selTop = y1;
				selectionDiv.css({'left': selLeft, 'top': selTop, 'width' : Math.abs(width), 'height' : Math.abs(height), 'cursor' : 'crosshair'});  
			}else if(height < 0){
				selLeft = x1;
				selTop = y2;
				selectionDiv.css({'left': selLeft, 'top': selTop, 'width' : Math.abs(width), 'height' : Math.abs(height), 'cursor' : 'crosshair'}); 
			}else{
				selLeft = x1;
				selTop = y1;
				selectionDiv.css({'left': selLeft, 'top': selTop,'width' : Math.abs(width), 'height' : Math.abs(height), 'cursor' : 'crosshair'});		  		  
			}
		}

		function selectionEnd(e){

			$(document).unbind("mousemove");
			selectionDiv.remove();
			cont++;
			var coords = {top: selTop,left: selLeft, width: Math.abs(width), height: Math.abs(height)};
			$.fn.annotateImage.add(obj,coords);
				
		}
	};
	
	
	$.fn.annotateImage.addNote = function(note){
		noteS.push(note);
	};
	
	$.fn.annotateImage.removeNote = function(notes,note){
		var iToRemove = $.inArray(note,notes);
		var auxNotes = new Array();
		
		for(var i = 0; i < notes.length; i++){
			if(iToRemove == i) continue;
			auxNotes.push(notes[i]);
		}
		
		notes = auxNotes;

		return notes;
	};
	
	$.fn.annotateImage.exportJsonData = function(){
		jsonData = noteS;
		// for (var i = 0; i < noteS.length; i++) {
		// 	jsonData.push({data: {titulo: noteS[i].text.titulo, subtitulo: noteS[i].text.subtitulo, conteudo: noteS[i].text.conteudo,
                    // rodape: noteS[i].text.rodape}, coords: {x1: noteS[i].left, y1:noteS[i].top, x2: noteS[i].left + noteS[i].width , y2: noteS[i].top + noteS[i].height}});
		// }
        // console.log(jsonData);
		
		return JSON.stringify(jsonData);
	};
		
})(jQuery);
