	$('body').on('contextmenu', '#canvas-container', function(e) {
		return false;
	});

	// CONSTANTS
	var MAX_X = 2000;
	var MAX_Y = 2000;
	var MIN_X = 0;
	var MIN_Y = 0;

	var img_url;
	var linhas;
	var colunas;
	var minX;
	var maxX;
	var minY;
	var maxY;
	var minDistance;
	var shiftOnCanvas;
	var highlightColor;
	var unhighlightColor;

	var toolBarState;
	var splitToolCursor;

	var segmentosSelecionados;
	var desenhandoSegmento;
	var isMouseDown;

	var mouseOverQueue;
	var novoSegmento;
	var selectionArea;

   	var zoom;
	var hasZoom;

	var stage;
	var imageLayer;
	var linhasLayer;
	var colunasLayer;
	var pointsLayer;
	var selectionLayer;
	var layerZoom;

	var sortLinesFunction = function(a, b) {
		pointsA = a.getPoints();
		pointsB = b.getPoints();
		posAX = pointsA[0].x;
		posAY = pointsA[0].y;
		posBX = pointsB[0].x;
		posBY = pointsB[0].y;

		if (posAY != posBY)
			return posAY - posBY;
		return posAX - posBX;
	};

	var sortColumnsFunction = function(a, b) {
                pointsA = a.getPoints();
                pointsB = b.getPoints();
                posAX = pointsA[0].x;
                posAY = pointsA[0].y;
                posBX = pointsB[0].x;
                posBY = pointsB[0].y;

                if (posAX != posBX)
                        return posAX - posBX;
                return posAY - posBY;
        };

	function initVariables(taskInfo, serverName) {
		linhas = new Array();
		colunas = new Array();
		segmentosUnidos = new Array();
	   	zoom = new Array();
		mouseOverQueue = new Array();
		segmentosSelecionados = new Array();

		resetToolBar();
		enableSelectionTool(true);

		isMouseDown = false;
		hasZoom = false;
		imageLayer = new Kinetic.Layer();
		linhasLayer = new Kinetic.Layer();
		colunasLayer = new Kinetic.Layer();
		pointsLayer = new Kinetic.Layer();
		selectionLayer = new Kinetic.Layer();

		segWidth = 2.5
		// distancia minima entre linhas e colunas (em pixels)
		minDistance = 7.5;
		// ajuste para que as linhas nas bordas aparecam completamente
		shiftOnCanvas = 25;
		unhighlightColor = "#E6663A";
		highlightColor = "#339ACD";

		hasZoom = taskInfo.hasZoom;
		img_url = taskInfo.img_url;
		splitToolCursor = "url('" + serverName + "/images/split_tool.png') 10 8, auto";

		if (hasZoom) zoom = taskInfo.zoom;

		minX = MAX_X;
		minY = MAX_Y;
		maxX = MIN_X;
		maxY = MIN_Y;
	}

	function resetToolBar() {
		enableSelectionTool(false);
		enableAreaSelectionTool(false);
		enableAddTool(false);
		enableSplitTool(false);

		resetSelecao();
		desenhandoSegmento = false;
	}

	function resetSelecao() {
		for (var i = 0; i < segmentosSelecionados.length; i++) {
			unhighlightSegmento(segmentosSelecionados[i]);
		}
		segmentosSelecionados = new Array();
	}

	// Segmento class definition
	function Segmento(segmento, pointsLayer) {
		this.segmento = segmento;
		this.shift = 2;

		var points = segmento.getPoints();

		this.initRect = new Kinetic.Rect({
				x: points[0].x - this.shift,
				y: points[0].y - this.shift,
				width: 4,
				height: 4,
				fill: 'black',
				visible: false
			      });

		this.finalRect = new Kinetic.Rect({
				x: points[1].x - this.shift,
				y: points[1].y - this.shift,
				width: 4,
				height: 4,
				fill: 'black',
				visible: false
			      });

		pointsLayer.add(this.initRect);
		pointsLayer.add(this.finalRect);
	}

	Segmento.prototype.getPoints = function(){
		return this.segmento.getPoints();
	}

	Segmento.prototype.setStroke = function(color) {
		this.segmento.setStroke(color);
		
		if (color == highlightColor) {
			this.initRect.show();
			this.finalRect.show();
		} else {
			this.initRect.hide();
			this.finalRect.hide();
		}
	}

	Segmento.prototype.getStroke = function() {
		return this.segmento.getStroke();
	}

	Segmento.prototype.setVisible = function(visible) {
		return this.segmento.setVisible(visible);
	}

	Segmento.prototype.setPoints = function(posArray) {
		this.segmento.setPoints(posArray);

		var points = this.segmento.getPoints();
		this.initRect.setX(points[0].x - this.shift);
		this.initRect.setY(points[0].y - this.shift);

		this.finalRect.setX(points[1].x - this.shift);
		this.finalRect.setY(points[1].y - this.shift);
	}

	Segmento.prototype.remove = function() {
		this.segmento.remove();
		this.initRect.remove();
		this.finalRect.remove();
	}

	Segmento.prototype.getInitRect = function(){
		return this.initRect;
	}

	Segmento.prototype.getFinalRect = function(){
		return this.finalRect;
	}

	function isLinha(pts) {
		return pts[0].y == pts[1].y;
	}

	function isMesmaLinha(points1, points2) {
		return isLinha(points1) && isLinha(points2) && points1[0].y == points2[0].y;
	}

	function isLinhaDaBorda(pts) {
		return isLinha(pts) && pts[0].y == maxY;
	}

	function isColuna(pts) {
		return pts[0].x == pts[1].x;
	}

	function isMesmaColuna(points1, points2) {
		return isColuna(points1) && isColuna(points2)
				&& points1[0].x == points2[0].x;
	}

	function isColunaDaBorda(pts) {
		return isColuna(pts) && pts[0].x == maxX;
	}

	function isBorda(pontos) {
		return ((pontos[0].x == pontos[1].x && (pontos[0].x == maxX || pontos[0].x == minX)) || (pontos[0].y == pontos[1].y && (pontos[0].y == maxY || pontos[0].y == minY)));
	}

	function isPosBorda(pontos) {
		return ((pontos[0] == pontos[2] && (pontos[0] == maxX || pontos[0] == minX)) || (pontos[1] == pontos[3] && (pontos[1] == maxY || pontos[1] == minY)));
	}

	function isPosColuna(pontos) {
		return pontos[0] == pontos[2];
	}

	function isPosLinha(pontos) {
		return pontos[1] == pontos[3];
	}

	function moverLinha(seg, newPosY) {
		var segPoints = seg.getPoints();
		if (!isBorda(segPoints) && inZoom(newPosY) && temColunasDelimitando(segPoints)) {
			seg.setPoints([ segPoints[0].x, newPosY, segPoints[1].x, newPosY ]);
			atualizaColunasPerpendiculares(segPoints, newPosY);
		}
	}
	
	function atualizaColunasPerpendiculares(segPoints, newPosY) {
		var posY = segPoints[0].y;
		for (var i = colunas.length -1; i >= 0; i--) {
			var points = colunas[i].getPoints();
			if (!insideClosedInterval(segPoints[0].x, segPoints[1].x, points[0].x)) continue;

			if (points[0].y == posY) {
				colunas[i].setPoints([points[0].x, newPosY, points[1].x,  points[1].y]);
			} else if (points[1].y == posY) {
				colunas[i].setPoints([points[0].x, points[0].y, points[1].x, newPosY]);
			}

			var newPoints = colunas[i].getPoints();
			if (newPoints[0].y == newPoints[1].y) {
				colunas[i].remove();
				colunas.splice(i, 1);
			}
		}
	}

	function moverColuna(seg, newPosX) {
		var segPoints = seg.getPoints();
		if (!isBorda(segPoints) && temLinhasDelimitando(segPoints)) {
			seg.setPoints([ newPosX, segPoints[0].y, newPosX, segPoints[1].y ]);
			atualizaLinhasPerpendiculares(segPoints, newPosX);
		}
	}

	function temLinhasDelimitando(colPoints) {
		var cruzandoComeco = false;
		var cruzandoFim = false;
		var colX = colPoints[0].x;
		var toquesNoInicio = 0;
		var toquesNoFim = 0;

		for (var i = 0; i < linhas.length; i++) {
			var segPoints = linhas[i].getPoints();

			// inicio da coluna na mesma altura da linha
			if (colPoints[0].y == segPoints[0].y) {
				if (insideInterval(segPoints[0].x, segPoints[1].x, colX)) {
					cruzandoComeco = true;
				} else if (segPoints[0].x == colX || segPoints[1].x == colX) {
					toquesNoInicio++;
				}
			// final da coluna na mesma altura da linha
			} else if (colPoints[1].y == segPoints[0].y) {
				
				if (insideInterval(segPoints[0].x, segPoints[1].x, colPoints[0].x)) {
					cruzandoFim = true;
				} else if (segPoints[0].x == colX || segPoints[1].x == colX) {
					toquesNoFim++;
				}
			}
		}

		if (hasZoom) {
			if (colPoints[0].y == (zoom[1] + shiftOnCanvas)) cruzandoComeco = true;
			if (colPoints[1].y == (zoom[3] + shiftOnCanvas)) cruzandoFim = true;
		}

		return (cruzandoComeco && cruzandoFim) || (cruzandoComeco && toquesNoFim == 2) ||
				 (toquesNoInicio == 2 && cruzandoFim) || (toquesNoInicio == 2 && toquesNoFim == 2);
	}

	function temColunasDelimitando(linPoints) {
		var cruzandoComeco = false;
		var cruzandoFim = false;
		var linY = linPoints[0].y;
		var toquesNoInicio = 0;
		var toquesNoFim = 0;

		for (var i = 0; i < colunas.length; i++) {
			var segPoints = colunas[i].getPoints();

			// inicio da linha na mesma distancia da coluna
			if (linPoints[0].x == segPoints[0].x) {
				if (insideInterval(segPoints[0].y, segPoints[1].y, linY)) {
					cruzandoComeco = true
				} else if (segPoints[0].y == linY || segPoints[1].y == linY) {
					toquesNoInicio++;
				}
			// final da linha na mesma distancia da coluna
			} else if (linPoints[1].x == segPoints[0].x) {
				if (insideInterval(segPoints[0].y, segPoints[1].y, linY)) {
					cruzandoFim = true;
				} else if (segPoints[0].y == linY || segPoints[1].y == linY) {
					toquesNoFim++;
				}
			}
		}
		return (cruzandoComeco && cruzandoFim) || (cruzandoComeco && toquesNoFim == 2) ||
				 (toquesNoInicio == 2 && cruzandoFim) || (toquesNoInicio == 2 && toquesNoFim == 2);
	}

	function atualizaLinhasPerpendiculares(segPoints, newPosX) {
		var posX = segPoints[0].x;
		for (var i = linhas.length -1; i >= 0; i--) {
			var points = linhas[i].getPoints();
			if (!insideClosedInterval(segPoints[0].y, segPoints[1].y, points[0].y)) continue;
			
			if (points[0].x == posX) {
				linhas[i].setPoints([newPosX, points[0].y, points[1].x,  points[1].y]);
			} else if (points[1].x == posX) {
				linhas[i].setPoints([points[0].x, points[0].y, newPosX, points[1].y]);
			}

			var newPoints = linhas[i].getPoints();
			if (newPoints[0].x == newPoints[1].x) {
				linhas[i].remove();
				linhas.splice(i, 1);
			}
		}
	}

	function adicionarFocoZoom(zoom){

		layerZoom = new Kinetic.Layer();

		var topRect = new Kinetic.Rect({
		    x: getTableMinX(),
		    y: getTableMinY(),
		    width: zoom[2],
		    height: zoom[1],
		    fill: '#000',
		    opacity: 0.6
		});

		var zoomFinalPosY = zoom[3] + shiftOnCanvas;
		var botRect = new Kinetic.Rect({
		    x: getTableMinX(),
		    y: zoomFinalPosY,
		    width: zoom[2],
		    height: getTableMaxY() - zoomFinalPosY,
		    fill: '#000',
		    opacity: 0.6
		});
		
		layerZoom.add(topRect);
		layerZoom.add(botRect);
	}

	function inZoom(posY){
		return !hasZoom || (posY >= getZoomUpperY() && posY <= getZoomBottomY());
	}

	function getZoomUpperY() {
		return  zoom[1] + shiftOnCanvas;
	}

	function getZoomBottomY() {
		return zoom[3] + shiftOnCanvas;
	}

	function criarNovaLinha(posY, initX, finalX) {
	        if (inZoom(posY)) {
			var intercessoes = encontraIntercessoesVerticais(posY);
			var minX = MAX_X;
			var maxX = MIN_X;

			for (var z = 0; z < intercessoes.length - 1; z++) {
				if ((intercessoes[z] >= initX && intercessoes[z] <= finalX) ||
					(intercessoes[z + 1] >= initX && intercessoes[z + 1] <= finalX) ||
						(intercessoes[z] <= initX && intercessoes[z + 1] >= finalX)) {

					if (intercessoes[z] < minX) minX = intercessoes[z];
					if (intercessoes[z+1] > maxX) maxX = intercessoes[z+1];
				}
			}
			return adicionarSegmento([ minX, posY, maxX, posY ]);	
        	}
	}

	function criarNovaColuna(posX, initY, finalY) {
		var intercessoes = encontraIntercessoesHorizontais(posX);
		var minY = MAX_Y;
		var maxY = MIN_Y;

		for (var z = 0; z < intercessoes.length - 1; z++) {
			if ((intercessoes[z] >= initY && intercessoes[z] <= finalY) ||
				(intercessoes[z + 1] >= initY && intercessoes[z + 1] <= finalY) ||
					(intercessoes[z] <= initY && intercessoes[z + 1] >= finalY)) {

				if (intercessoes[z] < minY) minY = intercessoes[z];
				if (intercessoes[z+1] > maxY) maxY = intercessoes[z+1];
			}
		}

		if (hasZoom) {
			var zoomMinY = zoom[1] + shiftOnCanvas;
			if (minY < zoomMinY) {
				minY = zoomMinY;
			}
			var zoomMaxY = zoom[3] + shiftOnCanvas;
			if (maxY > zoomMaxY) {
				maxY = zoomMaxY;
			}
		}
		return adicionarSegmento([ posX, minY, posX, maxY ]);		
	}

	function encontraIntercessoesVerticais(altura) {
		var intercessoes = new Array();
		for (var z = 0; z < colunas.length; z++) {
			var pts2 = colunas[z].getPoints();
			if (pts2[0].x == pts2[1].x) {
				if (pts2[0].y <= altura && pts2[1].y >= altura) {
					if (($.inArray(pts2[0].x, intercessoes)) == -1) {
						intercessoes.push(pts2[0].x);
					}
				}
			}
		}
		intercessoes.sort(function(a, b) {
			return a - b;
		});
		return intercessoes;
	}

	function encontraIntercessoesHorizontais(distancia) {
		var intercessoes = new Array();
		for (var z = 0; z < linhas.length; z++) {
			var pts2 = linhas[z].getPoints();
			if (pts2[0].y == pts2[1].y) {
				if (pts2[0].x <= distancia && pts2[1].x >= distancia) {
					if (($.inArray(pts2[0].y, intercessoes)) == -1) {
						intercessoes.push(pts2[0].y);
					}
				}
			}
		}
		intercessoes.sort(function(a, b) {
			return a - b;
		});
		return intercessoes;
	}

	function adicionarSegmento(pontos) {

		var kineticLine = new Kinetic.Line({
			points : pontos,
			stroke : unhighlightColor,
			strokeWidth : segWidth,
			draggable: true,
			drawHitFunc: function(canvas) {
			  var x1 = this.getPoints()[0].x;
			  var y1 = this.getPoints()[0].y;
			  var x2 = this.getPoints()[1].x;
			  var y2 = this.getPoints()[1].y;
			  var context = canvas.getContext();
			  context.beginPath();
			  
			  // a rectangle around the line
			  var linePad = 2.5;
			  context.moveTo(x1-linePad,y1-linePad);
			  context.lineTo(x2+linePad,y1-linePad);
			  context.lineTo(x2+linePad,y2+linePad);
			  context.lineTo(x1-linePad,y2+linePad);
			  context.closePath();
			  canvas.fillStroke(this);
			},
			dragBoundFunc: function(pos, event) {
				var points = this.getPoints();
				if (typeof event == 'undefined' || isBorda(points) ||
						isSplitToolActive() || isAreaToolActive()) {
					return {x : this.getAbsolutePosition().x, y : this.getAbsolutePosition().y};
				}

				var seg = getSegmento(points);
				if (isColuna(points)) {
					var posX = getMousePosX(event);
					var limEsq = encontraLimiteEsquerda(points);
					var limDir = encontraLimiteDireita(points);

					var newX = posX <= limEsq ? limEsq
							: (posX >= limDir ? limDir : posX);
					moverColuna(seg, newX);
				} else {
					var posY = getMousePosY(event);
					var limSup = encontraLimiteSuperior(points);
					var limInf = encontraLimiteInferior(points);
		
					var newY = posY <= limSup ? limSup
							: (posY >= limInf? limInf : posY);
					moverLinha(seg, newY);
				}

				if (hasSelectedSegment()) {
					clearSelection();
					resetSelecao();
				}
				highlightSegmento(seg);
				document.body.style.cursor = "move";
				layersRedraw();
				return {x : this.getAbsolutePosition().x, y : this.getAbsolutePosition().y};
			}
		});

		kineticLine.on("mouseover touchstart",
				function(evt) {
					var points = this.getPoints();
					var mouseOverElement = getSegmento(points);
					mouseOverQueue.push(mouseOverElement);

					if (isMouseDown || isAreaToolActive() || isBorda(points)) return;

					if (isSelectionToolActive() || isAddToolActive()) {
						document.body.style.cursor = "pointer";
					}

					if (hasSelectedSegment() && !isSplitToolActive() &&
						 this.getStroke() == highlightColor) {
						document.body.style.cursor = "move";
					}

					highlightSegmento(mouseOverElement);
					layersRedraw();
		});

		kineticLine.on('mouseout touchend', function(evt) {
			var points = this.getPoints();
			mouseOverQueue.shift();

			if (isMouseDown || isAreaToolActive() || isBorda(points)) return;

			if (isAddToolActive()) {
				document.body.style.cursor = "crosshair";
			}

			if (isSelectionToolActive() && !isMouseOverAnElement()) {
				document.body.style.cursor = "default";
			}

			if (isSegmentoSelected(points)) return;

			var mouseOverElement = getSegmento(points);
			if (typeof mouseOverElement != "undefined") {
				unhighlightSegmento(mouseOverElement);
				layersRedraw();
			}
		});

		var segmento = new Segmento(kineticLine, pointsLayer);

		if (isLinha(segmento.getPoints())) {
			linhas.push(segmento);
			linhasLayer.add(kineticLine);
		} else {
			colunas.push(segmento);
			colunasLayer.add(kineticLine);
		}
		return segmento;
	}

	function isSegmentoSelected(segPoints) {
		for (var i = 0; i < segmentosSelecionados.length; i++) {
			var points = segmentosSelecionados[i].getPoints();
			if (equalsSegmento(segPoints, points)) return true;
		}
		return false;
	}

	function clearSelection() {
		clearColunasSelection();
		clearLinhasSelection();
		layersRedraw();
	}

	function clearColunasSelection() {
		for (var i = 0; i < colunas.length; i++) {
			unhighlightSegmento(colunas[i]);
		}
	}

	function clearLinhasSelection() {
		for (var i = 0; i < linhas.length; i++) {
			unhighlightSegmento(linhas[i]);
		}
	}

	function encontraLimiteSuperior(points) {
		var posicoesY = new Array();
		var posY = points[0].y;

      		if (hasZoom && posY == getZoomUpperY()) {
	            return posY;
        	}

		for (var z = 0; z < linhas.length; z++) {
			var pts2 = linhas[z].getPoints();
			if (pts2[0].y < posY && lineIntersect(points, pts2)) {
				posicoesY.push(pts2[0].y);
			}
		}

		if (posicoesY.length == 0) {
			return minY;
		}
		posicoesY.sort(function(a, b) {
			return b - a;
		});
		return posicoesY[0] + minDistance;
	}

	function encontraLimiteEsquerda(points) {
		var posX = points[0].x;
		var posicoesX = new Array();

		for (var z = 0; z < colunas.length; z++) {
			var pts2 = colunas[z].getPoints();
			if (pts2[0].x < posX && columnIntersect(points, pts2)) {
				posicoesX.push(pts2[0].x);
			}
		}
		if (posicoesX.length == 0) {
			return minX;
		}
		posicoesX.sort(function(a, b) {
			return b - a;
		});
		return posicoesX[0] + minDistance;
	}

	function encontraLimiteInferior(points) {
		var posY = points[0].y;
		var posicoesY = new Array();

       		if (hasZoom && posY == getZoomBottomY()) {
	            return posY;
	        }

		var pts2;
		for (var z = 0; z < linhas.length; z++) {
			var pts2 = linhas[z].getPoints();
			if (pts2[0].y > posY && lineIntersect(points, pts2)) {
				posicoesY.push(pts2[0].y);
			}
		}

		if (posicoesY.length == 0) {
			return maxY;
		}
		posicoesY.sort(function(a, b) {
			return a - b;
		});
		return posicoesY[0] - minDistance;
	}

	function encontraLimiteDireita(points) {
		var posX = points[0].x;
		var posicoesX = new Array();

		for (var z = 0; z < colunas.length; z++) {
			var pts2 = colunas[z].getPoints();
			if (pts2[0].x > posX && columnIntersect(points, pts2)) {
				posicoesX.push(pts2[0].x);
			}
		}
		if (posicoesX.length == 0) {
			return maxX;
		}
		posicoesX.sort(function(a, b) {
			return a - b;
		});
		return posicoesX[0] - minDistance;
	}

	function uneIntercessaoColuna(posX, posY) {
		var pos1;
		var pos3;
		var color;

		for (var z = colunas.length - 1; z >= 0; z--) {
			var points2 = colunas[z].getPoints();
			if (points2[0].x == posX) {
				if (points2[0].y == posY) {
					pos3 = points2[1].y;
					color = colunas[z].getStroke();

					colunas[z].remove();
					colunas.splice(z, 1);
				}
				if (points2[1].y == posY) {
					pos1 = points2[0].y;
					colunas[z].remove();
					colunas.splice(z, 1);
				}
			}
		}

		if (typeof pos1 != 'undefined' && typeof pos3 != 'undefined') {
			var segmento = adicionarSegmento([ posX, pos1, posX, pos3 ]);
			segmento.setStroke(color);
			if (color == highlightColor) segmentosSelecionados.push(segmento);
		}
	}

	function uneIntercessaoLinha(posX, posY) {
		var pos0;
		var pos2;
		var color;

		for (var z = linhas.length - 1; z >= 0; z--) {
			var points2 = linhas[z].getPoints();
			if (points2[0].y == posY) {

				if (points2[0].x == posX) {
					pos2 = points2[1].x;
					color = linhas[z].getStroke();

					linhas[z].remove();
					linhas.splice(z, 1);
				}
				if (points2[1].x == posX) {
					pos0 = points2[0].x;
					linhas[z].remove();
					linhas.splice(z, 1);
				}
			}
		}

		if (typeof pos0 != 'undefined' && typeof pos2 != 'undefined') {
			var segmento = adicionarSegmento([ pos0, posY, pos2, posY ]);
			segmento.setStroke(color);
			if (color == highlightColor) segmentosSelecionados.push(segmento);
		}
	}

	function uneIntercessoes(points) {
		if (isLinha(points)) {
			var posY = points[0].y;
			var intercessoes = encontraIntercessoesVerticais(posY);

			for (var i = 0; i < intercessoes.length; i++) {
				var intercessao = intercessoes[i];
				if (intercessao == getTableMinX() || intercessao == getTableMaxX()) continue;

				if (insideClosedInterval(points[0].x, points[1].x, intercessao)) {
					if (points[0].x == intercessao && temContinuacaoLinha(points[0], points) ||
						points[1].x == intercessao && temContinuacaoLinha(points[1], points)) {
						continue;
					}
					uneIntercessaoColuna(intercessao, posY);
				}
			}
		} else {
			var posX = points[0].x;
			var intercessoes = encontraIntercessoesHorizontais(posX);

			for (var i = 0; i < intercessoes.length; i++) {
				var intercessao = intercessoes[i];
				if (intercessao == getTableMinY() || intercessao == getTableMaxY()) continue;

				if (insideClosedInterval(points[0].y, points[1].y, intercessao)) {
					if (points[0].y == intercessao && temContinuacaoColuna(points[0], points) ||
						points[1].y == intercessao && temContinuacaoColuna(points[1], points)) {
						continue;
					}
					uneIntercessaoLinha(posX, intercessao);
				}
			}
		}
	}

	function temContinuacaoLinha(point, linha) {
		return temContinuacao(linhas, point, linha);
	}

	function temContinuacaoColuna(point, coluna) {
		return temContinuacao(colunas, point, coluna);
	}

	function temContinuacao(segmentos, point, segPoints) {
		for (var i = 0; i< segmentos.length; i++) {
			var points = segmentos[i].getPoints();
			if (!equalsSegmento(points, segPoints) && (equalsPoint(points[0], point) || equalsPoint(points[1], point)))  return true; 		
		}
		return false;
	}

	function filterLines() {

		var zoomMinY = zoom[1] + shiftOnCanvas;
		var zoomMaxY = zoom[3] + shiftOnCanvas;

		for (var i = colunas.length - 1; i >= 0; i--) {
			var points = colunas[i].getPoints();

			if (isBorda(points)) continue;

			var minY = points[0].y;
			if (points[0].y < zoomMinY) {
				minY = zoomMinY;
			}
			var maxY = points[1].y;
			if (points[1].y > zoomMaxY) {
				maxY = zoomMaxY;
			}
			colunas[i].setPoints([points[0].x, minY, points[1].x, maxY]);
		}

		for (var i = linhas.length - 1; i >= 0; i--) {
			var points = linhas[i].getPoints();
			var segInZoom = inZoom(points[0].y);

			// linhas fora do zoom
			if (!segInZoom) {
				removeSegmentoLinha(linhas[i]);
			}
		}
	}

	function segmentoContains(seg1, seg2) {
		if (isMesmaLinha(seg1, seg2)
			&& insideLineInterval(seg1, seg2)) {
			return true;
		}
		if (isMesmaColuna(seg1, seg2)
			&& insideColumnInterval(seg1, seg2)) {
			return true;
		}
		return false;
	}

	function insideLineInterval(seg1, seg2) {
		return seg1[1].x >= seg2[1].x && seg1[0].x <= seg2[0].x;
	}

	function insideColumnInterval(seg1, seg2) {
		return seg1[1].y >= seg2[1].y && seg1[0].y <= seg2[0].y;
	}

	function lineIntersect(seg1, seg2) {
		return seg2[0].x < seg1[1].x && seg1[0].x < seg2[1].x;
	}

	function columnIntersect(seg1, seg2) {
		return seg2[0].y < seg1[1].y && seg1[0].y < seg2[1].y;
	}

	function insideInterval(init, final, element) {
		return element > init && element < final;
	}

	function insideClosedInterval(init, final, element) {
		return element >= init && element <= final;
	}

	function findContinuacaoDaLinha(ptsLinha) {
		for (var i = 0; i < linhas.length; i++) {
			var points = linhas[i].getPoints();
			
			if (points[0].y == ptsLinha[0].y && points[1].x == ptsLinha[0].x) {
				return i;
			}
		}
		return -1;
	}

	function findContinuacaoDaColuna(ptsLinha) {
		for (var i = 0; i < colunas.length; i++) {
			var points = colunas[i].getPoints();
			
			if (points[0].x == ptsLinha[0].x && points[1].y == ptsLinha[0].y) {
				return i;
			}
		}
		return -1;
	}

	function initGrid(taskInfo, minCanvasWidth, minCanvasHeight, serverName) {
		initVariables(taskInfo, serverName);

		var isLastAnswer = typeof taskInfo.last_answer != "undefined";
		var matrizDePontos = loadMatrizDePontos(taskInfo, isLastAnswer);

		if (typeof stage != "undefined") {
			$(".kineticjs-content").remove();
		}
		createStage(matrizDePontos, minCanvasWidth, minCanvasHeight, isLastAnswer);
	}

	function loadMatrizDePontos(taskInfo, isLastAnswer) {
		var matrizDePontos = new Array();

		if (isLastAnswer) {
			var lastAnswer = $.parseJSON(taskInfo.last_answer);
			matrizDePontos = matrizDePontos.concat(lastAnswer.linhas);
			matrizDePontos = matrizDePontos.concat(lastAnswer.colunas);
			maxX = lastAnswer.maxX;
			maxY = lastAnswer.maxY;
			minX = 0;
			minY = 0;

		} else {
			matrizDePontos = taskInfo.coords;
			var leftX, upperY, rightX, bottomY, arr;

			for (var i = 0; i < matrizDePontos.length; i++) {
				arr = matrizDePontos[i];
				leftX = arr[0];
				if (leftX < minX) minX = leftX;
				upperY = arr[1];
				if (upperY < minY) minY = upperY;
				rightX = arr[2];
				if (rightX > maxX) maxX = rightX;
				bottomY = arr[3];
				if (bottomY > maxY) maxY = bottomY;
			}
		}

		minX = minX + shiftOnCanvas;
		minY = minY + shiftOnCanvas;
		maxX = maxX + shiftOnCanvas;
		maxY = maxY + shiftOnCanvas;

		return matrizDePontos;
	}

	function createStage(matrizDePontos, minCanvasWidth, minCanvasHeight, isLastAnswer) {
		var widthCanvas = getTableMaxX();
		var heightCanvas = getTableMaxY();

		if ((widthCanvas + shiftOnCanvas) < minCanvasWidth) {
			widthCanvas = minCanvasWidth;
		} else {
			// pad lateral
			widthCanvas += shiftOnCanvas;
		}

		if ((heightCanvas + shiftOnCanvas) < minCanvasHeight) {
			heightCanvas = minCanvasHeight;
		} else {
			// pad inferior
			heightCanvas += shiftOnCanvas;
		}

		stage = new Kinetic.Stage({
			container : 'canvas-container',
			width : widthCanvas,
			height : heightCanvas,
		});

                stage.on("mousemove", function(evt){
			handleMouseMoveEvent(evt);
                });

		var imageObj = new Image();
		imageObj.src = img_url;
		imageObj.onload = function() {
			var tabela = new Kinetic.Image({
				x : shiftOnCanvas,
				y : shiftOnCanvas,
				image : imageObj,
				width : getTableMaxX() - shiftOnCanvas,
				height : getTableMaxY() - shiftOnCanvas
			});

			imageLayer.add(tabela);
			tabela.moveToBottom();

			stage.add(imageLayer);
			stage.add(colunasLayer);
			stage.add(linhasLayer);
			stage.add(pointsLayer);
			stage.add(selectionLayer);

			if (hasZoom) {
				adicionarFocoZoom(zoom);
		 		stage.add(layerZoom);
			}

			loadGrid(matrizDePontos, isLastAnswer);
		};
	}

	function loadGrid(matrizDePontos, isLastAnswer) {

		for (var i = 0; i < matrizDePontos.length; i++) {
			var arr = matrizDePontos[i];
			var leftX = arr[0] + shiftOnCanvas;
			var upperY = arr[1] + shiftOnCanvas;
			var rightX = arr[2] + shiftOnCanvas;
			var bottomY = arr[3] + shiftOnCanvas;

			if (isLastAnswer) {
				adicionarSegmento([{'x': leftX, 'y': upperY}, {'x': rightX, 'y': bottomY}]);
			} else {
				var cellLines = new Array();
				cellLines.push([{'x': leftX, 'y': upperY}, {'x': rightX, 'y': upperY}]);
				cellLines.push([{'x': leftX, 'y': upperY}, {'x': leftX, 'y': bottomY}]);
				cellLines.push([{'x': leftX, 'y': bottomY}, {'x': rightX, 'y': bottomY}]);
				cellLines.push([{'x': rightX, 'y': upperY}, {'x': rightX, 'y': bottomY}]);

				adicionaSegmentosDaCelula(cellLines);
			}
		}

		if (!isLastAnswer && hasZoom) filterLines();
		layersRedraw();
	}

	function adicionaSegmentosDaCelula(cellLines) {
		for (var z = 0; z < cellLines.length; z++) {
			var posLinha = cellLines[z];
			var indexSegmento = findSegmentoThatContains(posLinha);

			if (indexSegmento == -1) {
				if (isLinha(posLinha)) {
					indexContinuacao = findContinuacaoDaLinha(posLinha);

					if (indexContinuacao == -1) {
						adicionarSegmento(posLinha);
					} else {
						var continuacao = linhas[indexContinuacao];
						var points = continuacao.getPoints();
						continuacao.remove();
						linhas.splice(indexContinuacao, 1);
						adicionarSegmento([{'x': points[0].x, 'y': points[0].y}, {'x': posLinha[1].x, 'y': posLinha[1].y}]);
					}
				} else {
					indexContinuacao = findContinuacaoDaColuna(posLinha);

					if (indexContinuacao == -1) {
						adicionarSegmento(posLinha);
					} else {
						var continuacao = colunas[indexContinuacao];
						var points = continuacao.getPoints();
						continuacao.remove();
						colunas.splice(indexContinuacao, 1);
						adicionarSegmento([{'x': points[0].x, 'y': points[0].y}, {'x': posLinha[1].x, 'y': posLinha[1].y}]);
					}
				}
			}
		}
	}

	// Event Handling
	document.onkeydown = function (evt) { 
		if (typeof evt.keyCode != "undefined" && evt.keyCode == 46) {
			handleRemoveToolEvent();
		}
	};

	function handleAreaSelectionToolEvent() {
		resetToolBar();
		enableAreaSelectionTool(true);
	}

	function enableAreaSelectionTool(enable) {
		if (enable) {
			$('#button_area').addClass('active');
			document.body.style.cursor = "crosshair";
		} else {
			$('#button_area').removeClass('active');
		}
		toolBarState = "AREA";
	}

	function handleSelectionToolEvent() {
		resetToolBar();
		enableSelectionTool(true);
	}

	function enableSelectionTool(enable) {
		if (enable) {
			$('#button_select').addClass('active');
			document.body.style.cursor = "default";
		} else {
			$('#button_select').removeClass('active');
		}
		toolBarState = "SELECTION";
	}

	function handleAddToolEvent() {
		resetToolBar();
		enableAddTool(true);
	}

	function enableAddTool(enable) {
		if (enable) {
			document.body.style.cursor = "crosshair";
			$('#button_add').addClass('active');			
		} else {
			$('#button_add').removeClass('active');
		}
		toolBarState = "ADD";
	}

	function handleSplitToolEvent() {
		resetToolBar();
		enableSplitTool(true);
	}

	function enableSplitTool(enable) {
		if (enable) {
			document.body.style.cursor = splitToolCursor;
			$('#button_split').addClass('active');
		} else {
			$('#button_split').removeClass('active');
		}
		toolBarState = "SPLIT";
	}

	function isAddToolActive() {
		return toolBarState == "ADD";
	}

	function isSplitToolActive() {
		return toolBarState == "SPLIT";
	}

	function isSelectionToolActive() {
		return toolBarState == "SELECTION";
	}

	function isAreaToolActive() {
		return toolBarState == "AREA";
	}

	function hasSelectedSegment() {
		return segmentosSelecionados.length != 0;
	}

	function handleRemoveToolEvent() {

		if (!hasSelectedSegment()) {
			alert("Nenhum segmento está selecionado.");
			return;
		}

		var sucess = removeSelectedSegmentos();
		if (!sucess) alert("Não é possível remover este(s) segmento(s).");
		
		resetSelecao();
		layersRedraw();
	}

	$('body').on('mousedown', function(e) {
		handleMouseDownEvent(e);
	});

	function handleMouseDownEvent(evt) {
		isMouseDown = true;

		if (!isRightMouseClick(evt)) return;

		if (isAddToolActive() && !isMouseOverAnElement()) {
			desenhandoSegmento = true;
		}
	}

	function isMouseOverAnElement() {
		return mouseOverQueue.length != 0;
	}

	function getMouseOverElement() {
		return mouseOverQueue[0];
	}

	function separaSegmento(mouseX, mouseY) {
		resetSelecao();

		if (!isMouseOverAnElement()) {
			return;
		}

		var segmento = getMouseOverElement();
		var segPoints = segmento.getPoints();
		var newSeg;

		if (isLinha(segPoints)) {

			var posY = segPoints[0].y;
			var intercessoes = encontraIntercessoesVerticais(posY);
			var closest = closestIntersection(intercessoes, mouseX, segPoints[0].x, segPoints[1].x);

			if (typeof closest != "undefined") {
				segmento.setPoints([segPoints[0].x, posY, closest, posY]);
				newSeg = adicionarSegmento([closest, posY, segPoints[1].x, posY]);
				selecionaSegmento(newSeg);

				var newSegPoints = newSeg.getPoints();
				if (insideInterval(newSegPoints[0].x, newSegPoints[1].x, mouseX)) {
					mouseOverQueue.shift();
					mouseOverQueue.push(newSeg);
				}
			}
		} else {

			var posX = segPoints[0].x;
			var intercessoes = encontraIntercessoesHorizontais(posX);
			var closest = closestIntersection(intercessoes, mouseY, segPoints[0].y, segPoints[1].y);

			if (typeof closest != "undefined") {
				segmento.setPoints([posX, segPoints[0].y, posX, closest]);
				newSeg = adicionarSegmento([posX, closest, posX, segPoints[1].y]);
				selecionaSegmento(newSeg);

				var newSegPoints = newSeg.getPoints();
				if (insideInterval(newSegPoints[0].y, newSegPoints[1].y, mouseY)) {
					mouseOverQueue.shift();
					mouseOverQueue.push(newSeg);
				}
			}
		}
		selecionaSegmento(segmento);
	}

	function closestIntersection(intercessoes, pos, limInf, limSup) {
		var closestDist = isLinha ? MAX_X : MAX_Y;
		var closest;

		for (var i = 0; i < intercessoes.length; i++) {
			var intercessao = intercessoes[i];

			if (intercessao <= limInf || intercessao >= limSup) continue;

			var dist = Math.abs(pos - intercessao);
			if (dist < closestDist) {
				closestDist = dist;
				closest = intercessao;
			}
		}
		return closest;
	}

	function isRightMouseClick(evt) {
		return evt.which == 1;
	}

	function isToolBarClick(evt) {
		return evt.target.tagName == "BUTTON" || evt.target.tagName == "IMG" || evt.target.tagName == "I";
	}

	function handleMouseUpEvent(evt) {

		isMouseDown = false;
		desenhandoSegmento = false;

		if (!isRightMouseClick(evt) || isToolBarClick(evt)) return;

		if (isSplitToolActive()) {
			var posX = getMousePosX(evt);
			var posY = getMousePosY(evt);
			separaSegmento(posX, posY);
			return;
		}

		if (isAddToolActive() && typeof novoSegmento != 'undefined') {
			var points = novoSegmento.getPoints();
			novoSegmento.remove();
			novoSegmento = undefined;
			criaNovoSegmento(evt, points);
			return;
		}

		if (isAreaToolActive() && typeof selectionArea != 'undefined') {
			var initPos = selectionArea.getAbsolutePosition();
			var finalPosX = initPos.x + selectionArea.getWidth();
			var finalPosY = initPos.y + selectionArea.getHeight();

			selectionArea.remove();
			selectionArea = undefined;
			selectArea(initPos.x, initPos.y, finalPosX, finalPosY);
			return;
		}

		if ((isSelectionToolActive() || isAddToolActive()) && isMouseOverAnElement()) {
			clickOnSegmento(evt, getMouseOverElement());
			return;
		}

		resetSelecao();
		clearSelection();
	}

	function selectArea(initPosX, initPosY, finalPosX, finalPosY) {
		clearSelection();
		var maxX, maxY, minX, minY;

		if (initPosX > finalPosX) {
			maxX = initPosX;
			minX = finalPosX;
		} else {
			maxX = finalPosX;
			minX = initPosX;
		}

		if (initPosY > finalPosY) {
			maxY = initPosY;
			minY = finalPosY;
		} else {
			maxY = finalPosY;
			minY = initPosY;
		}

		var area = [minX, minY, maxX, maxY];
		for (var i = 0; i < linhas.length; i++) {
			var points = linhas[i].getPoints();
			if (!isBorda(points) && isSegmentInArea(points, area)) {
				highlightSegmento(linhas[i]);
				segmentosSelecionados.push(linhas[i]);
			}
		}
		for (var i = 0; i < colunas.length; i++) {
			var points = colunas[i].getPoints();
			if (!isBorda(points) && isSegmentInArea(points, area)) {
				highlightSegmento(colunas[i]);
				segmentosSelecionados.push(colunas[i]);
			}
		}
		layersRedraw();
	}

	function isSegmentInArea(points, area) {
		return isPosInArea(points[0].x, points[0].y, area) && isPosInArea(points[1].x, points[1].y, area);
	}

	function isPosInArea(posX, posY, area) {
		var minX = area[0];
		var minY = area[1];
		var maxX = area[2];
		var maxY = area[3];
		return (posX >= minX && posX <= maxX) && (posY >= minY && posY <= maxY);
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

	function criaNovoSegmento(evt, points) {

		var deltaX = Math.abs(points[1].x - points[0].x);
		var deltaY = Math.abs(points[1].y - points[0].y);

		if (deltaX == 0 && deltaY == 0) {
			layersRedraw();
		 	return;
		}

		var newSeg;

		if (deltaY > deltaX) {
			var posX = points[0].x;
			var initY = points[0].y;
			points[1].x = points[0].x;
			var finalY = points[1].y;
			newSeg = criarNovaColuna(posX, initY, finalY);
		} else {
			var posY = points[0].y;
			var initX= points[0].x;
			points[1].y = points[0].y;
			var finalX = points[1].x;
			newSeg = criarNovaLinha(posY, initX, finalX);
		}

		if (typeof newSeg != "undefined") {
			clickOnSegmento(evt, newSeg);
		}
		layersRedraw();
	}

	function isMousePosOffBorders(pos) {
		return (pos.x <  getTableMinX() || pos.x >  getTableMaxX()) ||
			(pos.y <  getTableMinY() || pos.y >  getTableMaxY());
	}

	function handleMouseMoveEvent(evt) {

		if (isAreaToolActive()) {
			document.body.style.cursor = "crosshair";
		}

		if (!isMouseDown) return;

		if (isAddToolActive() && desenhandoSegmento) {
			var mousePos = stage.getMousePosition();

			if (isMousePosOffBorders(mousePos)) return;

			if (typeof novoSegmento == 'undefined') {
				var kineticLine = new Kinetic.Line({points: [mousePos.x, mousePos.y, mousePos.x, mousePos.y]});
				novoSegmento = new Segmento(kineticLine, pointsLayer);
				highlightSegmento(novoSegmento);
				linhasLayer.add(kineticLine); 
			}

			var newX = mousePos.x;
			var newY = mousePos.y;

			var points =  novoSegmento.getPoints();
			novoSegmento.setPoints([points[0].x, points[0].y, newX, newY]);
			layersRedraw();
		}

		if (isAreaToolActive()) {
			var mousePos = stage.getMousePosition();

			if (typeof selectionArea == 'undefined') {
				selectionArea = new Kinetic.Rect({
					x: mousePos.x,
					y: mousePos.y,
					width: 0,
					height: 0,
					fillEnabled: false,
				        stroke: 'black',
				        dashArray: [2],
				        strokeWidth: 2
				      });
				selectionLayer.add(selectionArea);
			}

			var newX = mousePos.x;
			var newY = mousePos.y;

			var pos = selectionArea.getAbsolutePosition();

			var deltaX = newX - pos.x;
			var deltaY = newY - pos.y;

			selectionArea.setWidth(deltaX);
			selectionArea.setHeight(deltaY);
			selectionLayer.moveToTop();	
			layersRedraw();
		}
	}

	function clickOnSegmento(evt, seg) {
		var segPoints = seg.getPoints();
		if (isBorda(segPoints)) return;

		if (isMouseOverAnElement()) {
			document.body.style.cursor = "move";
		}

		if (!evt.shiftKey) {
			resetSelecao();
		}
		selecionaSegmento(seg);
	}

	function selecionaSegmento(seg) {
		highlightSegmento(seg);
		segmentosSelecionados.push(seg);
		layersRedraw();
	}

	function highlightSegmento(seg) {
		setStrokeOverLine(seg, highlightColor);
	}

	function unhighlightSegmento(seg) {
		seg.setStroke(unhighlightColor);
	}

	function setStrokeOverLine(seg, color) {
		var points = seg.getPoints();

		if (isColuna(points) && !isBorda(points)) {
			seg.setStroke(color);
			colunasLayer.moveToTop();
		} else if (isLinha(points) && !isBorda(points)) {
			seg.setStroke(color);
			linhasLayer.moveToTop();
		}
		
		pointsLayer.moveToTop();
		if (hasZoom) layerZoom.moveToTop();
	}

	function removeSegmento(segmento) {
		var points = segmento.getPoints();

		if (!isBorda(points)) {
			if (isColuna(points)) {
				return removeSegmentoColuna(segmento);
			} else if (isLinha(points) && inZoom(points[1].y) && inZoom(points[0].y)) {
				return removeSegmentoLinha(segmento);
			}
		}
	}

	function removeSelectedSegmentos() {
		var removedAny = false;
		var failed = false;
		return recursiveDeletion(removedAny, failed);
	}

	function recursiveDeletion(removedAny, failed) {
		
		if (segmentosSelecionados.length == 0 || failed) return removedAny;

		var allFailed = true;
		for (var i = segmentosSelecionados.length - 1; i >= 0; i--) {
			var points = segmentosSelecionados[i].getPoints();
			var segmento = getSegmento(points);

			if (typeof segmento == "undefined") {
				segmentosSelecionados.splice(i, 1);
				continue;
			}

			var success = removeSegmento(segmento);
			allFailed = allFailed && !success;

			if (success) {
				segmentosSelecionados.splice(i, 1);
				removedAny = true;
			}
		}
		return recursiveDeletion(removedAny, allFailed);
	}
	
	function removeSegmentoColuna(segmento) {
		var segPoints = segmento.getPoints();

		if (!validaRemocao(segPoints)) {
			return false;
		}

		for (var i = colunas.length - 1; i >= 0; i--) {
			var points2 = colunas[i].getPoints();
			if (equalsSegmento(segPoints, points2)) {
				colunas[i].remove();
				colunas.splice(i, 1);

				uneIntercessoes(points2);
				break;
			}
		}
		return true;
	}

	function removeSegmentoLinha(segmento) {
		var segPoints = segmento.getPoints();

		if (!validaRemocao(segPoints)) {
			return false;
		}

		for (var i = linhas.length - 1; i >= 0; i--) {
			var points2 = linhas[i].getPoints();
			if (equalsSegmento(segPoints, points2)) {
				linhas[i].remove();
				linhas.splice(i, 1);

				if (hasZoom && isLinhaInZoomBorder(segPoints)) break;
				uneIntercessoes(points2);
				break;
			}
		}
		return true;
	}

	function isLinhaInZoomBorder(segPoints) {
		return segPoints[0].y == (zoom[1] + shiftOnCanvas) ||
					segPoints[0].y == (zoom[3] + shiftOnCanvas);
	}

	function validaRemocao(segPoints) {

		if (isLinha(segPoints)) {

			if (!temColunasDelimitando(segPoints)) return false;

			if (hasZoom && isLinhaInZoomBorder(segPoints)) return true;

			// checa se as colunas que tocam a linha tem continuacao
			var posY = segPoints[0].y;
			for (var i = 0; i < colunas.length; i++) {
				var points = colunas[i].getPoints();
				if (!insideClosedInterval(segPoints[0].x, segPoints[1].x, points[0].x)) continue;

				if (points[0].y == posY && !temContinuacaoColuna(points[0], points)) {
					return false;
				} else if (points[1].y == posY && !temContinuacaoColuna(points[1], points)) {
					return false;
				}
			}
		} else {

			if (!temLinhasDelimitando(segPoints)) return false;

			// checa se as linhas que tocam a coluna tem continuacao
			var posX = segPoints[0].x;
			for (var i = 0; i < linhas.length; i++) {
				var points = linhas[i].getPoints();
				if (!insideClosedInterval(segPoints[0].y, segPoints[1].y, points[0].y)) continue;

				if (points[0].x == posX && !temContinuacaoLinha(points[0], points)) {
					return false;
				} else if (points[1].x == posX && !temContinuacaoLinha(points[1], points)) {
					return false;
				}
			}
		}
		return true;
	}

	function equalsSegmento(points, points2) {
		return points[0].x == points2[0].x && points[0].y == points2[0].y && 
			points[1].x == points2[1].x && points[1].y == points2[1].y;
	}

	function equalsPoint(point1, point2) {
		return point1.x == point2.x && point1.y == point2.y;
	}

	function findSegmentoColuna(points) {
		for (var i = 0; i < colunas.length; i++) {
			var points2 = colunas[i].getPoints();
			if (equalsSegmento(points, points2)) return i;

		}
		return -1;
	}

	function findSegmentoLinha(points) {
		for (var i = 0; i < linhas.length; i++) {
			var points2 = linhas[i].getPoints();
			if (equalsSegmento(points, points2)) return i;

		}
		return -1;
	}

	function getSegmento(segPoints) {
		return isLinha(segPoints) ? linhas[findSegmentoLinha(segPoints)] : colunas[findSegmentoColuna(segPoints)];
	}

	function findSegmentoColunaThatContains(points) {
		for (var i = 0; i < colunas.length; i++) {
			var points2 = colunas[i].getPoints();
			if (segmentoContains(points2, points)) return i;
		}
		return -1;
	}

	function findSegmentoLinhaThatContains(points) {
		for (var i = 0; i < linhas.length; i++) {
			var points2 = linhas[i].getPoints();
			if (segmentoContains(points2, points)) return i;
		}
		return -1;
	}

	function findSegmentoThatContains(points) {
		if (isColuna(points)) {
			return findSegmentoColunaThatContains(points);
		} else {
			return findSegmentoLinhaThatContains(points);
		}
	}

	function layersRedraw() {
		colunasLayer.draw();
		linhasLayer.draw();
		pointsLayer.draw();
		selectionLayer.draw();
	}

	function getGridLinesAnswer() {
		linhas.sort(sortLinesFunction);
		colunas.sort(sortColumnsFunction);

		var linhasASalvar = new Array();
		var colunasASalvar = new Array();

		for (var i = 0; i < linhas.length; i++){
			var linha = linhas[i].getPoints();
		        var segmento = [ linha[0].x - shiftOnCanvas, linha[0].y - shiftOnCanvas, linha[1].x - shiftOnCanvas, linha[1].y - shiftOnCanvas];
			linhasASalvar.push(segmento);
		}

		for (var i = 0; i < colunas.length; i++){
			var coluna = colunas[i].getPoints();
			var segmento = [ coluna[0].x - shiftOnCanvas, coluna[0].y - shiftOnCanvas, coluna[1].x - shiftOnCanvas, coluna[1].y - shiftOnCanvas];
			colunasASalvar.push(segmento);
		}

		return JSON.stringify({'img_url': img_url, 'linhas' : linhasASalvar, 'colunas' : colunasASalvar,
				 'maxX' : getTableMaxX() - shiftOnCanvas, 'maxY': getTableMaxY() - shiftOnCanvas});
	}

	function clearCanvas() {
		stage.removeChildren();
		stage.remove();
	}

	function getTableMaxX() {
		return maxX;
	}

	function getTableMaxY() {
		return maxY;
	}

	function getTableMinX() {
		return minX;
	}

	function getTableMinY() {
		return minY;
	}

	function getCanvasWidth() {
		return stage.getWidth();
	}

	function getCanvasHeight() {
		return stage.getHeight();
	}
