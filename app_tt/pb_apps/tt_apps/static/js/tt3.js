$('body').on('contextmenu', '#container', function(e){ return false; });
	var linhas = new Array();
	var colunas = new Array();
	var arr = new Array();
	var minX;
	var maxX;
	var minY;
	var maxY;
	var leftX;
	var rightX;
	var upperY;
	var bottomY;
	var horizontal = 1;
	var vertical = 2;
	var posUnidas = new Array();

	var i = 0;
	var j = 0;

	var stage = new Kinetic.Stage({
		container : 'container',
		width : 800,
		height : 800
	});

	var layer = new Kinetic.Layer();

	function isLinha(pts){
		return pts[0].y == pts[1].y;	
	}
	
	function isLinhaDaBorda(pts){
		return isLinha(pts) && pts[0].y == maxY;
	}
	
	function isColuna(pts){
		return pts[0].x == pts[1].x;	
	}
	
	function isColunaDaBorda(pts){
		return isColuna(pts) && pts[0].x == maxX;
	}
	
	function salvarAlteracoes() {
		var leftX;
		var rightX;
		var upperY;
		var bottomY;
		var primeiraLinha;
		var pts;
		var z = 0;

		var resultado = new Array();

		var limite = linhas.length;
		while (linhas.length > 0 && z < limite) {
			primeiraLinha = linhas[z];
			pts = primeiraLinha.getPoints();
			if (isLinhaDaBorda(pts) || isColuna(pts)) {
				z++;
			} else {

				leftX = pts[0].x;
				upperY = pts[0].y;
				rightX = null;
				bottomY = null;

				rightX = encontraRightX(leftX, upperY);
				bottomY = encontraBottomY(leftX, upperY);
				if (rightX == null || bottomY == null) {
					linhas.splice(z, 1);
				} else {
					resultado.push([ leftX, upperY, rightX, bottomY ]);
				}
			}
			limite = linhas.length;
		}

		return resultado;
	}

	function isBorda(pontos) {
		return ((pontos[0].x == pontos[1].x && (pontos[0].x == maxX || pontos[0].x == minX)) || (pontos[0].y == pontos[1].y && (pontos[0].y == maxY || pontos[0].y == minY)));
	}

	function isPosBorda(pontos) {
		return ((pontos[0] == pontos[2] && (pontos[0] == maxX || pontos[0] == minX)) || (pontos[1] == pontos[3] && (pontos[1] == maxY || pontos[1] == minY)));
	}

	function encontraRightX(leftX, upperY) {
		var z;
		var pts;
		var segmentoAtual;
		segmentoAtual = buscaSegmentoAtual(leftX, upperY, 1);
		while (segmentoAtual != null && !contemCorte(segmentoAtual, 1)) {
			leftX = segmentoAtual.getPoints()[1].x;
			removeSegmento(segmentoAtual);
			segmentoAtual = buscaSegmentoAtual(leftX, upperY, 1);
		}
		if (segmentoAtual != null) {
			removeSegmento(segmentoAtual);
			return segmentoAtual.getPoints()[1].x;
		}
		return null;
	}

	function removeSegmento(segmento) {
		var z;
		var pts1 = segmento.getPoints();
		var pts2;
		var arr1 = [ pts1[0].x, pts1[0].y, pts1[1].x, pts1[1].y ];
		for (z = linhas.length - 1; z >= 0; z--) {
			pts2 = linhas[z].getPoints();
			if (pts1[0].x == pts2[0].x && pts1[0].y == pts2[0].y
					&& pts1[1].x == pts2[1].x && pts1[1].y == pts2[1].y) {
				linhas.splice(z, 1);
			}
		}

	}

	function contemCorte(segmento, orientacao) {
		var pts1 = segmento.getPoints();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (orientacao == 1 && pts1[1].x == pts2[0].x && pts1[0].y == pts2[0].y
					&& pts2[0].x == pts2[1].x) {
				return true;
			}
			if (orientacao == 2 && pts1[1].y == pts2[0].y && pts1[0].x == pts2[0].x
					&& pts2[0].y == pts2[1].y) {
				return true;
			}
		}
		return false;
	}

	function buscaSegmentoAtual(leftX, upperY, orientacao) {
		for ( var z = 0; z < linhas.length; z++) {
			var pts = linhas[z].getPoints();
			if (orientacao == horizontal && pts[0].x == leftX && pts[0].y == upperY
					&& pts[0].y == pts[1].y) {
				return linhas[z];
			}
			if (orientacao == vertical && pts[0].x == leftX && pts[0].y == upperY
					&& pts[0].x == pts[1].x) {
				return linhas[z];
			}
		}
		return null;
	}

	function encontraBottomY(leftX, upperY) {
		var z;
		var pts;
		var segmentoAtual;
		segmentoAtual = buscaSegmentoAtual(leftX, upperY, 2);
		while (segmentoAtual != null && !contemCorte(segmentoAtual, 2)) {
			upperY = segmentoAtual.getPoints()[1].y;
			removeSegmento(segmentoAtual);
			segmentoAtual = buscaSegmentoAtual(leftX, upperY, 2);
		}
		if (segmentoAtual != null) {
			removeSegmento(segmentoAtual);
			return segmentoAtual.getPoints()[1].y;
		}
		return null;
	}

	function isColunaMovivel(newX) {
		for (i = 0; i < linhas.length; i++) {
			pts = linhas[i].getPoints();
			if (pts[0].x == pts[1].x && pts[0].x == newX) {
				return false;
			}
		}
		return true;
	}
	function isSegmentoColunaMovivel(pts, newX) {
		for (i = 0; i < linhas.length; i++) {
			pts2 = linhas[i].getPoints();
			if (pts2[0].x == pts2[1].x && pts2[0].x == newX) {
				if ((pts[0].y < pts2[1].y && pts[0].y > pts2[0].y)
						|| (pts[1].y < pts2[1].y && pts[1].y > pts2[0].y)) {
					return false;
				}
			}
		}
		return true;
	}

	function isLinhaMovivel(newY) {
		for (i = 0; i < linhas.length; i++) {
			pts = linhas[i].getPoints();
			if (pts[0].y == pts[1].y && pts[0].y == newY) {
				return false;
			}
		}
		return true;
	}

	function isSegmentoLinhaMovivel(pts, newY) {
		for (i = 0; i < linhas.length; i++) {
			pts2 = linhas[i].getPoints();
			if (pts2[0].y == pts2[1].y && pts2[0].y == newY) {
				if ((pts[0].x < pts2[1].x && pts[0].x > pts2[0].x)
						|| (pts[1].x < pts2[1].x && pts[1].x > pts2[0].x)) {
					return false;
				}
			}
		}
		return true;
	}
	function moverLinha(posY, newPosY) {
		if (!isPosBorda([ minX, posY, maxX, posY ])) {
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

	function moverColuna(posX, newPosX) {
		if (!isPosBorda([ posX, minY, posX, maxY ])) {
			for (i = 0; i < linhas.length; i++) {
				var pts = linhas[i].getPoints();
				if (pts[0].x == pts[1].x && pts[0].x == posX) {
					atualizaSegmentosAdjacentes(pts, [ newPosX, pts[0].y, newPosX,
							pts[1].y ]);
					linhas[i].setPoints([ newPosX, pts[0].y, newPosX, pts[1].y ]);
				}
			}
		}
	}

	function moverSegmento(ptsAntes, ptsDepois) {
		if (!isBorda(ptsAntes)) {
			for (i = 0; i < linhas.length; i++) {
				var pts = linhas[i].getPoints();
				if (pts[0].x == ptsAntes[0].x && pts[0].y == ptsAntes[0].y
						&& pts[1].x == ptsAntes[1].x && pts[1].y == ptsAntes[1].y) {
					atualizaSegmentosAdjacentes(pts, ptsDepois);
					linhas[i].setPoints(ptsDepois);
				}
			}
		}
	}

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
	}

	function verificaExistenciaLinha(pontos) {
		for ( var t = 0; t < linhas.length; t++) {
			var pts = linhas[t].getPoints();
			if (pts[0].x == pontos[0] && pts[0].y == pontos[1]
					&& pts[1].x == pontos[2] && pts[1].y == pontos[3]) {
				return true;
			}
		}
		return false;
	}

	function adicionarNovaLinha() {
		var posY = Math.round((maxY - minY) / 2);
		while (temLinha(posY) && posY < maxY) {
			posY += 5;
		}
		var intercessoes = encontraIntercessoesVerticais(posY);
		for ( var z = 0; z < intercessoes.length - 1; z++) {
			var pontos = [ intercessoes[z], posY, intercessoes[z + 1], posY ];
			adicionarLinha(pontos);
			atualizarIntercessao(pontos);
		}
	}

	function adicionarNovaColuna() {
		var posX = Math.round((maxX - minX) / 2);
		while (temLinha(posX) && posX < maxX) {
			posX += 5;
		}
		var intercessoes = encontraIntercessoesHorizontais(posX);
		for ( var z = 0; z < intercessoes.length - 1; z++) {
			var pontos = [ posX, intercessoes[z], posX, intercessoes[z + 1] ];
			adicionarLinha(pontos);
			atualizarIntercessao(pontos);
		}
	}

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

	function atualizarIntercessao(pontos) {
		var pts2;
		var aAdicionar = new Array();
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pontos[1] == pontos[3]) {
				if (pts2[0].x == pts2[1].x) {
					if (pontos[0] <= pts2[0].x && pontos[2] >= pts2[1].x
							&& pts2[0].y < pontos[1] && pts2[1].y > pontos[1]) {
						linhas[z].setPoints([ pts2[0].x, pts2[0].y, pts2[1].x,
								pontos[1] ]);
						aAdicionar.push([ pts2[0].x, pontos[1], pts2[1].x,
								pts2[1].y ]);
					}
				}
			} else if (pontos[0] == pontos[2]) {
				if (pts2[0].y == pts2[1].y) {
					if (pontos[1] <= pts2[0].y && pontos[3] >= pts2[1].y
							&& pts2[0].x < pontos[0] && pts2[1].x > pontos[2]) {
						linhas[z].setPoints([ pts2[0].x, pts2[0].y, pontos[0],
								pts2[1].y ]);
						aAdicionar.push([ pontos[0], pts2[0].y, pts2[1].x,
								pts2[1].y ]);
					}
				}
			}
		}
		for ( var w = 0; w < aAdicionar.length; w++) {
			adicionarLinha(aAdicionar[w]);
		}
	}

	function encontraIntercessoesVerticais(altura) {
		var intercessoes = new Array();
		for ( var z = 0; z < linhas.length; z++) {
			var pts2 = linhas[z].getPoints();
			if (pts2[0].x == pts2[1].x) {
				if (pts2[0].y <= altura && pts2[1].y >= altura) {
					if (($.inArray(pts2[0].x, intercessoes)) == -1) {
						intercessoes.push(pts2[0].x);
					}
				}
			}
		}
		intercessoes.sort(function(a, b) {
			return a - b
		});
		return intercessoes;
	}

	function encontraIntercessoesHorizontais(distancia) {
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
			return a - b
		});
		return intercessoes;
	}

	function adicionarLinha(pontos) {
		var linha = new Kinetic.Line({
			points : pontos,
			stroke : 'red',
			draggable : true,
			strokeWidth : 2,
			dragBoundFunc : function(pos, event) {
				var points = this.getPoints();
				if (points[0].x == points[1].x) {
					var posX = event.offsetX == undefined ? event.layerX
							: event.offsetX;
					var limEsq = encontraLimiteEsquerda(points[0].x);
					var limDir = encontraLimiteDireita(points[0].x);
					var newX = posX < limEsq ? limEsq : (posX > limDir ? limDir
							: posX);
					if (isColunaMovivel(newX)) {
						moverColuna(points[0].x, newX);
					}
				} else {
					var posY = event.offsetY == undefined ? event.layerY
							: event.offsetY;
					var limSup = encontraLimiteSuperior(points[0].y);
					var limInf = encontraLimiteInferior(points[0].y);
					var newY = posY < limSup ? limSup : (posY > limInf ? limInf
							: posY);
					if (isLinhaMovivel(newY)) {
						moverLinha(points[0].y, newY);
					}
				}

				return {
					x : 0,
					y : 0
				}
			}
		});
		var pts = linha.getPoints();
		if (pts[0].x == pts[1].x) {
			linha.on("mouseover", function() {
				document.body.style.cursor = "ew-resize";
				layer.draw();
			});
		} else {
			linha.on("mouseover", function() {
				document.body.style.cursor = "ns-resize";
				layer.draw();
			});
		}

		linha.on("mouseout", function() {
			document.body.style.cursor = "default";
			layer.draw();
		});

		linha.on("mouseover touchstart", function() {
			var points = this.getPoints();
			if (points[0].x == points[1].x) {
				var z;
				for (z = 0; z < linhas.length; z++) {
					var points2 = linhas[z].getPoints();
					if (points2[0].x == points2[1].x
							&& points[0].x == points2[0].x) {
						linhas[z].setStroke('green');
					}
				}
			} else if (points[0].y == points[1].y) {
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
		linha.on('mouseout touchend', function() {
			for (i = 0; i < linhas.length; i++) {
				linhas[i].setStroke('red');
			}
			layer.draw();
		});
		linhas.push(linha);
		layer.add(linha);
		stage.add(layer);
	}

	function encontraLimiteSuperior(posY) {
		var posicoesY = new Array();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].y == pts2[1].y && pts2[0].y < posY) {
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
	
	function encontraLimiteEsquerda(posX) {
		var posicoesX = new Array();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].x == pts2[1].x && pts2[0].x < posX) {
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

	function encontraLimiteInferior(posY) {
		var posicoesY = new Array();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].y == pts2[1].y && pts2[0].y > posY) {
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

	function encontraLimiteDireita(posX) {
		var posicoesX = new Array();
		var pts2;
		for ( var z = 0; z < linhas.length; z++) {
			pts2 = linhas[z].getPoints();
			if (pts2[0].x == pts2[1].x && pts2[0].x > posX) {
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
	
	function uneIntercessaoColuna(posX, posY){
		var pos1;
		var pos3;
		
		var z;
		
		for (z = linhas.length - 1; z >= 0; z--){
			var points2 = linhas[z].getPoints();
			if (isColuna(points2) && points2[0].x == posX){
				if (points2[0].y == posY){
					pos3 = points2[1].y;
					linhas[z].remove();
					linhas.splice(z, 1);
				}
				if (points2[1].y == posY){
					pos1 = points2[0].y;
					linhas[z].remove();
					linhas.splice(z, 1);
				}
			}
		}
		adicionarLinha([posX, pos1, posX, pos3]);
	}
	
	function uneIntercessaoLinha(posX, posY){
		var pos0;
		var pos2;
		
		var z;
		
		for (z = linhas.length - 1; z >= 0; z--){
			var points2 = linhas[z].getPoints();
			if (isLinha(points2) && points2[0].y == posY){
				if (points2[0].x == posX){
					pos2 = points2[1].x;
					linhas[z].remove();
					linhas.splice(z, 1);
				}
				if (points2[1].x == posX){
					pos0 = points2[0].x;
					linhas[z].remove();
					linhas.splice(z, 1);
				}
			}
		}
		adicionarLinha([pos0, posY, pos2, posY]);
	}
	
	function uneIntercessoes(points){
		var pos1, pos2;
		if (isLinha(points)){
			pos0 = points[0].x;
			pos1 = points[1].x;
			var posY = points[0].y;
			var t = $.inArray(pos0, posUnidas);
			if (t == -1){
				uneIntercessaoColuna(pos0, posY);
				posUnidas.push(pos0);
			}
			t = $.inArray(pos1, posUnidas);
			if (t == -1) {
				uneIntercessaoColuna(pos1, posY);
				posUnidas.push(pos1);
			}
		}
		else {
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

	function initGrid(matrizDePontos, uri) {
		minX = 2000;
		minY = 2000;
		maxX = 0;
		maxY = 0;

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

			for ( var z = 0; z < novasLinhas.length; z++) {
				if (!verificaExistenciaLinha(novasLinhas[z])) {
					adicionarLinha(novasLinhas[z]);
				}
			}
		}

		layer.on('click', function(evt) {

			// Codigo para remover todos os segmentos que pertencam a uma mesma
			// linha
			//if (removendoLinha) {
			if ((evt.which && evt.which == 3) || (evt.button && evt.button == 2)) {
				posicoesUnidas = new Array();
				// Recupera o objeto que foi clicado
				var shape = evt.shape;
				var points = shape.getPoints();
				if (!isBorda(points)) {

					if (points[0].x == points[1].x) {

						// E necessario fazer iteracao inversa sobre o array para
						// nao pular nenhum elemento.
						for (i = linhas.length - 1; i >= 0; i--) {
							var points2 = linhas[i].getPoints();
							if (points2[0].x == points[0].x
									&& points2[1].x == points[1].x) {
								linhas[i].remove();
								linhas.splice(i, 1);
								//Finalmente, atualizamos todas aquelas intercessões que não são mais cruzadas.
								uneIntercessoes(points2);
							}
						}
					} else if (points[0].y == points[1].y) {
						for (i = linhas.length - 1; i >= 0; i--) {
							var points2 = linhas[i].getPoints();
							if (points2[0].y == points[0].y
									&& points2[1].y == points[1].y) {
								linhas[i].remove();
								linhas.splice(i, 1);
								//Finalmente, atualizamos todas aquelas intercessões que não são mais cruzadas.
								uneIntercessoes(points2);
							}
						}
					}
					
				}
			}
			// Apos remover os objetos selecionados, redesenhamos a camada apenas
			// com os objetos restantes.
			layer.draw();
		});
		var imageObj = new Image();
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

		};
		imageObj.src = uri;
	}

	function clearCanvas() {
		layer.remove();
	}
