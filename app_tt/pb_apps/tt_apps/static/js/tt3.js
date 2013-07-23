	$('body').on('contextmenu', '#canvas-container', function(e) {
		return false;
	});

	// Usada
	Array.prototype.compare = function(array) {
		// if the other array is a falsy value, return
		if (!array)
			return false;

		// compare lengths - can save a lot of time
		if (this.length != array.length)
			return false;

		for ( var i = 0; i < this.length; i++) {
			// Check if we have nested arrays
			if (this[i] instanceof Array && array[i] instanceof Array) {
				// recurse into the nested arrays
				if (!this[i].compare(array[i]))
					return false;
			} else if (this[i] != array[i]) {
				// Warning - two different object instances will never be equal:
				// {x:20} != {x:20}
				return false;
			}
		}
		return true;
	}

	var linhas;
	var colunas;
	var arr;
	var minX;
	var maxX;
	var minY;
	var maxY;
	var minDistance;
	var leftX;
	var rightX;
	var upperY;
	var bottomY;
	var horizontal = 1;
	var vertical = 2;
	var posUnidas;
	var adicionandoLinha = false;
	var adicionandoColuna = false;
   	var zoom = new Array();
	var hasZoom = false;
	var sortFunction = function(a, b) {
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
	var element2Remove;

	var i = 0;
	var j = 0;

	var stage;

	var layer;

	function initVariables() {
		linhas = new Array();
		colunas = new Array();
		arr = new Array();
		posUnidas = new Array();
	   	zoom = new Array();
		adicionandoLinha = false;
		adicionandoColuna = false;
		hasZoom = false;
		i = 0;
		j = 0;
		layer = new Kinetic.Layer();
		minX = 2000;
		minY = 2000;
		maxX = 0;
		maxY = 0;
		// distância mínima entre linhas e colunas (em pixels)
		minDistance = 4;
	}

	// Usada
	function isLinha(pts) {
		return pts[0].y == pts[1].y;
	}

	// Usada
	function isMesmaLinha(points1, points2) {
		return isLinha(points1) && isLinha(points2) && points1[0].y == points2[0].y;
	}

	// Usada
	function isLinhaDaBorda(pts) {
		return isLinha(pts) && pts[0].y == maxY;
	}

	// Usada
	function isColuna(pts) {
		return pts[0].x == pts[1].x;
	}

	// Usada
	function isMesmaColuna(points1, points2) {
		return isColuna(points1) && isColuna(points2)
				&& points1[0].x == points2[0].x;
	}

	// Usada
	function isColunaDaBorda(pts) {
		return isColuna(pts) && pts[0].x == maxX;
	}

	// Usada
	function isBorda(pontos) {
		return ((pontos[0].x == pontos[1].x && (pontos[0].x == maxX || pontos[0].x == minX)) || (pontos[0].y == pontos[1].y && (pontos[0].y == maxY || pontos[0].y == minY)));
	}

	// Usada
	function isPosBorda(pontos) {
		// var points = [{x:pontos[0],y:pontos[1]},{x:pontos[2],y:pontos[3]}];
		// return isBorda(points);
		return ((pontos[0] == pontos[2] && (pontos[0] == maxX || pontos[0] == minX)) || (pontos[1] == pontos[3] && (pontos[1] == maxY || pontos[1] == minY)));
	}

	// Usada
	function moverLinha(posY, newPosY) {
		if (!isPosBorda([ minX, posY, maxX, posY ]) && inZoom(posY) && inZoom(newPosY)) {
			for (i = 0; i < linhas.length; i++) {
				var pts = linhas[i].getPoints();
				if (pts[0].y == pts[1].y && pts[0].y == posY) {
					atualizaSegmentosAdjacentes(pts, [ pts[0].x, newPosY, pts[1].x,
							newPosY ]);
					linhas[i].setPoints([ pts[0].x, newPosY, pts[1].x, newPosY ]);
				}
			}
		}
	}

	// Usada
	function moverColuna(posX, newPosX) {
		if (!isPosBorda([ posX, minY, posX, maxY ])) {
			for (i = 0; i < colunas.length; i++) {
				var pts = colunas[i].getPoints();
				if (pts[0].x == pts[1].x && pts[0].x == posX) {
					atualizaSegmentosAdjacentes(pts, [ newPosX, pts[0].y, newPosX,
							pts[1].y ]);
					colunas[i].setPoints([ newPosX, pts[0].y, newPosX, pts[1].y ]);
				}
			}
		}
	}

	// TODO Essa funcao DEVE ser refatorada.
	// Usada
	function atualizaSegmentosAdjacentes(ptsAntes, ptsDepois) {
		for ( var z = 0; z < linhas.length; z++) {
			pts = linhas[z].getPoints();
			if (ptsAntes[0].x == ptsAntes[1].x && pts[0].y == pts[1].y
					&& (ptsAntes[0].y == pts[0].y || ptsAntes[1].y == pts[0].y)
					&& ptsAntes[0].x == pts[0].x) {
				linhas[z].setPoints([ ptsDepois[0], pts[0].y, pts[1].x, pts[1].y ]);
			} else if (ptsAntes[0].x == ptsAntes[1].x && pts[0].y == pts[1].y
					&& (ptsAntes[0].y == pts[0].y || ptsAntes[1].y == pts[0].y)
					&& ptsAntes[0].x == pts[1].x) {
				linhas[z].setPoints([ pts[0].x, pts[0].y, ptsDepois[2], pts[1].y ]);
			} else if (ptsAntes[0].y == ptsAntes[1].y && pts[0].x == pts[1].x
					&& (ptsAntes[0].x == pts[0].x || ptsAntes[1].x == pts[0].x)
					&& ptsAntes[0].y == pts[0].y) {
				linhas[z].setPoints([ pts[0].x, ptsDepois[1], pts[1].x, pts[1].y ]);
			} else if (ptsAntes[0].y == ptsAntes[1].y && pts[0].x == pts[1].x
					&& (ptsAntes[0].x == pts[0].x || ptsAntes[1].x == pts[0].x)
					&& ptsAntes[0].y == pts[1].y) {
				linhas[z].setPoints([ pts[0].x, pts[0].y, pts[1].x, ptsDepois[3] ]);
			}
		}
		for ( var z = 0; z < colunas.length; z++) {
			pts = colunas[z].getPoints();
			if (ptsAntes[0].x == ptsAntes[1].x && pts[0].y == pts[1].y
					&& (ptsAntes[0].y == pts[0].y || ptsAntes[1].y == pts[0].y)
					&& ptsAntes[0].x == pts[0].x) {
				colunas[z]
						.setPoints([ ptsDepois[0], pts[0].y, pts[1].x, pts[1].y ]);
			} else if (ptsAntes[0].x == ptsAntes[1].x && pts[0].y == pts[1].y
					&& (ptsAntes[0].y == pts[0].y || ptsAntes[1].y == pts[0].y)
					&& ptsAntes[0].x == pts[1].x) {
				colunas[z]
						.setPoints([ pts[0].x, pts[0].y, ptsDepois[2], pts[1].y ]);
			} else if (ptsAntes[0].y == ptsAntes[1].y && pts[0].x == pts[1].x
					&& (ptsAntes[0].x == pts[0].x || ptsAntes[1].x == pts[0].x)
					&& ptsAntes[0].y == pts[0].y) {
				colunas[z]
						.setPoints([ pts[0].x, ptsDepois[1], pts[1].x, pts[1].y ]);
			} else if (ptsAntes[0].y == ptsAntes[1].y && pts[0].x == pts[1].x
					&& (ptsAntes[0].x == pts[0].x || ptsAntes[1].x == pts[0].x)
					&& ptsAntes[0].y == pts[1].y) {
				colunas[z]
						.setPoints([ pts[0].x, pts[0].y, pts[1].x, ptsDepois[3] ]);
			}
		}
	}

	// Usada
	function verificaExistenciaLinha(pontos) {

		// Se for uma linha, verifica existencia entre as linhas.
		if (pontos[1] == pontos[3]) {
			for ( var t = 0; t < linhas.length; t++) {
				var pts = linhas[t].getPoints();
				if (pts[0].x == pontos[0] && pts[0].y == pontos[1]
						&& pts[1].x == pontos[2] && pts[1].y == pontos[3]) {
					return true;
				}
			}
		}

		// Se for uma coluna, verifica existencia entre as colunas.
		else {
			for ( var t = 0; t < colunas.length; t++) {
				var pts = colunas[t].getPoints();
				if (pts[0].x == pontos[0] && pts[0].y == pontos[1]
						&& pts[1].x == pontos[2] && pts[1].y == pontos[3]) {
					return true;
				}
			}
		}
		return false;
	}

	// Usada
	function adicionarNovaLinha() {
		if (adicionandoColuna) {
			adicionandoColuna = false;
		}

        	adicionandoLinha = true;
		document.body.style.cursor = "pointer";
	}

	function adicionarFocoZoom(zoom){

		layerZoom = new Kinetic.Layer();
		var topRect = new Kinetic.Rect({
		    x: minX,
		    y: minY,
		    width: minX + zoom[2],
		    height: minY + zoom[1],
		    fill: '#000',
		    opacity: 0.6,

		});

		var botRect = new Kinetic.Rect({
		    x: minX,
		    y: zoom[3],
		    width: minX + zoom[2],
		    height: zoom[3] + maxY,
		    fill: '#000',
		    opacity: 0.6

		});

		layerZoom.add(topRect);
		layerZoom.add(botRect);
	}

	function inZoom(posY){
		return !hasZoom || (posY >= zoom[1] && posY <= zoom[3]);
	}

	// Usada
	function criarNovaLinha(posY) {
		while (temLinha(posY) && posY < maxY) {
			posY += 2;
		}

	        if (inZoom(posY)) {
	            var intercessoes = encontraIntercessoesVerticais(posY);
	            for ( var z = 0; z < intercessoes.length - 1; z++) {
	                var pontos = [ intercessoes[z], posY, intercessoes[z + 1], posY ];
	                adicionarSegmento(pontos);
	                atualizarIntercessao(pontos);
	            }
                    adicionandoLinha = false;
                    document.body.style.cursor = "default";
        	}
	}

	// Usada
	function adicionarNovaColuna() {
		if (adicionandoLinha) {
			adicionandoLinha = false;
		}
	        adicionandoColuna = true;
		document.body.style.cursor = "pointer";
	}

	// Usada
	function criarNovaColuna(posX) {
		while (temLinha(posX) && posX < maxX) {
			posX += 2;
		}
		var intercessoes = encontrarIntercessoesHorizontais(posX);
		for ( var z = 0; z < intercessoes.length - 1; z++) {
			var pontos = [ posX, intercessoes[z], posX, intercessoes[z + 1] ];

			adicionarSegmento(pontos);
			atualizarIntercessao(pontos);
		}
		adicionandoColuna = false;
                document.body.style.cursor = "default";	
	}

	// Usada
	function temLinha(posY) {
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].y == pts2[1].y && pts2[0].y == posY) {
				return true;
			}
		}
		return false;
	}

	// Usada
	function atualizarIntercessao(pontos) {
		var pts2;
		var aAdicionar = new Array();
		// Se for uma linha
		if (pontos[1] == pontos[3]) {
			for ( var z = 0; z < colunas.length; z++) {
				pts2 = colunas[z].getPoints();
				if (pontos[0] == pts2[0].x && pontos[1] > pts2[0].y
						&& pontos[3] < pts2[1].y) {
					colunas[z].setPoints([ pts2[0].x, pts2[0].y, pts2[1].x,
							pontos[1] ]);
					aAdicionar.push([ pts2[0].x, pontos[1], pts2[1].x, pts2[1].y ]);
				}
			}
		} else if (pontos[0] == pontos[2]) {
			for ( var z = 0; z < linhas.length; z++) {
				pts2 = linhas[z].getPoints();
				if (pontos[1] == pts2[0].y && pontos[0] > pts2[0].x
						&& pontos[2] < pts2[1].x) {
					linhas[z].setPoints([ pts2[0].x, pts2[0].y, pontos[0],
							pts2[1].y ]);
					aAdicionar.push([ pontos[2], pts2[0].y, pts2[1].x, pts2[1].y ]);
				}
			}
		}
		for ( var w = 0; w < aAdicionar.length; w++) {
			if (!verificaExistenciaLinha(aAdicionar[w])) {
				adicionarSegmento(aAdicionar[w]);
			}
		}
	}

	// Usada
	function encontraIntercessoesVerticais(altura) {
		var intercessoes = new Array();
		for ( var z = 0; z < colunas.length; z++) {
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

	// Usada
	function encontrarIntercessoesHorizontais(distancia) {
		var intercessoes = new Array();
		for ( var z = 0; z < linhas.length; z++) {
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

	// Usada
	function adicionarSegmento(pontos) {

		var segmento = new Kinetic.Line({
			points : pontos,
			stroke : 'red',
			draggable : true,
			strokeWidth : 2,
			dragBoundFunc : function(pos, event) {
				var points = this.getPoints();
				if (isColuna(points)) {
					var posX = event.offsetX == undefined ? event.layerX
							: event.offsetX;
					var limEsq = encontraLimiteEsquerda(points[0].x) + minDistance;
					var limDir = encontraLimiteDireita(points[0].x) - minDistance;

					var newX = posX <= limEsq ? limEsq
							: (posX >= limDir ? limDir : posX);
					moverColuna(points[0].x, newX);

				} else {
					var posY = event.offsetY == undefined ? event.layerY
							: event.offsetY;
					var limSup = encontraLimiteSuperior(points[0].y) + minDistance;
					var limInf = encontraLimiteInferior(points[0].y) - minDistance;

					var newY = posY <= limSup ? limSup
							: (posY >= limInf? limInf : posY);
					moverLinha(points[0].y, newY);
				}

				return {
					x : 0,
					y : 0
				};
			}
		});
		var pts = segmento.getPoints();
		if (pts[0].x == pts[1].x) {
			if (!isBorda(pts)) {
				segmento.on("mouseover", function() {
					if (!(adicionandoLinha || adicionandoColuna))
						document.body.style.cursor = "ew-resize";
					layer.draw();
				});
			}
		} else if (inZoom(pts[0].y) && inZoom(pts[1].y)) {
			if (!isBorda(pts)) {
				segmento.on("mouseover", function() {
					if (!(adicionandoLinha || adicionandoColuna))
						document.body.style.cursor = "ns-resize";
					layer.draw();
				});
			}
		}

		segmento.on("mouseout", function() {
			document.body.style.cursor = "default";
			layer.draw();
		});

		segmento.on("mouseover touchstart",
				function() {
					var points = this.getPoints();
					if (isColuna(points) && !isBorda(points)) {
						var z;
						for (z = 0; z < colunas.length; z++) {
							var points2 = colunas[z].getPoints();
							if (points2[0].x == points2[1].x
									&& points[0].x == points2[0].x) {
								colunas[z].setStroke('green');
							}
						}
					} else if (isLinha(points) && !isBorda(points) && inZoom(points[0].y)) {
                        var z;
						for (z = 0; z < linhas.length; z++) {
							var points2 = linhas[z].getPoints();
							if (points2[0].y == points2[1].y
									&& points[0].y == points2[0].y) {
								linhas[z].setStroke('green');
							}
						}
					}

					layer.draw();
				});
		segmento.on('mouseout touchend', function() {
			var points = this.getPoints();
			if (isColuna(points)) {
				for (i = 0; i < colunas.length; i++) {
					colunas[i].setStroke('red');
				}
			} else {
				for (i = 0; i < linhas.length; i++) {
					linhas[i].setStroke('red');
				}
			}
			layer.draw();
		});
		if (isLinha(segmento.getPoints())) {
			linhas.push(segmento);
		} else {
			colunas.push(segmento);
		}
		layer.add(segmento);
		layer.draw();
	}

	// Usada
	function encontraLimiteSuperior(posY) {
		var posicoesY = new Array();
		var pts2;

      		if (posY == zoom[1]){
	            return zoom[1];
        	}

		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].y < posY) {
				posicoesY.push(pts2[0].y);
			}
		}
		if (posicoesY.length == 0) {
			return minY;
		}
		posicoesY.sort(function(a, b) {
			return b - a;
		});
		return posicoesY[0];
	}

	// Usada
	function encontraLimiteEsquerda(posX) {
		var posicoesX = new Array();
		var pts2;
		for ( var z = 0; z < colunas.length; z++) {
			pts2 = colunas[z].getPoints();
			if (pts2[0].x < posX) {
				posicoesX.push(pts2[0].x);
			}
		}
		if (posicoesX.length == 0) {
			return minX;
		}
		posicoesX.sort(function(a, b) {
			return b - a;
		});
		return posicoesX[0];
	}

	// Usada
	function encontraLimiteInferior(posY) {

       		if (posY == zoom[3]){ //Jey aqui
	            return zoom[3];
	        }

		var posicoesY = new Array();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].y > posY) {
				posicoesY.push(pts2[0].y);
			}
		}

		if (posicoesY.length == 0) {
			return maxY;
		}
		posicoesY.sort(function(a, b) {
			return a - b;
		});
		return posicoesY[0];
	}

	// Usada
	function encontraLimiteDireita(posX) {
		var posicoesX = new Array();
		var pts2;
		for ( var z = 0; z < colunas.length; z++) {
			pts2 = colunas[z].getPoints();
			if (pts2[0].x > posX) {
				posicoesX.push(pts2[0].x);
			}
		}
		if (posicoesX.length == 0) {
			return maxX;
		}
		posicoesX.sort(function(a, b) {
			return a - b;
		});
		return posicoesX[0];
	}

	// Usada
	function uneIntercessaoColuna(posX, posY) {
		var pos1;
		var pos3;

		var z;

		for (z = colunas.length - 1; z >= 0; z--) {
			var points2 = colunas[z].getPoints();
			if (points2[0].x == posX) {
				if (points2[0].y == posY) {
					pos3 = points2[1].y;
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
		adicionarSegmento([ posX, pos1, posX, pos3 ]);
	}

	// Usada
	function uneIntercessaoLinha(posX, posY) {
		var pos0;
		var pos2;

		var z;

		for (z = linhas.length - 1; z >= 0; z--) {
			var points2 = linhas[z].getPoints();
			if (points2[0].y == posY) {
				if (points2[0].x == posX) {
					pos2 = points2[1].x;
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
		adicionarSegmento([ pos0, posY, pos2, posY ]);
	}

	// Usada
	function uneIntercessoes(points) {
		var pos1, pos2;
		if (isLinha(points)) {
			pos0 = points[0].x;
			pos1 = points[1].x;
			var posY = points[0].y;
			var t = $.inArray(pos0, posUnidas);
			if (t == -1) {
				uneIntercessaoColuna(pos0, posY);
				posUnidas.push(pos0);
			}
			t = $.inArray(pos1, posUnidas);
			if (t == -1) {
				uneIntercessaoColuna(pos1, posY);
				posUnidas.push(pos1);
			}
		} else {
			pos0 = points[0].y;
			pos1 = points[1].y;
			var posX = points[0].x;
			var t = $.inArray(pos0, posUnidas);
			if (t == -1) {
				uneIntercessaoLinha(posX, pos0);
				posUnidas.push(pos0);
			}
			t = $.inArray(pos1, posUnidas);
			if (t == -1) {
				uneIntercessaoLinha(posX, pos1);
				posUnidas.push(pos1);
			}
		}
	}

	// Usada
	function existeSegmento(pontos, array) {
		var z;
		for (z = 0; z < array.length; z++) {
			if (pontos.compare(array[z])) {
				return true;
			}
		}
		return false;
	}

	function filterRectangles() {
		var linhas2Remove = new Array();

		// remove linhas com uma distancia minima
		for (i = colunas.length - 1; i >= 0; i--) {
			var points = colunas[i].getPoints();
			if ((points[1].y - points[0].y) < minDistance) {
				var segmentoLinha = encontraSegmentoLinhaSuperior(points);
				if (isBorda(segmentoLinha.getPoints())) {
					segmentoLinha = encontraSegmentoLinhaInferior(points);
				}
				linhas2Remove.push(segmentoLinha);
			}
		}

		var colunas2Remove = new Array();

		// remove colunas com uma distancia minima
		for (i = linhas.length - 1; i >= 0; i--) {
			var points = linhas[i].getPoints();
			if ((points[1].x - points[0].x) < minDistance) {
				var segmentoColuna = encontraSegmentoColunaSuperior(points);
				if (isBorda(segmentoColuna.getPoints())) {
					segmentoColuna = encontraSegmentoColunaInferior(points);
				}
				colunas2Remove.push(segmentoColuna);
			}
		}

		for (var i = 0; i < linhas2Remove.length; i++) {
			removerLinha(linhas2Remove[i]);
		}

		for (var i = 0; i < colunas2Remove.length; i++) {
			removerColuna(colunas2Remove[i]);
		}
	}

	function encontraSegmentoLinhaSuperior(points){
		var posY = points[0].y;
		return encontraSegmentoLinha(posY);
	}

	function encontraSegmentoLinhaInferior(points){
		var posY = points[1].y;
		return encontraSegmentoLinha(posY);
	}

	function encontraSegmentoLinha(posY) {
		for (var z = 0; z < linhas.length; z++){
			var pointsLinha = linhas[z].getPoints();
			if (pointsLinha[0].y == posY) return linhas[z];
		}
	}

	function encontraSegmentoColunaSuperior(points){
		var posX = points[1].x;
		return encontraSegmentoColuna(posX);
	}

	function encontraSegmentoColunaInferior(points){
		var posX = points[0].X;
		return encontraSegmentoColuna(posX);
	}

	function encontraSegmentoColuna(posX) {
		for (var z = 0; z < colunas.length; z++){
			var pointsColuna = colunas[z].getPoints();
			if (pointsColuna[0].x == posX) return colunas[z];
		}
	}

	function removerLinha(segmento) {
		var points = segmento.getPoints();
		for (i = linhas.length - 1; i >= 0; i--) {
			var points2 = linhas[i].getPoints();
			if (isMesmaLinha(points, points2)) {
				linhas[i].remove();
				linhas.splice(i, 1);
				// Finalmente, atualizamos todas aquelas
				// intercessões que não são mais cruzadas.
				uneIntercessoes(points2);
			}
		}
	}

	function removerColuna(segmento) {
		var points = segmento.getPoints();

		// Eh necessario fazer iteracao inversa sobre o array para
		// nao pular nenhum elemento.
		for (i = colunas.length - 1; i >= 0; i--) {
			var points2 = colunas[i].getPoints();
			if (isMesmaColuna(points, points2)) {
				colunas[i].remove();
				colunas.splice(i, 1);
				// Finalmente, atualizamos todas aquelas
				// intercessões que não são mais cruzadas.
				uneIntercessoes(points2);
			}
		}
	}

	// Usada
	function initGrid(matrizDePontos, uri, hasZoom, zoom_input) {
		hasZoom = hasZoom;
		initVariables();

		if (hasZoom) {
		        zoom = zoom_input;
		}

		var arrayAux = new Array();

		for (i = 0; i < matrizDePontos.length; i++) {

			arr = matrizDePontos[i];

			leftX = arr[0];
			if (leftX < minX)
				minX = leftX;
			upperY = arr[1];
			if (upperY < minY)
				minY = upperY;
			rightX = arr[2];
			if (rightX > maxX)
				maxX = rightX;
			bottomY = arr[3];
			if (bottomY > maxY)
				maxY = bottomY;

			var novasLinhas = new Array();
			novasLinhas.push([ leftX, upperY, rightX, upperY ]);
			novasLinhas.push([ leftX, upperY, leftX, bottomY ]);
			novasLinhas.push([ leftX, bottomY, rightX, bottomY ]);
			novasLinhas.push([ rightX, upperY, rightX, bottomY ]);

			// Inicialmente, colocamos todas as coordenadas de todos os
			// segmentos gerados a partir do arquivo de entrada em arrayAux,
			// contanto que eles nao existam ainda no mesmo.
			for ( var z = 0; z < novasLinhas.length; z++) {
				if (!existeSegmento(novasLinhas[z], arrayAux)) {
					arrayAux.push(novasLinhas[z]);
				}
			}
		}

		// Definicao da acao que deve ser tomada quando ocorrer um clique no
		// canvas (botao direito deve remover a linha selecionada).
		layer.on('click', function(evt) {

			// Codigo para remover todos os segmentos que pertencam a uma mesma
			// linha

			if ((evt.which && evt.which == 3) || (evt.button && evt.button == 2)) {
				posUnidas = new Array();
				// Recupera o objeto que foi clicado
				var shape = evt.targetNode;
				if (typeof shape == "undefined" || shape.getClassName() != "Line") return;

				var points = shape.getPoints();

				var posX = evt.offsetX == undefined ? evt.layerX
						: evt.offsetX;
				var posY = evt.offsetY == undefined ? evt.layerY
						: evt.offsetY;

				$("#context-menu").css("top", posY - 70);
				$("#context-menu").css("left", posX);
				$("#context-menu").css("position", "relative");

				$("#remover-menu").show();
				element2Remove = shape;
			}
			// Apos remover os objetos selecionados, redesenhamos a camada apenas
			// com os objetos restantes.
			layer.draw();
		});

		

	        adicionarFocoZoom(zoom);

		if (typeof stage == "undefined") {
			stage = new Kinetic.Stage({
				container : 'canvas-container',
				width : maxX,
				height : maxY
			});
		}

		for ( var z = 0; z < arrayAux.length; z++) {
			adicionarSegmento(arrayAux[z]);
		}

		filterRectangles();

		$("#canvas-container").click(function(evt) {

			if (adicionandoLinha) {
				var posY = evt.offsetY == undefined ? evt.layerY : evt.offsetY;
				criarNovaLinha(posY);
			}

			else if (adicionandoColuna) {
				var posX = evt.offsetX == undefined ? evt.layerX : evt.offsetX;
				criarNovaColuna(posX);
			}
		});

		var imageObj = new Image();
		imageObj.src = uri;
		imageObj.onload = function() {
			var tabela = new Kinetic.Image({
				x : 0,
				y : 0,
				image : imageObj,
				width : maxX,
				height : maxY
			});

			// add the shape to the layer
			layer.add(tabela);
			tabela.moveToBottom();

			// add the layer to the stage
			stage.add(layer);
                        stage.add(layerZoom);
		};
	}

	function handleRemoverSegmentoEvent() {
		points = element2Remove.getPoints();
		if (!isBorda(points)) {

			if (isColuna(points)) {
				removerSegmentoColuna(element2Remove);
			} else if (isLinha(points) && inZoom(points[1].y) && inZoom(points[0].y)) {
				removerSegmentoLinha(element2Remove);
			}
		}
	}

	function removerSegmentoColuna(segmento) {
		var points = segmento.getPoints();
		for (i = colunas.length - 1; i >= 0; i--) {
			var points2 = colunas[i].getPoints();
			if (equalsSegmento(points, points2)) {
				colunas[i].remove();
				colunas.splice(i, 1);
				//uneIntercessoes(points2);
				break;
			}
		}
	}

	function equalsSegmento(points, points2) {
		return points[0].x == points2[0].x && points[0].y == points2[0].y && 
			points[1].x == points2[1].x && points[1].y == points2[1].y;
	}

	function removerSegmentoLinha(segmento) {
		var points = segmento.getPoints();
		for (i = linhas.length - 1; i >= 0; i--) {
			var points2 = linhas[i].getPoints();
			if (equalsSegmento(points, points2)) {
				linhas[i].remove();
				linhas.splice(i, 1);
				//uneIntercessoes(points2);
				break;
			}
		}
	}

	function handleRemoverLinhaColunaEvent() {
		points = element2Remove.getPoints();
		if (!isBorda(points)) {

			if (isColuna(points)) {
				removerColuna(element2Remove);
			} else if (isLinha(points) && inZoom(points[1].y) && inZoom(points[0].y)) {
				removerLinha(element2Remove);
			}
		}
	}

	// Usada
	function salvarAlteracoes() {
		var leftX;
		var rightX;
		var upperY;
		var bottomY;
		var ptsLinha;
		var ptsColuna;
		var iteradorLinha;
		var iteradorColuna;
		var resultado = new Array();

		linhas.sort(sortFunction);
		colunas.sort(sortFunction);

		iteradorLinha = 0;
		iteradorColuna = 0;
		ptsLinha = linhas[iteradorLinha].getPoints();
		while (ptsLinha[0].y < maxY) { 
			ptsColuna = colunas[iteradorColuna].getPoints();
			
			// Essa situacao so ocorre quando comecamos a percorrer uma nova linha. 
			while (ptsColuna[0].y != ptsLinha[0].y) {
				iteradorColuna++;
				ptsColuna = colunas[iteradorColuna].getPoints();
			}
			
			leftX = ptsLinha[0].x;
			rightX = ptsLinha[1].x;
			upperY = ptsColuna[0].y;
			bottomY = ptsColuna[1].y;
			
			resultado.push([leftX, upperY, rightX, bottomY]);
			iteradorLinha++;
			iteradorColuna++;
			ptsLinha = linhas[iteradorLinha].getPoints();
		} 
		

		for (var z = 0; z < resultado.length; z++) {
			console.log(resultado[z][0] + ", " + resultado[z][1] + ", " + resultado[z][2] + ", " + resultado[z][3]);
		}

		return resultado;
	}

	// Usada 
	function clearCanvas() {
		stage.removeChildren();
		stage.remove();
	}
