var linhas = new Array();
var arr = new Array();
var matrizDePontos = new Array();
var coordenadasOriginais = new Array();
var resultado;
var removendo = true;
var movendo = false;
var removendoLinha = false;
var movendoLinha = false;
var minX;
var maxX;
var minY;
var maxY;
var leftX;
var rightX;
var upperY;
var bottomY;

var i = 0;
var j = 0;

var stage = new Kinetic.Stage({
    container : 'container',
    width : 800,
    height : 800
});

var layer = new Kinetic.Layer();

function salvarAlteracoes(){
    var leftX;
    var rightX;
    var upperY;
    var bottomY;
    var primeiraLinha;
    var pts;
    var z = 0;

    resultado = new Array();

    resultado.push(coordenadasOriginais);
    
    while (linhas.length > 0 && z < linhas.length){
        primeiraLinha = linhas[z];
        pts = primeiraLinha.getPoints();
        if (isBorda(pts)) {
            z++;
        } else {
            
            leftX = pts[0].x;
            upperY = pts[0].y;
            rightX = pts[1].x;
            bottomY = pts[1].y;

            rightX = encontraRightX(leftX, upperY);
            bottomY = encontraBottomY(leftX, upperY);
            if (rightX == null || bottomY == null){
                linhas.splice(0,1);
            } else {
                resultado.push([leftX, upperY, rightX, bottomY]);
            }
        }
    }
    return resultado;
}

function isBorda(pontos){
    var l;
    var pts;
    for (l=0; l<linhas.length; l++){
        pts = linhas[l].getPoints();
        if (pontos[0].x == pontos[1].x && pts[1].x > pontos[1].x){
            return false;
        }
        if (pontos[0].y == pontos[1].y && pts[1].y > pontos[1].y){
            return false;
        }
    }
    return true;
}

function encontraRightX(leftX, upperY){
    var z;
    var pts;
    var segmentoAtual;
    segmentoAtual = buscaSegmentoAtual(leftX, upperY, 1);
    while (segmentoAtual != null && !contemCorte(segmentoAtual, 1)) {
        leftX = segmentoAtual.getPoints()[1].x;
        removeSegmento(segmentoAtual);
        segmentoAtual = buscaSegmentoAtual(leftX, upperY, 1);
    }
    if (segmentoAtual != null){
        removeSegmento(segmentoAtual);
        return segmentoAtual.getPoints()[1].x;
    }
    return null;
}

function removeSegmento(segmento){
    var z;
    var pts1 = segmento.getPoints();
    var pts2;
    var arr1 = [pts1[0].x, pts1[0].y, pts1[1].x, pts1[1].y];
    for (z = linhas.length-1; z>=0; z--){
        pts2 = linhas[z].getPoints();
        if (pts1[0].x == pts2[0].x && pts1[0].y == pts2[0].y && pts1[1].x == pts2[1].x && pts1[1].y == pts2[1].y){
            linhas.splice(z, 1);
        }
    }
    
}

function contemCorte(segmento, orientacao){
    var pts1 = segmento.getPoints();
    var pts2;
    for (var z = 0; z < linhas.length; z++){
        pts2 = linhas[z].getPoints();
        if (orientacao == 1 && pts1[1].x == pts2[0].x && pts1[0].y == pts2[0].y && pts2[0].x == pts2[1].x){
            return true;
        }
        if (orientacao == 2 && pts1[1].y == pts2[0].y && pts1[0].x == pts2[0].x && pts2[0].y == pts2[1].y){
            return true;
        }
    }
    return false;
}

function buscaSegmentoAtual(leftX, upperY, orientacao){
    for (var z = 0; z < linhas.length; z++){
        var pts = linhas[z].getPoints();
        if (orientacao == 1 && pts[0].x == leftX && pts[0].y == upperY && pts[0].y == pts[1].y){
            return linhas[z];
        }
        if (orientacao == 2 && pts[0].x == leftX && pts[0].y == upperY && pts[0].x == pts[1].x){
            return linhas[z];
        }
    }
    return null;
}

function encontraBottomY(leftX, upperY){
    var z;
    var pts;
    var segmentoAtual;
    segmentoAtual = buscaSegmentoAtual(leftX, upperY, 2);
    while (segmentoAtual != null && !contemCorte(segmentoAtual, 2)) {
        upperY = segmentoAtual.getPoints()[1].y;
        removeSegmento(segmentoAtual);
        segmentoAtual = buscaSegmentoAtual(leftX, upperY, 2);
    }
    if (segmentoAtual != null){
        removeSegmento(segmentoAtual);
        return segmentoAtual.getPoints()[1].y;
    }
    return null;
}

function isColunaMovivel(newX){
    for (i=0; i<linhas.length; i++){
        pts = linhas[i].getPoints();
        if (pts[0].x == pts[1].x && pts[0].x == newX){
            return false;
        }
    }
    return true;
}
function isSegmentoColunaMovivel(pts, newX){
    for (i=0; i<linhas.length; i++){
        pts2 = linhas[i].getPoints();
        if (pts2[0].x == pts2[1].x && pts2[0].x == newX){
            if ((pts[0].y < pts2[1].y && pts[0].y > pts2[0].y) || (pts[1].y < pts2[1].y && pts[1].y > pts2[0].y)) {
                return false;
            }
        }
    }
    return true;
}

function isLinhaMovivel(newY){
    for (i=0; i<linhas.length; i++){
        pts = linhas[i].getPoints();
        if (pts[0].y == pts[1].y && pts[0].y == newY){
            return false;
        }
    }
    return true;
}

function isSegmentoLinhaMovivel(pts, newY){
    for (i=0; i<linhas.length; i++){
        pts2 = linhas[i].getPoints();
        if (pts2[0].y == pts2[1].y && pts2[0].y == newY){
            if ((pts[0].x < pts2[1].x && pts[0].x > pts2[0].x) || (pts[1].x < pts2[1].x && pts[1].x > pts2[0].x)) {
                return false;
            }
        }
    }
    return true;
}
function moverLinha(posY, newPosY){
    for (i=0; i < linhas.length; i++){
        var pts = linhas[i].getPoints();
        if (pts[0].y == pts[1].y && pts[0].y == posY){
            linhas[i].setPoints([pts[0].x, newPosY, pts[1].x, newPosY]);
        }
    }
}

function moverColuna(posX, newPosX) {
    for (i=0; i < linhas.length; i++){
        var pts = linhas[i].getPoints();
        if (pts[0].x == pts[1].x && pts[0].x == posX){
            linhas[i].setPoints([newPosX, pts[0].y, newPosX, pts[1].y]);
        }
    }
}

function verificaExistenciaLinha(pontos){
    for (var t=0; t<linhas.length; t++){
        var pts = linhas[t].getPoints();
        if (pts[0].x == pontos[0] && pts[0].y == pontos[1] && pts[1].x == pontos[2] && pts[1].y == pontos[3]){
            return true;
        }
    }
    return false;
}

$(document).ready(function() {

    $(".remover").click(function() {
        removendo = true;
        movendo = false;
        removendoLinha = false;
        movendoLinha = false;
    });

    $(".mover").click(function() {
        removendo = false;
        movendo = true;
        removendoLinha = false;
        movendoLinha = false;
    });

    $(".removerLinha").click(function() {
        removendo = false;
        movendo = false;
        removendoLinha = true;
        movendoLinha = false;
    });

    $(".moverLinha").click(function() {
        removendo = false;
        movendo = false;
        removendoLinha = false;
        movendoLinha = true;
    });
});


function initGrid(matrizDePontos, uri) {
    minX = 2000;
    minY = 2000;
    maxX = 0;
    maxY = 0;
    
    for (i = 0; i < matrizDePontos.length; i++) {
        arr = matrizDePontos[i];
        
        leftX = arr[0];
        if (leftX < minX){ minX = leftX; }
        upperY = arr[1];
        if (upperY < minY){ min = upperY;}
        rightX = arr[2];
        console.log("RightX: " + rightX + "MaxX: " + maxX);
        
        if (rightX > maxX){ 
            maxX = rightX;
            console.log("Dentro do if: " + rightX);
        }
        bottomY = arr[3];
        if (bottomY > maxY){ maxY = bottomY;}
        
        var novasLinhas = new Array();
        novasLinhas.push([leftX, upperY, leftX, bottomY]);
        novasLinhas.push([rightX, upperY, rightX, bottomY]);
        novasLinhas.push([leftX, upperY, rightX, upperY]);
        novasLinhas.push([leftX, bottomY, rightX, bottomY]);

        for (var z=0; z<novasLinhas.length; z++){
            if (!verificaExistenciaLinha(novasLinhas[z])){
                var linha = new Kinetic.Line({
                    points : novasLinhas[z],
                    stroke : 'red',
                    draggable : false,
                    strokeWidth : 2,
                    dragBoundFunc: function(pos, event) {
                        var points = this.getPoints();
                        if (points[0].x == points[1].x){
                            var posX = event.offsetX;
                            var newX = posX < minX ? minX : (posX > maxX ? maxX : posX);
                            if (movendoLinha) {
                                if(isColunaMovivel(newX)){
                                    moverColuna(points[0].x, newX);
                                    this.setPoints([newX, points[0].y, newX, points[1].y]);
                                }
                            }
                            else{
                                if(isSegmentoColunaMovivel(points, newX)){
                                    this.setPoints([newX, points[0].y, newX, points[1].y]);
                                }
                            }
                            return {
                                x: this.getAbsolutePosition().x,
                                y: this.getAbsolutePosition().y
                            }
                        } else {
                            var posY = event.offsetY;
                            var newY = posY < minY ? minY : (posY > maxY ? maxY : posY);
                            if (movendoLinha) {
                                if (isLinhaMovivel(newY)){
                                    moverLinha(points[0].y, newY);
                                    this.setPoints([points[0].x, newY, points[1].x, newY]);
                                }
                            }
                            else{
                                if (isSegmentoLinhaMovivel(points, newY)){
                                    this.setPoints([points[0].x, newY, points[1].x, newY]);
                                }
                            }
                            return {
                                x: this.getAbsolutePosition().x,
                                y: this.getAbsolutePosition().y
                            }
                        }
                    }
                });
                var pts= linha.getPoints();
                if (pts[0].x == pts[1].x) {
                    linha.on("mouseover", function() {
                        if (movendo || movendoLinha) {
                            document.body.style.cursor = "ew-resize";
                        } else if (removendo || removendoLinha) {
                            document.body.style.cursor = "pointer";
                            layer.draw();
                        }
                    });
                } else {
                    linha.on("mouseover", function() {
                        if (movendo || movendoLinha) {
                            document.body.style.cursor = "ns-resize";
                        } else if (removendo || removendoLinha) {
                            document.body.style.cursor = "pointer";
                            layer.draw();
                        }
                    });
                }

                linha.on("mouseout", function() {
                    document.body.style.cursor = "default";
                    layer.draw();
                });

                linha.on("mouseover touchstart", function() {
                    if (movendoLinha || removendoLinha) {
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
                    } else {
                        this.setStroke('green');
                    }

                    if (removendo || removendoLinha) {
                        this.setDraggable(false);
                    }
                    layer.draw();
                });
                linha.on('mouseout touchend', function() {
                    for (i = 0; i < linhas.length; i++) {
                        linhas[i].setStroke('red');
                    }
                    this.setDraggable(true);
                    layer.draw();
                });
                linhas.push(linha);
                layer.add(linha);
            }
        }
    }

    layer.on('click', function(evt) {

        //Cï¿½digo para remover apenas um segmento da tabela
        if (removendo) {
            
            // Recupera o objeto que foi clicado
            var shape = evt.shape;
            var points = shape.getPoints();

            // ï¿½ necessï¿½rio fazer iteraï¿½ï¿½o inversa sobre o array para nï¿½o pular nenhum elemento.
            for (i = linhas.length - 1; i >= 0; i--) {
                var points2 = linhas[i].getPoints();
                if (points2[0].x == points[0].x && 
                    points2[1].x == points[1].x && 
                    points2[0].y == points[0].y && 
                    points2[1].y == points[1].y) {

                    linhas[i].remove();
                    linhas.splice(i,1);
                }
            }
        }
        //Cï¿½digo para remover todos os segmentos que pertenï¿½am a uma mesma linha
        else if (removendoLinha) {

            // Recupera o objeto que foi clicado
            var shape = evt.shape;
            var points = shape.getPoints();
            if (points[0].x == points[1].x) {

                // ï¿½ necessï¿½rio fazer iteraï¿½ï¿½o inversa sobre o array para nï¿½o pular nenhum elemento.
                for (i = linhas.length - 1; i >= 0; i--) {
                    var points2 = linhas[i].getPoints();
                    if (points2[0].x == points[0].x
                            && points2[1].x == points[1].x) {
                        linhas[i].remove();
                        linhas.splice(i,1);
                    }
                }
            } else if (points[0].y == points[1].y) {
                for (i = linhas.length - 1; i >= 0; i--) {
                    var points2 = linhas[i].getPoints();
                    if (points2[0].y == points[0].y
                            && points2[1].y == points[1].y) {
                        linhas[i].remove();
                        linhas.splice(i,1);
                    }
                }
            }
        }
        // Apï¿½s remover os objetos selecionados, redesenhamos a camada apenas com os objetos restantes.
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
        console.log(tabela.width);

        // add the shape to the layer
        layer.add(tabela);
        tabela.moveToBottom();

        // add the layer to the stage

        stage.add(layer);

    };
    imageObj.src = uri;
}

function clearCanvas(){
    layer.remove();
}
