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

	var selecaoAtivada;
	var selecaoAreaAtivada;
	var adicaoAtivada;
	var separarAtivado;

	var selecionandoArea;
	var selecionandoSegmento;
	var desenhandoSegmento;

	var splitToolCursor;
	var novoSegmento;
	var selectionArea;
	var mouseOverElement;

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

		resetToolBar();
		enableSelectionTool(true);

		hasZoom = false;
		imageLayer = new Kinetic.Layer();
		linhasLayer = new Kinetic.Layer();
		colunasLayer = new Kinetic.Layer();
		pointsLayer = new Kinetic.Layer();
		selectionLayer = new Kinetic.Layer();

		segWidth = 2.5
		// distancia minima entre linhas e colunas (em pixels)
		minDistance = 5;
		// ajuste para que as linhas nas bordas aparecam completamente
		shiftOnCanvas = 25;
		unhighlightColor = "#CD3300";
		highlightColor = "#339ACD";

		splitToolCursor = "url('" + serverName + "/images/split_tool.png') 10 8, auto";

		hasZoom = taskInfo.hasZoom;
		img_url = taskInfo.img_url;

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

		selecionandoArea = false;
		selecionandoSegmento = false;
		desenhandoSegmento = false;
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
		for (var i = 0; i < colunas.length; i++) {
			var points = colunas[i].getPoints();
			if (points[0].y == posY) {
				colunas[i].setPoints([points[0].x, newPosY, points[1].x,  points[1].y]);
			} else if (points[1].y == posY) {
				colunas[i].setPoints([points[0].x, points[0].y, points[1].x, newPosY]);
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
		var toquesNaExtremidade = 0;

		for (var i = 0; i < linhas.length; i++) {
			var segPoints = linhas[i].getPoints();
			// inicio da coluna na mesma altura da linha
			if (colPoints[0].y == segPoints[0].y) {
				if (insideInterval(segPoints[0].x, segPoints[1].x, colX)) {
					cruzandoComeco = true;
				} else if (segPoints[0].x == colX || segPoints[1].x == colX) {
					toquesNaExtremidade++;
				}
			// final da coluna na mesma altura da linha
			} else if (colPoints[1].y == segPoints[0].y) {
				
				if (insideInterval(segPoints[0].x, segPoints[1].x, colPoints[0].x)) {
					cruzandoFim = true;
				} else if (segPoints[0].x == colX || segPoints[1].x == colX) {
					toquesNaExtremidade++;
				}
			}
		}
		return (cruzandoComeco && cruzandoFim) || (toquesNaExtremidade != 0 && toquesNaExtremidade % 2 == 0);
	}

	function temColunasDelimitando(linPoints) {
		var cruzandoComeco = false;
		var cruzandoFim = false;
		var linY = linPoints[0].y;
		var toquesNaExtremidade = 0;

		for (var i = 0; i < colunas.length; i++) {
			var segPoints = colunas[i].getPoints();

			// inicio da linha na mesma distancia da coluna
			if (linPoints[0].x == segPoints[0].x) {
				if (insideInterval(segPoints[0].y, segPoints[1].y, linY)) {
					cruzandoComeco = true
				} else if (segPoints[0].y == linY || segPoints[1].y == linY) {
					toquesNaExtremidade++;
				}
			// final da linha na mesma distancia da coluna
			} else if (linPoints[1].x == segPoints[0].x) {
				if (insideInterval(segPoints[0].y, segPoints[1].y, linY)) {
					cruzandoFim = true;
				} else if (segPoints[0].y == linY || segPoints[1].y == linY) {
					toquesNaExtremidade++;
				}
			}
		}
		return (cruzandoComeco && cruzandoFim) || (toquesNaExtremidade != 0 && toquesNaExtremidade % 2 == 0);
	}

	function atualizaLinhasPerpendiculares(segPoints, newPosX) {
		var posX = segPoints[0].x;
		for (var i = 0; i < linhas.length; i++) {
			var points = linhas[i].getPoints();
			if (points[0].x == posX) {
				linhas[i].setPoints([newPosX, points[0].y, points[1].x,  points[1].y]);
			} else if (points[1].x == posX) {
				linhas[i].setPoints([points[0].x, points[0].y, newPosX, points[1].y]);
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
			dragBoundFunc: function(pos, event) {
				if (typeof event == 'undefined' || separarAtivado) return {x : this.getAbsolutePosition().x, y : this.getAbsolutePosition().y};

				if (selecionandoSegmento) {
					clearSelection();
					selecionandoSegmento = false;
				}

				var points = this.getPoints();
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

				highlightSegmento(seg);
				document.body.style.cursor = "move";
				layersRedraw();
				return {x : this.getAbsolutePosition().x, y : this.getAbsolutePosition().y};
			}
		});

		// refatorar condicoes booleanas
		kineticLine.on("mouseover touchstart",
				function() {

					var points = this.getPoints();

					if (isBorda(points) || selecaoAreaAtivada) return;

					mouseOverElement = getSegmento(points);

					if (selecionandoSegmento && this.getStroke() == highlightColor) {
						document.body.style.cursor = "move";
						return;
					} 

					if (!separarAtivado) {
						document.body.style.cursor = "pointer";
					}

					if (selecionandoSegmento) {
						return;	
					}

					highlightSegmento(mouseOverElement);
					layersRedraw();
		});

		kineticLine.on('mouseout touchend', function(evt) {

			mouseOverElement = undefined;

			if (selecaoAreaAtivada) return;

			if (adicaoAtivada) document.body.style.cursor = "crosshair";

			if (!adicaoAtivada && !separarAtivado && !evt.shiftKey) {
				document.body.style.cursor = "default";
			}

			if (selecionandoSegmento) return;

			var points = this.getPoints();
			if (isColuna(points)) {
				clearColunasSelection();
			} else {
				clearLinhasSelection();
			}
			layersRedraw();
		});

		var segmento = new Segmento(kineticLine, pointsLayer);

		if (isLinha(segmento.getPoints())) {
			linhas.push(segmento);
			linhasLayer.add(kineticLine);
		} else {
			colunas.push(segmento);
			colunasLayer.add(kineticLine);
		}
		layersRedraw();
		return segmento;
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
		}
	}

	function uneIntercessoes(points) {
		var pos0, pos1;

		if (isLinha(points)) {
			pos0 = points[0].x;
			pos1 = points[1].x;
			var posY = points[0].y;

			if (!temContinuacaoLinha(points[0], points)) {
				uneIntercessaoColuna(pos0, posY);
			}
			if (!temContinuacaoLinha(points[1], points)) {
				uneIntercessaoColuna(pos1, posY);
			}
		} else {

			pos0 = points[0].y;
			pos1 = points[1].y;
			var posX = points[0].x;

			if (!temContinuacaoColuna(points[0], points)) {
				uneIntercessaoLinha(posX, pos0);
			}
			if (!temContinuacaoColuna(points[1], points)) {
				uneIntercessaoLinha(posX, pos1);
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

	function getNearColumns(colPoints) {
		var columns = new Array();
		for (var i = 0; i < colunas.length; i++) {
			var pts = colunas[i].getPoints();
			var ptsPosX = pts[0].x;
			if (!isMesmaColuna(colPoints, pts) && insideInterval(ptsPosX - minDistance, ptsPosX + minDistance, colPoints[0].x)) {
				columns.push(colunas[i]);
			}
		}
		return columns;
	}

	function getNearLines(linPoints) {
		var lines = new Array();
		for (var i = 0; i < linhas.length; i++) {
			var pts = linhas[i].getPoints();
			var ptsPosY = pts[0].y;
			if (!isMesmaLinha(linPoints, pts) && insideInterval(ptsPosY - minDistance, ptsPosY + minDistance, linPoints[0].y)) {
				lines.push(linhas[i]);
			}
		}
		return lines;
	}

	function filterRectangles() {
		// remove colunas com uma distancia minima
		for (var i = colunas.length - 1; i >= 0; i--) {
			var points = colunas[i].getPoints();

			var nearColumns = getNearColumns(points);
			for (var z = 0; z < nearColumns.length; z++) {
				removeSegmentoColuna(nearColumns[z]);
			}
		}

		// remove linhas com uma distancia minima
		for (var i = linhas.length - 1; i >= 0; i--) {
			var points = linhas[i].getPoints();

			// linhas fora do zoom
			if (hasZoom && !inZoom(points[0].y)) {
				removeSegmentoLinha(linhas[i]);
				continue;
			}

			var nearLines = getNearLines(points);
			for (var z = 0; z < nearLines.length; z++) {
				removeSegmentoLinha(nearLines[z]);
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

	function initGrid(taskInfo, maxCanvasWidth, maxCanvasHeight, serverName) {
		initVariables(taskInfo, serverName);

		var isLastAnswer = typeof taskInfo.last_answer != "undefined";
		var matrizDePontos = loadMatrizDePontos(taskInfo, isLastAnswer);

		if (typeof stage != "undefined") {
			$(".kineticjs-content").remove();
		}

		createStage(matrizDePontos, maxCanvasWidth, maxCanvasHeight, isLastAnswer);
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

	function createStage(matrizDePontos, maxCanvasWidth, maxCanvasHeight, isLastAnswer) {
		var widthCanvas = getTableMaxX();
		var heightCanvas = getTableMaxY();

		if ((widthCanvas + shiftOnCanvas) < maxCanvasWidth) {
			widthCanvas = maxCanvasWidth;
		} else {
			// pad lateral
			widthCanvas += shiftOnCanvas;
		}

		if ((heightCanvas + shiftOnCanvas) < maxCanvasHeight) {
			heightCanvas = maxCanvasHeight;
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

			// add the shape to the layer
			imageLayer.add(tabela);
			tabela.moveToBottom();

			// add the layer to the stage
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
				continue;
			}

			var novasLinhas = new Array();

			novasLinhas.push([{'x': leftX, 'y': upperY}, {'x': rightX, 'y': upperY}]);
			novasLinhas.push([{'x': leftX, 'y': upperY}, {'x': leftX, 'y': bottomY}]);
			novasLinhas.push([{'x': leftX, 'y': bottomY}, {'x': rightX, 'y': bottomY}]);
			novasLinhas.push([{'x': rightX, 'y': upperY}, {'x': rightX, 'y': bottomY}]);

			for (var z = 0; z < novasLinhas.length; z++) {
				var posLinha = novasLinhas[z];
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
		filterRectangles();
	}

	// Event Handling
	document.onkeydown = function (evt) { 
		if (typeof evt.keyCode != "undefined" && evt.keyCode == 46) {
			handleRemoveToolEvent();
		}

		if (evt.shiftKey) {
			document.body.style.cursor = "pointer";
		}
	};

	document.onkeyup = function (evt) { 
		if (typeof evt.keyCode != "undefined" && evt.keyCode == 16){
			document.body.style.cursor = "default";
		}
	}

	// Toolbar
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
		selecaoAreaAtivada = enable;
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
		selecaoAtivada = enable;
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
		adicaoAtivada = enable;
	}

	function handleSplitToolEvent() {
		resetToolBar();
		clearSelection();
		enableSplitTool(true);
	}

	function enableSplitTool(enable) {
		if (enable) {
			document.body.style.cursor = splitToolCursor;
			$('#button_split').addClass('active');
		} else {
			$('#button_split').removeClass('active');
		}
		separarAtivado = enable;
	}

	function handleRemoveToolEvent() {

		var result = removeSelectedSegmentos();

		if (!result.selectedAny) {
			alert("Nenhum segmento está selecionado.");
		} else if (!result.removedAny) {
			alert("Não é possível remover este(s) segmento(s).");
		}
		
		// substituir por metodo
		selecionandoSegmento = false;
	}

	$('body').on('mousedown', function(e) {
		handleMouseDownEvent(e);
	});

	function handleMouseDownEvent(evt) {
		if (evt.which != 1) return;

		if (adicaoAtivada && !isMouseOverAnElement()) {
			desenhandoSegmento = true;
		}

		if (selecaoAreaAtivada) {
			selecionandoArea = true;
		}
	}

	function isMouseOverAnElement() {
		return typeof mouseOverElement != "undefined";
	}

	function separaSegmento(segmento, mouseX, mouseY) {
		
		clearSelection();
		var segPoints = segmento.getPoints();
		var newSeg;

		if (isLinha(segPoints)) {

			var posY = segPoints[0].y;
			var intercessoes = encontraIntercessoesVerticais(posY);
			var closest = closestIntersection(intercessoes, mouseX, segPoints[0].x, segPoints[1].x);

			if (typeof closest != "undefined") {
				segmento.setPoints([segPoints[0].x, posY, closest, posY]);
				newSeg = adicionarSegmento([closest, posY, segPoints[1].x, posY]);
				highlightSegmento(newSeg);
			}
		} else {

			var posX = segPoints[0].x;
			var intercessoes = encontraIntercessoesHorizontais(posX);
			var closest = closestIntersection(intercessoes, mouseY, segPoints[0].y, segPoints[1].y);

			if (typeof closest != "undefined") {
				segmento.setPoints([posX, segPoints[0].y, posX, closest]);
				newSeg = adicionarSegmento([posX, closest, posX, segPoints[1].y]);
				highlightSegmento(newSeg);
			}
		}

		highlightSegmento(segmento);
		layersRedraw();
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

	function handleMouseUpEvent(evt) {

		if (evt.which != 1) return;


		var posX = getMousePosX(evt);
		var posY = getMousePosY(evt);

		// separa segmento
		if (separarAtivado) {
			if (isMouseOverAnElement()) separaSegmento(getSegmento(mouseOverElement.getPoints()), posX, posY);
			return;
		}

		//cria novo segmento
		desenhandoSegmento = false;

		if (adicaoAtivada && typeof novoSegmento != 'undefined') {
			var points = novoSegmento.getPoints();
			novoSegmento.remove();
			novoSegmento = undefined;

			var seg = criaNovoSegmento(points);
			clickOnSegmento(evt, seg);
			return;
		}

		selecionandoArea = false;
		if (selecaoAreaAtivada && typeof selectionArea != 'undefined') {
			selectArea(selectionArea);
			selectionArea.remove();
			selectionArea = undefined;
			layersRedraw();
			return
		}

		if (evt.target.tagName != "CANVAS") return;

		if (isMouseOverAnElement()) {
			clickOnSegmento(evt, mouseOverElement);
			console.log(mouseOverElement.getPoints());
			return;
		}

		if (!adicaoAtivada) {
			document.body.style.cursor = "default";
		}

		selecionandoSegmento = false;
		clearSelection();
	}

	function selectArea(selectionArea) {
		clearSelection();

		var initPos = selectionArea.getAbsolutePosition();
		var finalPosX = initPos.x + selectionArea.getWidth();
		var finalPosY = initPos.y + selectionArea.getHeight();

		var maxX, maxY, minX, minY;

		if (initPos.x > finalPosX) {
			maxX = initPos.x;
			minX = finalPosX;
		} else {
			maxX = finalPosX;
			minX = initPos.x;
		}

		if (initPos.y > finalPosY) {
			maxY = initPos.y;
			minY = finalPosY;
		} else {
			maxY = finalPosY;
			minY = initPos.y;
		}

		var area = [minX, minY, maxX, maxY];
		for (var i = 0; i < linhas.length; i++) {
			var points = linhas[i].getPoints();
			if (isSegmentInArea(points, area)) {
				highlightSegmento(linhas[i]);
			}
		}
		for (var i = 0; i < colunas.length; i++) {
			var points = colunas[i].getPoints();
			if (isSegmentInArea(points, area)) {
				highlightSegmento(colunas[i]);
			}
		}
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
//		var localEvt = typeof evt.originalEvent == "undefined" ? evt : evt.originalEvent;
//		return (typeof localEvt.offsetX == "undefined") ? localEvt.layerX
//				: localEvt.offsetX;
		return (typeof evt.offsetX == "undefined") ? evt.layerX
				: evt.offsetX;
	}

	function getMousePosY(evt) {
		/*var localEvt = typeof evt.originalEvent == "undefined" ? evt : evt.originalEvent;
		return (typeof localEvt.offsetY == "undefined") ? localEvt.layerY
				: localEvt.offsetY;*/
		return (typeof evt.offsetY == "undefined") ? evt.layerY
				: evt.offsetY;
	}

	function criaNovoSegmento(points) {

		var deltaX = Math.abs(points[1].x - points[0].x);
		var deltaY = Math.abs(points[1].y - points[0].y);

		if (deltaX == 0 && deltaY == 0) {
			layersRedraw();
		 	return;
		}

		var seg;

		if (deltaY > deltaX) {
			var posX = points[0].x;
			var initY = points[0].y;
			points[1].x = points[0].x;
			var finalY = points[1].y;
			seg = criarNovaColuna(posX, initY, finalY);
		} else {
			var posY = points[0].y;
			var initX= points[0].x;
			points[1].y = points[0].y;
			var finalX = points[1].x;
			seg = criarNovaLinha(posY, initX, finalX);
		}
		return seg;
	}

	function isMousePosOffBorders(pos) {
		return (pos.x < minX || pos.x > maxX) ||
			(pos.y < minY || pos.y > maxY);
	}

	function handleMouseMoveEvent(evt) {

		if (evt.which != 1) return;

		//mudar desenhando & selecionando pra isMousedown boolean
		if (adicaoAtivada && desenhandoSegmento) {
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
			return;
		}

		if (selecaoAreaAtivada && selecionandoArea) {

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
			return;
		}
	}

	function clickOnSegmento(evt, seg) {

		if (isMouseOverAnElement()) {
			document.body.style.cursor = "move";
		}

		if (!evt.shiftKey) {
			clearSelection();
		}

		highlightSegmento(seg);
		selecionandoSegmento = true;
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
		} else if (isLinha(points) && !isBorda(points) && inZoom(points[0].y)) {
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
		var selectedAny = false;

		for (var i = linhas.length - 1; i >= 0; i--) {
			if (linhas[i].getStroke() == highlightColor) {
				var success = removeSegmento(linhas[i]);
				removedAny = removedAny || success;
				selectedAny = true;
			}
		}
		for (var i = colunas.length - 1; i >= 0; i--) {
			if (colunas[i].getStroke() == highlightColor) {
				var success = removeSegmento(colunas[i]);
				removedAny = removedAny || success;
				selectedAny = true;
			}
		}
		return {'removedAny': removedAny, 'selectedAny': selectedAny};
	}

	function handleBodyClickEvent(e) {
		if (e.target.tagName != "CANVAS" && e.target.tagName != "BUTTON" &&
			 e.target.tagName != "IMG" && e.target.tagName != "I") {
			clearSelection();
			selecionandoSegmento = false;
			document.body.style.cursor = "default";
		}
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
	        layersRedraw();
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

				uneIntercessoes(points2);
				break;
			}
		}
	       	layersRedraw();
		return true;
	}

	function validaRemocao(segPoints) {

		if (isLinha(segPoints)) {

			if (!temColunasDelimitando(segPoints)) return false;

			// checa se as colunas que tocam a linha tem continuacao
			var posY = segPoints[0].y;
			for (var i = 0; i < colunas.length; i++) {
				var points = colunas[i].getPoints();
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

		for (var i = 0; i < colunas.length; i++){
			var coluna = colunas[i].getPoints();
			var segmento = [ coluna[0].x - shiftOnCanvas, coluna[0].y - shiftOnCanvas, coluna[1].x - shiftOnCanvas, coluna[1].y - shiftOnCanvas];
			linhasASalvar.push(segmento);
		}

		for (var i = 0; i < linhas.length; i++){
			var linha = linhas[i].getPoints();
		        var segmento = [ linha[0].x - shiftOnCanvas, linha[0].y - shiftOnCanvas, linha[1].x - shiftOnCanvas, linha[1].y - shiftOnCanvas];
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
