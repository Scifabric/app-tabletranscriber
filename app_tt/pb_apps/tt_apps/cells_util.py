# -*- coding: utf-8 -*-

def create_cells(lines, columns, maxX, maxY):
	lines = sorted(lines, key=lambda line: (line[1], line[0]))
	columns = sorted(columns, key=lambda column: (column[0], column[1]))

	lines = __splitLines(lines, columns)
	columns = __splitColumns(lines, columns)

	iteradorLinha = 0
	iteradorColuna = 0
	ptsLinha = lines[iteradorLinha]
	ptsColuna = columns[iteradorColuna]
	resultado = []

	while (__getInitY(ptsLinha) < maxY):

		leftX = __getInitX(ptsLinha)
		upperY = __getInitY(ptsLinha)

		# Procura pela linha limitada por uma coluna perpendicular.
		iteradorColuna = __findColunaPerpendicular(ptsLinha, columns)

		while (iteradorColuna == -1 and __getInitY(ptsLinha) == upperY):
			iteradorLinha += 1
			ptsLinha = lines[iteradorLinha]
			iteradorColuna = __findColunaPerpendicular(ptsLinha, columns)
	

		rightX = __getFinalX(ptsLinha)
		ptsColuna = columns[iteradorColuna]

		# Procura pela coluna limitada por uma linha perpendicular.
		while (__findLinhaPerpendicular(ptsColuna, lines) == -1 and __getInitX(ptsColuna) == rightX):
			iteradorColuna += 1
			ptsColuna = columns[iteradorColuna]
		

		bottomY = __getFinalY(ptsColuna)

		resultado.append([leftX, upperY, rightX, bottomY])
		iteradorLinha += 1
		ptsLinha = lines[iteradorLinha]
	

	#print("Length:" + str(len(resultado)))
	#print(resultado)
	return resultado

def __findColunaPerpendicular(ptsLinha, colunas):
	linY = __getInitY(ptsLinha)
	for i in range(0, len(colunas)):
		ptsColuna = colunas[i];
		colX = __getInitX(ptsColuna);

		if (linY == __getInitY(ptsColuna) and __getFinalX(ptsLinha) == colX):
			return i
	return -1


def __findLinhaPerpendicular(ptsColuna, linhas):
	colX = __getInitX(ptsColuna)
	for i in range(0, len(linhas)):
		ptsLinha = linhas[i];
		linY = __getInitY(ptsLinha);

		if (__getFinalY(ptsColuna) == linY and colX == __getFinalX(ptsLinha)):
			return i
	return -1


def __splitLines(lines, columns):
	splittedLines = []
	for i in range(0, len(lines)):
		line = lines[i]
		linY = __getInitY(line)
		intersections = __getColumnIntersections(line, columns)
	
		for j in range(0, len(intersections)-1):
			splittedLines.append([intersections[j], linY, intersections[j+1], linY])
	return splittedLines

def __splitColumns(lines, columns):
	splittedColumns = []
	for i in range(0, len(columns)):
		column = columns[i]
		colX = __getInitX(column)
		intersections = __getLineIntersections(column, lines)
	
		for j in range(0, len(intersections)-1):
			splittedColumns.append([colX, intersections[j], colX, intersections[j+1]])
	return splittedColumns

def __getColumnIntersections(line, columns):
	intersections = []
	linY = __getInitY(line)

	for i in range(0, len(columns)):
		column = columns[i]
		colX = __getInitX(column)

		if (__insideClosedInterval(__getInitY(column), __getFinalY(column), linY)
				 and __insideClosedInterval(__getInitX(line), __getFinalX(line), colX)):
			if (__findElementInArray(colX, intersections) == -1):
				intersections.append(colX);
	return intersections

def __getLineIntersections(column, lines):
	intersections = []
	colX = __getInitX(column)

	for i in range(0, len(lines)):
		line = lines[i]
		linY = __getInitY(line)

		if (__insideClosedInterval(__getInitX(line), __getFinalX(line), colX)
				 and __insideClosedInterval(__getInitY(column), __getFinalY(column), linY)):
			if (__findElementInArray(linY, intersections) == -1):
				intersections.append(linY);
	return intersections

def __insideClosedInterval(init, final, element):
	return element >= init and element <= final

def __findElementInArray(element, arr):
	for i in range(0, len(arr)):
		if (element == arr[i]):
			 return i
	return -1

def __getInitX(posArr):
	return posArr[0]

def __getInitY(posArr):
	return posArr[1]

def __getFinalX(posArr):
	return posArr[2]

def __getFinalY(posArr):
	return posArr[3]

