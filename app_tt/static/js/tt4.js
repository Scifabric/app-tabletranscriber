(function($){

    $.fn.table = function(options){
		var opts = $.extend({}, $.fn.table.defaults, options);

        var image = this;
        this.image = this;

        this.imgUrl = opts.imgUrl;
        this.color = opts.color;
        this.cells = opts.cells;

        this.canvas = $('<div class="image-table-canvas"><div class="image-table-cells"></div><div class="image-table-text"></div></div>');
		this.image.after(this.canvas);

		// Give the canvas and the container their size and background
        this.canvas.height(this.height());
		this.canvas.width(this.width());
        console.log(this.css('margin'));
		this.canvas.css({ 'margin': this.css('margin')});
        this.canvas.css({ 'background-image': 'url("' + this.attr('src') + '")', 'background-size': this.height() + 'px' + this.width() + 'px;' });
		this.canvas.children('.image-table-cells, .image-table-text').height(this.height());
		this.canvas.children('.image-table-cells, .image-table-text').width(this.width());

        // var arr = [ [25,53,266,120], [267,53,339,120], [25,131,267,169], [267,131,343,169], [343,131,425,169], [425,131,506,169], [506,131,589,169], [342,53,427,120], [427,53,505,120], [505,53,589,120] ];
        //
        //
        //
        console.log(this.cells);
         // for (var i = 0; i < this.cells.length; i += 1) {
         //    console.log(this.cells[i]);
         //    coords = [this.cells[i][0], this.cells[i][1], this.cells[i][2], this.cells[i][3]];
         //    content = this.cells[i][4];
         //    $.fn.table.add(this,i, coords, content);
         // }

        // var cell = $.fn.table.add(this, 1, [0,20,40,40], "abcde");
        // var cell2 = $.fn.table.add(this, 2, [40,0,80,20], "fghij");
        // var cell3 = $.fn.table.add(this,3,[40,20,80,40],"klmno");
        // var cell4 = $.fn.table.add(this,4,[40,40,80,60],"pqrst");
        // var cell5 = $.fn.table.add(this,5,[80,20,120,40],"uvwxy");

		$.fn.table.load(this);
        this.hide();

        return this;

    };

    $.fn.table.defaults = {
            color: '#0120EC',
            cells: new Array()
    };

	$.fn.table.load = function(image){
		//console.log(image.cells);
		for(i=0; i< image.cells.length; i++){
			new $.fn.cellView(image, image.cells[i]);
		}
	};

    $.fn.table.add = function(image, id, coords, content){
        new $.fn.cell(image, id, coords, content);
    };


    // $.fn.cell = function(image, id, coords, content){
    //     this.image = image;

    //     //var imageRight = image.width() + imageLeft;
    //     //var imageBottom = image.height() + imageTop;
		
    //     var cellLeftTop = {x : coords[0], y : coords[1]};
    //     var cellRightBottom = {x: coords[2], y: coords[3]};

    //     var width = cellRightBottom.x - cellLeftTop.x;
    //     var height = cellRightBottom.y - cellLeftTop.y;

		// var newCell = new Object();
		// newCell.width = width;
		// newCell.height = height;
		// newCell.top = cellLeftTop.y;
		// newCell.left = cellLeftTop.x;
		// newCell.text = content;
    //     newCell.id = id;
		
		// image.cells.push(newCell);
		
        // return this;

    // };

    $.fn.cellView = function(image, cell) {
		///	<summary>
		///		Defines a cell area.
		///	</summary>
		this.image = image;
		this.cell = cell;
        this.inputOn = false;

		// Add the cell area
		var area = document.createElement('div');
		this.area = $(area).addClass('image-table-cell');
        this.area.attr('id', 'cell'+ this.cell.id);
		image.canvas.children('.image-table-cells').prepend(this.area);
		
		// Add the text
		var textSpan = $('<div class="image-table-cell-text"><span>Valor da célula:</span></div>');
        textSpan.append($('<p>' + this.cell.text + '</p>'));
		this.textSpan = textSpan;
		image.canvas.children('.image-table-text').prepend(textSpan);
		this.textSpan.hide();

        var form = $('<input class="image-table-cell-input" type="text" value="' + this.cell.text + '"/>');
        this.form = form;
        image.canvas.children('.image-table-text').prepend(this.form);
        this.form.hide();
               
		// Set the position and size of the cell
		this.setPos();

        var toShow = this;

        var textOn = function(){
			toShow.area.css('border-color', 'rgb(0,255,0)');
            toShow.textSpan.fadeIn();
        };
        var textOff = function(){
            toShow.textSpan.fadeOut();
        };


        this.area.hover(textOn,textOff); // Show the text on mouse hover

        var inputOff = function(){
            toShow.form.hide();
            toShow.inputOn = false;
            cell.text = toShow.form.attr('value');
            toShow.textSpan.children('p').text(cell.text);
            toShow.area.hover(textOn, textOff);

        };


        this.form.keypress(function(e){
            if(e.which == 13 ){
                inputOff();
            }
        });


        this.area.click(function(){
            if(!toShow.inputOn){
                toShow.form.show();
                toShow.inputOn = true;
                toShow.textSpan.hide();
                toShow.area.unbind('hover');
            }else{
                inputOff();
            }
        
        });

        // Toggle input text on click
        // $(document.body).click(function(e) {
        //     var target = $(e.target);
        //     if(target.attr('id') != ('cell' + toShow.cell.id) && target.attr('class') != toShow.form.attr('class') ) {
        //         toShow.form.hide();
        //         console.log("toShow cell " + toShow.form.attr('value'));
        //         //cell.text = toShow.form.attr('value');
        //         console.log("text cell "+cell.text);
        //         toShow.area.hover(textOn,textOff);
        //     }else if(target.attr('class') !=toShow.form.attr('class')){
        //         toShow.form.show();
        //         toShow.textSpan.hide();
        //         toShow.area.unbind('hover');
        //     }
        // });

        return this;
		
	};

    $.fn.cellView.prototype.setPos = function() {
		this.area.css('height', this.cell.height + 'px');
		this.area.css('width', this.cell.width + 'px');
		this.area.css('left', this.cell.left + 'px');
		this.area.css('top', this.cell.top + 'px');
        console.log(this.area.offset());
		var overWindow = this.cell.top < this.cell.height;
		this.textSpan.css('top', overWindow ? (this.cell.top + this.cell.height + 2) : (this.cell.top - this.cell.height)  + 'px');
		this.textSpan.css('left', this.cell.left + 'px');
        this.textSpan.css('height', this.cell.height + 'px');
        this.textSpan.css('width', this.cell.width + 'px');
        this.form.css('top', this.cell.top);
		this.form.css('left', this.cell.width + this.cell.left + 2 + 'px');
        this.form.css('width', this.cell.width);


    };

})(jQuery);
