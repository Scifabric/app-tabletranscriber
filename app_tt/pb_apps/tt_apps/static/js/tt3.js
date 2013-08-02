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
	var posXAdicao;
	var posYAdicao;
	var posUnidas;
	var adicionandoLinha = false;
	var adicionandoColuna = false;
   	var zoom = new Array();
	var hasZoom = false;
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

	var element2Remove;

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
		posXAdicao = 0;
		posYAdicao = 0;
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
			for (var i = 0; i < linhas.length; i++) {
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
			for (var i = 0; i < colunas.length; i++) {
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
		for (var z = 0; z < linhas.length; z++) {
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
		for (var z = 0; z < colunas.length; z++) {
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
		    opacity: 0.6

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
	            for (var z = 0; z < intercessoes.length - 1; z++) {
	                var pontos = [ intercessoes[z], posY, intercessoes[z + 1], posY ];
	                adicionarSegmento(pontos);
	                atualizarIntercessao(pontos);
	            }
                    adicionandoLinha = false;
                    //document.body.style.cursor = "default";
        	}
	}

	function adicionarNovaColuna() {
		if (adicionandoLinha) {
			adicionandoLinha = false;
		}
	        adicionandoColuna = true;
		document.body.style.cursor = "pointer";
	}

	// Usada
	function criarNovaColuna(posX) {
		// revisar
		while (temLinha(posX) && posX < maxX) {
			posX += 2;
		}
		var intercessoes = encontrarIntercessoesHorizontais(posX);

		for (var z = 0; z < intercessoes.length - 1; z++) {
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
		for (var z = 0; z < linhas.length; z++) {
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
			for (var z = 0; z < colunas.length; z++) {
				pts2 = colunas[z].getPoints();
				if (verificaSeColunaCruzaLinha(pontos, pts2)) {
					colunas[z].setPoints([ pts2[0].x, pts2[0].y, pts2[1].x,
							pontos[1] ]);
					aAdicionar.push([ pts2[0].x, pontos[1], pts2[1].x, pts2[1].y ]);
				}
			}
		} else if (pontos[0] == pontos[2]) {
			for (var z = 0; z < linhas.length; z++) {
				pts2 = linhas[z].getPoints();
				if (verificaSeLinhaCruzaColuna(pts2, pontos)) {
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

	function verificaSeLinhaCruzaColuna(pontosLinha, pontosColuna) {
		return (pontosColuna[1] == pontosLinha[0].y && pontosColuna[0] > pontosLinha[0].x && pontosColuna[2] < pontosLinha[1].x) ||
			(pontosColuna[3] == maxY && pontosColuna[3] == pontosLinha[0].y && pontosColuna[0] > pontosLinha[0].x && pontosColuna[2] < pontosLinha[1].x);
	}

	function verificaSeColunaCruzaLinha(pontosLinha, pontosColuna) {
		return (pontosLinha[0] == pontosColuna[0].x && pontosLinha[1] > pontosColuna[0].y && pontosLinha[3] < pontosColuna[1].y) ||
			(pontosLinha[2] == maxX && pontosLinha[2] == pontosColuna[0].x && pontosLinha[1] > pontosColuna[0].y && pontosLinha[3] < pontosColuna[1].y);
	}

	// Usada
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

	// Usada
	function encontrarIntercessoesHorizontais(distancia) {
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
					var limSup = encontraLimiteSuperior(points[0].y);
					var limInf = encontraLimiteInferior(points[0].y);
					
					limSup = limSup == zoom[1] ? limSup : limSup + minDistance;
					limInf = limInf == zoom[3] ? limInf : limInf - minDistance;	

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
						for (var z = 0; z < colunas.length; z++) {
							var points2 = colunas[z].getPoints();
							if (points2[0].x == points2[1].x
									&& points[0].x == points2[0].x) {
								colunas[z].setStroke('green');
							}
						}
					} else if (isLinha(points) && !isBorda(points) && inZoom(points[0].y)) {
						for (var z = 0; z < linhas.length; z++) {
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
				for (var i = 0; i < colunas.length; i++) {
					colunas[i].setStroke('red');
				}
			} else {
				for (var i = 0; i < linhas.length; i++) {
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

      		if (hasZoom && posY == zoom[1]){
	            return posY;
        	}

		for (var z = 0; z < linhas.length; z++) {
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
		for (var z = 0; z < colunas.length; z++) {
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

       		if (hasZoom && posY == zoom[3]) {
	            return posY;
	        }

		var posicoesY = new Array();
		var pts2;
		for (var z = 0; z < linhas.length; z++) {
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
		for (var z = 0; z < colunas.length; z++) {
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

		for (var z = colunas.length - 1; z >= 0; z--) {
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

		for (var z = linhas.length - 1; z >= 0; z--) {
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
			if (t == -1 && !temContinuacaoLinha(points[0], points)) {
				uneIntercessaoColuna(pos0, posY);
				posUnidas.push(pos0);
			}
			t = $.inArray(pos1, posUnidas);
			if (t == -1 && !temContinuacaoLinha(points[1], points)) {
				uneIntercessaoColuna(pos1, posY);
				posUnidas.push(pos1);
			}
		} else {
			pos0 = points[0].y;
			pos1 = points[1].y;
			var posX = points[0].x;
			var t = $.inArray(pos0, posUnidas);
			if (t == -1 && !temContinuacaoColuna(points[0], points)) {
				uneIntercessaoLinha(posX, pos0);
				posUnidas.push(pos0);
			}
			t = $.inArray(pos1, posUnidas);
			if (t == -1 && !temContinuacaoColuna(points[1], points)) {
				uneIntercessaoLinha(posX, pos1);
				posUnidas.push(pos1);
			}
		}
	}

	function temContinuacaoLinha(points, linha) {
		return temContinuacao(linhas, points, linha);
	}

	function temContinuacaoColuna(points, coluna) {
		return temContinuacao(colunas, points, coluna);
	}

	function temContinuacao(segmentos, points, segmento) {

		for (var i = 0; i< segmentos.length; i++) {
			var pointsSegmento = segmentos[i].getPoints();
			if (equalsPoints(pointsSegmento[0], points) || equalsPoints(pointsSegmento[1], points))  return true; 		
		}
		
		return false;
	}

	// Usada
	function existeSegmento(pontos, array) {
		var z;
		for (var z = 0; z < array.length; z++) {
			if (pontos.compare(array[z])) {
				return true;
			}
		}
		return false;
	}

	function filterRectangles() {
		var linhas2Remove = new Array();
		var colunas2Remove = new Array();

		// remove linhas com uma distancia minima
		for (var i = colunas.length - 1; i >= 0; i--) {
			var points = colunas[i].getPoints();
			if ((points[1].y - points[0].y) < minDistance) {
				var segmentoLinha = encontraSegmentoLinhaSuperior(points);
				if (isBorda(segmentoLinha.getPoints())) {
					segmentoLinha = encontraSegmentoLinhaInferior(points);
				}
				
				if ($.inArray(segmentoLinha, linhas2Remove) == -1) {
					linhas2Remove.push(segmentoLinha);
				}
			}
		}

		// remove colunas com uma distancia minima
		for (var i = linhas.length - 1; i >= 0; i--) {
			var points = linhas[i].getPoints();
			if ((points[1].x - points[0].x) < minDistance) {
				var segmentoColuna = encontraSegmentoColunaSuperior(points);
				if (isBorda(segmentoColuna.getPoints())) {
					segmentoColuna = encontraSegmentoColunaInferior(points);
				}
				colunas2Remove.push(segmentoColuna);
				continue;
			}

			if (!inZoom(points[0].y)) {
				if (!isBorda(points) && $.inArray(linhas[i], linhas2Remove) == -1) {
					linhas2Remove.push(linhas[i]);
				}
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

	// Codigo para remover todos os segmentos que pertencam a uma mesma
	// linha
	function removerLinha(segmento) {
		posUnidas = new Array();
		var points = segmento.getPoints();
		for (var i = linhas.length - 1; i >= 0; i--) {
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

	// Codigo para remover todos os segmentos que pertencam a uma mesma
	// coluna
	function removerColuna(segmento) {

		posUnidas = new Array();
		var points = segmento.getPoints();

		// Eh necessario fazer iteracao inversa sobre o array para
		// nao pular nenhum elemento.
		for (var i = colunas.length - 1; i >= 0; i--) {
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
	function initGrid(matrizDePontos, uri, zoomEnabled, zoom_input) {
		initVariables();
		hasZoom = zoomEnabled;

		if (zoomEnabled) {
		        zoom = zoom_input;
		}

		var arrayAux = new Array();

		for (var i = 0; i < matrizDePontos.length; i++) {

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
			for (var z = 0; z < novasLinhas.length; z++) {
				if (!existeSegmento(novasLinhas[z], arrayAux)) {
					arrayAux.push(novasLinhas[z]);
				}
			}
		}

		if (zoomEnabled) {
			adicionarFocoZoom(zoom);
		}

		if (typeof stage != "undefined") {
			$(".kineticjs-content").remove();
		}

		stage = new Kinetic.Stage({
			container : 'canvas-container',
			width : maxX,
			height : maxY
		});

		// Definicao da acao que deve ser tomada quando ocorrer um clique no
		// canvas (botao direito deve remover a linha selecionada).
		stage.on('click', function(evt) {
			$("#remover-menu").hide();

			if ((evt.which && evt.which == 3) || (evt.button && evt.button == 2)) {

				// Ajuste vertical para mostrar o context menu no local correto.
				// Necessário verificar se esse ajuste é o mesmo para qualquer navegador/SO.
				var ajusteVertical = 70; //70px

				// Recupera o objeto que foi clicado
				var shape = evt.targetNode;
				if (typeof shape == "undefined") return;

				var posX = evt.offsetX == undefined ? evt.layerX
						: evt.offsetX;
				var posY = evt.offsetY == undefined ? evt.layerY
						: evt.offsetY;

				if (hasZoom && (posY < zoom[1] || posY > zoom[3])) return;

				$("#context-menu").css("top", posY - ajusteVertical);
				$("#context-menu").css("left", posX);
				$("#context-menu").css("position", "relative");

				if (shape.getClassName() == "Line") {

					$("#adicionar-linha").css("display", "none");
					$("#adicionar-coluna").css("display", "none");
					$("#remover-linha-coluna").show();
					$("#remover-segmento").show();

					element2Remove = shape;

				} else {

					$("#remover-linha-coluna").css("display", "none");
					$("#remover-segmento").css("display", "none");
					$("#adicionar-linha").show();
					$("#adicionar-coluna").show();
					
					// Armazenamos a posição do click para poder ter a referência de onde adicionar
					// a nova linha/coluna.
					posXAdicao = posX;
					posYAdicao = posY;
				}

				$("#remover-menu").show();
			}
		});

		for (var z = 0; z < arrayAux.length; z++) {
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
			if (hasZoom) stage.add(layerZoom);
		};
	}

	function handleAdicionarLinhaEvent() {
		criarNovaLinha(posYAdicao);
	}

	function handleAdicionarColunaEvent() {
		criarNovaColuna(posXAdicao);
	}

	function handleRemoverSegmentoEvent() {
		var points = element2Remove.getPoints();

		if (!isBorda(points)) {

			if (isColuna(points)) {
				return removerSegmentoColuna(element2Remove);
			} else if (isLinha(points) && inZoom(points[1].y) && inZoom(points[0].y)) {
				return removerSegmentoLinha(element2Remove);
			}
		}
	}

	function removerSegmentoColuna(segmento) {
		var points = segmento.getPoints();

		if (!validaIntersecoes(points)) {
			return false;
		}

		posUnidas = new Array();
		for (var i = colunas.length - 1; i >= 0; i--) {
			var points2 = colunas[i].getPoints();
			if (equalsSegmento(points, points2)) {
				colunas[i].remove();
				colunas.splice(i, 1);
				uneIntercessoes(points2);
				break;
			}
		}
	        layer.draw();
		return true;
	}

	function equalsSegmento(points, points2) {
		return points[0].x == points2[0].x && points[0].y == points2[0].y && 
			points[1].x == points2[1].x && points[1].y == points2[1].y;
	}

	function removerSegmentoLinha(segmento) {

		var points = segmento.getPoints();

		if (!validaIntersecoes(points)) {
			return;
		}

		posUnidas = new Array();
		for (var i = linhas.length - 1; i >= 0; i--) {
			var points2 = linhas[i].getPoints();
			if (equalsSegmento(points, points2)) {
				linhas[i].remove();
				linhas.splice(i, 1);

				uneIntercessoes(points2);
				break;
			}
		}
	        layer.draw();
		return true;
	}

	function validaIntersecoes(points) {

		var countIntersecoes = 0;
		var segmentos = new Array();
		
		if (isLinha(points)) {
			segmentos = colunas;
		} else {
			segmentos = linhas;
		}

		for (var i = 0; i < segmentos.length; i++) {
			pts2 = segmentos[i].getPoints();

			if (verificaSeTocaExtremidade(points, pts2)) {
				countIntersecoes++;
			}
		}

		return countIntersecoes == 4;
	}

	function verificaSeTocaExtremidade(segmento1, segmento2) {
		return equalsPoints(segmento1[0], segmento2[0]) || equalsPoints(segmento1[0], segmento2[1]) ||
			equalsPoints(segmento1[1], segmento2[0]) || equalsPoints(segmento1[1], segmento2[1]);

	}

	function equalsPoints(point1, point2) {
		return point1.x == point2.x && point1.y == point2.y;
	}

	function handleRemoverLinhaColunaEvent() {
		var points = element2Remove.getPoints();

		if (!isBorda(points)) {

			if (isColuna(points)) {
				removerColuna(element2Remove);
			} else if (isLinha(points) && inZoom(points[1].y) && inZoom(points[0].y)) {
				removerLinha(element2Remove);
			}
		}
	}

        function findColunaPerpendicular(ptsLinha){
        	for (var z = 0; z < colunas.length; z++){
			var points = colunas[z].getPoints();
			if (ptsLinha[0].y == points[0].y && ptsLinha[1].x == points[1].x) return z;
		}

		return -1;
        }

	function findLinhaPerpendicular(ptsColuna){
                for (var z = 0; z < linhas.length; z++){
                        var points = linhas[z].getPoints();
                        if (ptsColuna[1].x == points[1].x && ptsColuna[1].y == points[1].y) return z;
                }

                return -1;
        }

	// Usada
	function salvarAlteracoes() {

		linhas.sort(sortLinesFunction);
		colunas.sort(sortColumnsFunction);

		var segmento;

		var segmentosASalvar = new Array();

		for (var i = 0; i < colunas.length; i++){
			// Recupera os pontos da linha.
			var coluna = colunas[i].getPoints();

			// Transformação para o padrão "[ x1, y1, x2, y2]".
			segmento = [ coluna[0].x, coluna[0].y, coluna[1].x, coluna[1].y ];
		
			// Se o final da coluna estiver tocando a borda acima do zoom, 
			// significa que a coluna está fora do zoom e não deve ser salva.
			if ( segmento[3] == zoom[1] ) continue;

			// Se o início da coluna estiver tocando a borda abaixo do zoom, 
		        // significa que a coluna está fora do zoom e não deve ser salva.
		        if ( segmento[1] == zoom[3] ) continue;

			// Se o início da coluna estiver acima da borda de cima do zoom, 
		        // significa que a coluna deve ser redimensionada.
		        if ( segmento[1] < zoom[1] ) segmento[1] = zoom[1];

			// Se o final da coluna estiver abaixo da borda de baixo do zoom, 
		        // significa que a coluna deve ser redimensionada.
		        if ( segmento[3] > zoom[3] ) segmento[3] = zoom[3];

			// Adiciona a coluna aos segmentos que devem ser salvos.
			segmentosASalvar.push(segmento);
		}

		for (var i = 0; i < linhas.length; i++){
			// Recupera os pontos da coluna.
			var linha = linhas[i].getPoints();

			// Transformação para o padrão "[ x1, y1, x2, y2]".
		        segmento = [ linha[0].x, linha[0].y, linha[1].x, linha[1].y ];
		        
			// Se a linha estiver acima da borda superior do zoom, significa
			// que a linha está fora do zoom e não deve ser salva.
		        if ( segmento[1] < zoom[1] ) continue;

			// Se a linha estiver abaixo da borda inferior do zoom, significa
		        // que a linha está fora do zoom e não deve ser salva.
		        if ( segmento[3] > zoom[3] ) continue;

			// Como as linhas, com exceção das que fazem parte das bordas
			// sempre pertencem ao zoom, elas não precisam ser redimensionadas.
			// Resta, então, apenas salvá-las.
			segmentosASalvar.push(segmento);
		}

		return segmentosASalvar;
	}

	// Usada 
	function clearCanvas() {
		stage.removeChildren();
		stage.remove();
	}
