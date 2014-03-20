# -*- coding: utf-8 -*-

from app_tt.pb_apps.pb_task import pb_task
from app_tt.core import pbclient
import ttapps
from app_tt.core import app
from subprocess import call
import requests
import urllib2
from requests import RequestException
import json
import sys
import os
import cellsUtil
import math
from InvalidTaskGroupException import InvalidTaskGroupException
from operator import itemgetter, attrgetter
from app_tt.data_mngr import data_manager

"""
    Table transcriber tasks
    ~~~~~~~~~~~~~~~~~~~~~~
"""


class TTTask1(pb_task):
    """
    Table Transcriber Task type 1
    """
    def __init__(self, task_id, app_short_name):
        super(TTTask1, self).__init__(task_id, app_short_name)

    def add_next_task(self):
        # Verify the answer of the question to create a new task
        if(self.task.info["answer"] == "Yes"):
            info = dict(link=self.task.info["url_m"],
                        page=self.task.info["page"])
            tt2_app_short_name = self.app_short_name[:-1] + "2"
            tt2_app = ttapps.Apptt_meta(short_name=tt2_app_short_name)

            tt2_app.add_task(info)

    def close_task(self):
        pass

    def check_answer(self):
        task_runs = self.get_task_runs()
        N_ANSWER = 2
        answers = {}
        for taskrun in task_runs:
            answer = taskrun.info
            if(answer not in answers.keys()):
                answers[answer] = 1
            else:
                answers[answer] += 1

            if(answers[answer] == N_ANSWER and answer != "NotKnown"):
                self.task.info["answer"] = answer
                # put the answer into task info
                requests.put("%s/api/task/%s?api_key=%s" % (
                    app.config['PYBOSSA_URL'], self.task.id,
                    app.config['API_KEY']),
                    data=json.dumps(dict(info=self.task.info)))
                
                bookId = self.app_short_name[:-4]
                archiveURL = self.task.info["url_m"]
                page = self.task.info["page"]
                
                data_manager.record_page((bookId, archiveURL, page))
                
                return True
        return False

    def get_next_app(self):
        curr_app_name = self.app_short_name
        next_app_name = curr_app_name[:-1] + "2"
        return ttapps.Apptt_meta(short_name=next_app_name)


class TTTask2(pb_task):
    """
    Table Transcriber Task type 2
    """
    def __init__(self, task_id, app_short_name):
        super(TTTask2, self).__init__(task_id, app_short_name)

    def add_next_task(self):

        if (self.__checkIfNextTaskWasCreated()):
            return

        # Get the list of task_runs
        task_runs = json.loads(urllib2.urlopen(
            "%s/api/taskrun?task_id=%s&limit=%d" % (
                app.config['PYBOSSA_URL'], self.task.id, sys.maxint)).read())

        task_run = task_runs[len(task_runs) - 1]  # Get the last answer
        answer = task_run["info"]
        answer_json = json.loads(answer)

        if (answer != "0" and answer != "[]"):

            tt3_app_short_name = self.app_short_name[:-1] + "3"
            tt3_app = ttapps.Apptt_struct(short_name=tt3_app_short_name)

            bookId = self.app_short_name[:-4]
            imgId = self.task.info["page"]
            
            rotate = answer_json[0]["text"]["girar"]
                        
            self.__downloadArchiveImages(bookId, imgId)
            self.__runLinesRecognition(bookId, imgId, rotate)

            try:
                # file with the lines recognized
                arch = open(
                    "%s/books/%s/metadados/saida/image%s_model%s.txt" % (
                    app.config['CV_MODULES'], bookId, imgId, "1"))
                # get the lines recognitions
                tables_coords = self.__splitFile(arch)
                for tableId in range(len(tables_coords)):
                    self.__runAreaSelection(
                        bookId, imgId, tableId, rotate)

                    image_pieces = self.__getAreaSelection(
                        bookId, imgId, tableId)

                    if(len(image_pieces) > 0):
                        for image_piece in image_pieces:
                            info = dict(hasZoom=True, zoom=image_piece,
                                        coords=tables_coords[tableId],
                                        table_id=tableId,
                                        page=imgId, img_url=self.__url_table(
                                        bookId, imgId, tableId))
                            tt3_app.add_task(info)  # add task to tt3_backend
                    else:
                        info = dict(hasZoom=False,
                                    coords=tables_coords[tableId],
                                    table_id=tableId,
                                    page=imgId, img_url=self.__url_table(
                                    bookId, imgId, tableId))
                        tt3_app.add_task(info)

            except IOError:
                print "Error. File image%s_model%s.txt couldn't be opened" % (
                    imgId, "1")
            # TODO: the task will not be created,
            # routine to solve this must be implemented
            except Exception, e:
                print str(e)

    def __checkIfNextTaskWasCreated(self):
        page_num = self.task.info['page']
        tt3_app = self.get_next_app()
        tt3_tasks = tt3_app.get_tasks()

        for t in tt3_tasks:
            if (t.info['page'] == page_num):
                return True
        return False

    def close_task(self):
        pass

    def check_answer(self):
        task_runs = self.get_task_runs()
        n_taskruns = len(task_runs)  # task_runs goes from 0 to n-1
        
        if(n_taskruns > 1):
            answer1 = task_runs[n_taskruns - 1].info
            answer2 = task_runs[n_taskruns - 2].info
            answer1_json = json.loads(answer1)
            answer2_json = json.loads(answer2)
    
            if self.__compare_answers(answer1_json, answer2_json):
                if answer2 != "0" and answer2 != "[]":
                    return self.__fileOutput(answer2_json)
                elif answer2 == "0":  # There is one error at TTTask1 answer
                    pass
        else:
            return False

    def __compare_answers(self, answer1, answer2):
        threshold = 2
        
        if len(answer1) != len(answer2):
                return False
    
        for i in range(0, len(answer1)):
            table1 = answer1[i]
            table2 = answer2[i]
    
            for answer_type in table1.keys():
                a1_value = table1[answer_type]
                a2_value = table2[answer_type]
                if answer_type in ["top", "left", "width", "height"]:
                    if a2_value < (a1_value - threshold) or a2_value > (a1_value + threshold):
                        return False
                else:
                    if a1_value != a2_value:
                        return False
        return True

    def get_next_app(self):
        curr_app_name = self.app_short_name
        next_app_name = curr_app_name[:-1] + "3"
        return ttapps.Apptt_struct(short_name=next_app_name)

    def __downloadArchiveImages(self, bookId, imgId, width=550, height=700, max_width=1650, max_height=2100):
        """
        Download internet archive images to tt3_backend project
        :returns: True if the download was successful
        :rtype: bool
        """

        try:
            archiveURL = "http://archive.org/download/%s/page/n%s_w%s_h%s" % (
                bookId, imgId, max_width, max_height)
            
            url_request = requests.get(archiveURL)

            fullImgPath = "%s/books/%s/alta_resolucao/image%s" % (
                app.config['CV_MODULES'], bookId, imgId)
            fullImgPathJPG = fullImgPath + ".jpg"
            fullImgPathPNG = fullImgPath + ".png"

            fullImgFile = open(fullImgPathJPG, "w")
            fullImgFile.write(url_request.content)
            fullImgFile.close()
    
            # shell command to convert jpg to png
            command = 'convert %s -resize %dx%d! %s; rm %s; ' % (
                fullImgPathJPG, max_width, max_height, fullImgPathPNG, fullImgPathJPG)

            # create image with low resolution
            lowImgPath = "%s/books/%s/baixa_resolucao/image%s" % (
                app.config['CV_MODULES'], bookId, imgId)
            lowImgPathPNG = lowImgPath + ".png"

            command += 'convert %s -resize %dx%d! %s' % (
                fullImgPathPNG, width, height, lowImgPathPNG)

            print("Command: " + command)
            call([command], shell=True)  # calls the shell command
            
            return True
        except IOError, e:
            print str(e)
        # TODO: Implement strategies for exceptions cases
        except RequestException, e:
            print str(e)
        except Exception, e:
            print str(e)

        return False

    def __runLinesRecognition(self, bookId, imgId, rotate, model="1"):
        """
        Call cpp software that recognizes lines into the table and
        writes lines coords into \
        <tt3_backend_dir>/books/bookId/metadados/saida/image<imgId>.txt

        :returns: True if the write was successful
        :rtype: bool
        """
        # command shell to enter into the tt3 backend project and
        # calls the lines recognizer software

        if rotate:  # rotated table
            rotate = "-r"
            command = 'cd %s/TableTranscriber2/; ./tabletranscriber2 ' \
            '"/books/%s/baixa_resolucao/image%s.png" "model%s" "%s"' % (
            app.config['CV_MODULES'], bookId, imgId, model, rotate)
            
            print("command: " + command)
            
            call([command], shell=True)  # calls the shell command
            # TODO: implements exception strategy
        
        else:  # not rotated table
            rotate = "-nr"
            command = 'cd %s/TableTranscriber2/; ./tabletranscriber2 ' \
            '"/books/%s/baixa_resolucao/image%s.png" "model%s" "%s"' % (
            app.config['CV_MODULES'], bookId, imgId, model, rotate)
            
            print("command: " + command)
            
            call([command], shell=True)  # calls the shell command
            # TODO: implements exception strategy
            
        return self.__checkFile(bookId, imgId)

    def __checkFile(self, bookId, imgId):
        directory = "%s/books/%s/metadados/saida/" % (
            app.config['CV_MODULES'], bookId)
        output_files = os.listdir(directory)
        images = [f.split('_')[0] for f in output_files]

        return ("image%s" % imgId) in images

    def __runAreaSelection(self, bookId, imgId, tableId, rotate):
        """
        Call cpp ZoomingSelector software that splits the
        tables and write the pieces at
        <tt3_backend_id>/books/bookId/selections/image<imgId>_tableId.txt

        :returns: True if the execution was ok
        :rtype: bool
        """
        
        command = 'cd %s/ZoomingSelector/; ./zoomingselector ' \
        '"/books/%s/metadados/tabelasAlta/image%s_%d.png"' % (
        app.config['CV_MODULES'], bookId, imgId, tableId)
        
        call([command], shell=True)

    def __getAreaSelection(self, bookId, imgId, tableId):

        selections = []

        try:
            filepath = "%s/books/%s/selections/image%s_%d.txt" % (
                app.config['CV_MODULES'], bookId, imgId, tableId)
            arch = open(filepath)
            data = arch.read().strip().split('\n')

            for data_idx in range(1, len(data)):
                selections.append([
                    int(coord) for coord in data[data_idx].split(',')])

        except IOError:
            print "Error! Couldn't open" \
                "image%s_%d.txt selection file" % (
                imgId, tableId)

        except Exception, e:
            print str(e)

        return selections

    def __url_table(self, bookId, imgId, idx):
        """""
        Build a url of a splited image for the lines recognizer
        :returns: a indexed book table image
        :rtype: str
        """
        return "%s/books/%s/metadados/tabelasBaixa/image%s_%d.png" % (
            app.config['URL_TEMPLATES'], bookId, imgId, idx)

    def __splitFile(self, arch):
        """""
        Splits a given file and return a matrices list \
        where the lines with '#' are the index and the other \
        lines with values separated with ',' are the vectors \
        of the inner matrices

        :returns: a list of matrix
        :rtype: list
        """

        strLines = arch.read().strip().split("\n")
        matrix = []
        matrix_index = -1

        for line in strLines:
            if line.find("#") != -1:
                matrix_index += 1
                matrix.append([])
            else:
                line = line.split(",")
                for char_idx in range(len(line)):
                    line[char_idx] = int(line[char_idx])  # int cast

                matrix[matrix_index].append(line)

        arch.close()
        return matrix

    def __fileOutput(self, answer):
        """""
        Writes tt2 answers into the file input for the lines recognitions

        :returns: True if the answer is saved at the file
        :rtype: bool
        """
        pb_app_name = self.app_short_name
        bookId = pb_app_name[:-4]
        imgId = self.task.info["page"]

        try:
            print("File path:" + "%s/books/%s/metadados/entrada/image%s.txt" % (
                app.config["CV_MODULES"], bookId, imgId), "a")
            arch = open("%s/books/%s/metadados/entrada/image%s.txt" % (
                app.config["CV_MODULES"], bookId, imgId), "w")
            for table in answer:
                x0 = int(table["left"])
                x1 = int(table["width"] + x0)
                y0 = int(table["top"])
                y1 = int(table["height"] + y0)
                arch.write(
                    str(x0) + "," + str(y0) + "," + 
                    str(x1) + "," + str(y1) + "\n")
            arch.close()

            return True
        except IOError:
            print "Error: Couldn't open %s to write image%s.txt file" % (
                bookId, imgId)
            # TODO: see what to do with the flow in exceptions

        return False

# TODO ==> rodar OCR (TesseractExecutor)
     
# Se tiver zoom checar se as tasks do grupo terminaram
      
# 1. inserir carregar respostas de TesseractExecutor
# 2. verificar niveis de confianca para ocrzacoes de celulas
# 3. inserir respostas em T4

class TTTask3(pb_task):
    """
    Table Transcriber Task type 3
    """
    def __init__(self, task_id, app_short_name):
        super(TTTask3, self).__init__(task_id, app_short_name)

    def add_next_task(self):

        if (self.__checkIfNextTaskWasCreated()):
            return

        try:
            linesAndColumnsMap = self.__loadAnswers()
            
            cells = cellsUtil.create_cells(linesAndColumnsMap["linhas"], linesAndColumnsMap["colunas"], 
            linesAndColumnsMap["maxX"], linesAndColumnsMap["maxY"])
            
            #print "linesAndColumnsMap: " + str(linesAndColumnsMap)
            
            linkImg = self.task.info['img_url']
            book_id = self.app_short_name[:-4]
            page = self.task.info['page']
            table_id = self.task.info['table_id']
            maxX = linesAndColumnsMap["maxX"]
            maxY = linesAndColumnsMap["maxY"]
            
            self.__runOCR(cells, book_id, page, table_id, maxX, maxY)
            
            values = self.__loadValues(book_id, page, table_id)
            confidences = self.__loadConfidences(book_id, page, table_id)
            
            infoDict = {}
            infoDict['cells'] = cells
            infoDict['img_url'] = linkImg
            infoDict['page'] = page
            infoDict['table_id'] = table_id
            infoDict['maxX'] = maxX
            infoDict['maxY'] = maxY
            infoDict['values'] = values
            infoDict['confidences'] = confidences
            
            tt4_app_short_name = self.app_short_name[:-1] + "4"
            tt4_app = ttapps.Apptt_transcribe(short_name=tt4_app_short_name)
            tt4_app.add_task(infoDict)
        
        except Exception, e:
            print str(e)
    
    def __checkIfNextTaskWasCreated(self):
        img_url = self.task.info['img_url']
        tt4_app = self.get_next_app()
        tt4_tasks = tt4_app.get_tasks()

        for t in tt4_tasks:
            if (t.info['img_url'] == img_url):
                return True
        return False

    """
     Load values transcripted by tesseract ocr for this table
    """
    def __loadValues(self, book_id, page, table_id):
        
        f = open("%s/books/%s/transcricoes/texts/image%s_%s.txt" % (
                       app.config['CV_MODULES'], book_id, page, table_id), 'r')
        tmp = f.readlines()
        f.close()
        
        values = []
        for val in tmp[1:]:
            values.append(val[:-1]) # exclude \n
        
        return values #excluding header
    
    """
     Load confidences identified in transcriptions by tesseract ocr for
     this table.
    """
    def __loadConfidences(self, book_id, page, table_id):
        f = open("%s/books/%s/transcricoes/confidences/image%s_%s.txt" % (
                       app.config['CV_MODULES'], book_id, page, table_id), 'r')
        tmp = f.readlines()
        
        f.close()
        
        confidences = []
        for conf in tmp[1:]:
            confidences.append( int(conf[:-1])) # exclude \n
        
        return confidences # excluding header
    
    """
      Run tesseract executor
    """
    def __runOCR(self, cells, book_id, page, table_id, maxX, maxY):
        
        self.__saveCells(cells, book_id, page, table_id, maxX, maxY)
        
        command = 'cd %s/TesseractExecutorApp2/; ./tesseractexecutorapp2 ' \
        '"/books/%s/metadados/tabelasAlta/image%s_%d.png"' % (
        app.config['CV_MODULES'], book_id, page, table_id)
        
        call([command], shell=True)
        
    
    """
      Save cells in /books/<book_id>/metadados/respostaUsuarioTT/image<page>_<table_id>.png
      
      obs.: the algorithm used open the file two times to
       don't accept duplicated answers.
    """
    def __saveCells(self, cells, book_id, page, table_id, maxX, maxY):
        
        try:
            # file with the cells identified by users
            
            header = "#0,0" + "," + str(maxX) + "," + str(maxY) + "\n"
            arch = open("%s/books/%s/metadados/respostaUsuarioTT/image%s_%s.txt" % (
                       app.config['CV_MODULES'], book_id, page, table_id), 'w')
            arch.write(header)
            arch.close()
            
            arch = open("%s/books/%s/metadados/respostaUsuarioTT/image%s_%s.txt" % (
                       app.config['CV_MODULES'], book_id, page, table_id), 'a')
            for cell in cells:
                cStr = str(cell[0]) + "," + str(cell[1]) + "," + str(cell[2]) + "," + str(cell[3]) + "\n"
                arch.write(cStr)
            
            arch.close()
        
        except IOError:
            print "Error. File image%s_%s.txt couldn't be opened" % (
                    page, table_id)
        except Exception, e:
            print str(e)
    
    """
     Returns the info in json format to tasks, be them either zoom
     or not.
     
     obs.: the properties returned in json_answer are modified in this method: if
     the task has zoom, the answer equivalent to the group of tasks similar to this
     will be returned, in the same format of one simple task, without zoom.
     
     
    """
    def __loadAnswers(self):
        if(self.task.info['hasZoom']):
            
            similarTasks = self.__searchSimilarsTasks()
            groupedAnswers = None
                
            if(not self.__validateTaskGroup(similarTasks)):
                raise InvalidTaskGroupException()
            else:
                groupedAnswers = self.__joinTaskGroupAnswers(similarTasks)
            
            answer_json = {}
            answer_json['linhas'] = groupedAnswers['lines']
            answer_json['colunas'] = groupedAnswers['columns']
            answer_json['maxX'] = groupedAnswers['maxX']
            answer_json['maxY'] = groupedAnswers['maxY']
            
            return answer_json
        else:
            task_runs = json.loads(urllib2.urlopen(
                "%s/api/taskrun?task_id=%s&limit=%d" % (
                    app.config['PYBOSSA_URL'], self.task.id, sys.maxint)).read())
            
            task_run = task_runs[len(task_runs) - 1]  # Get the last answer
            answer = task_run["info"]
            answer_json = json.loads(answer)
            
            return answer_json
    
    """
      Search similar tasks to this task in pybossa task table
    """        
    def __searchSimilarsTasks(self):
        img_url = self.task.info['img_url']
        table_id = self.task.info['table_id']
        
        similarTasks = []
        tasks = self.__get_tasks()
        
        for t in tasks:
            if (t.info['img_url'] == img_url and t.info['table_id'] == table_id):
                similarTasks.append(t)
        
        return similarTasks
    
    """
     Get tasks with this.app_id
    """
    def __get_tasks(self):
        return pbclient.get_tasks(self.task.app_id, sys.maxint)
        
    """
      Verify if all tasks, that are similar to this task, and this task
      are completed.
    """
    def __validateTaskGroup(self, similarTasks):
        for t in similarTasks:
            if(not t.state == "completed"):
                return False
        return self.task.state == "completed"
    
    """
     Load last answer in json format of the last task_run of
     each task in similarTasks.
    """
    def __loadSimilarsTaskRunsAnswers(self, similarTasks):
        tasksRunsAnswers = []
        for t in similarTasks: 
            task_runs = json.loads(urllib2.urlopen(
                    "%s/api/taskrun?task_id=%s&limit=%d" % (
                        app.config['PYBOSSA_URL'], t.id, sys.maxint)).read())
                
            task_run = task_runs[len(task_runs) - 1]  # Get the last answer
            answer = task_run["info"]
            answer_json = json.loads(answer)
            tasksRunsAnswers.append(answer_json)
        
        return tasksRunsAnswers
    
    """
      Join all answers of task_runs to return a table grid.
    """
    def __joinTaskGroupAnswers(self, similarTasks):
        
        similarTaskRunsAnswers = self.__loadSimilarsTaskRunsAnswers(similarTasks)
        
        lines = []
        columns = []
        maxX = 0
        maxY = 0
              
        for info in similarTaskRunsAnswers:
            for c in info['colunas']:
                columns.append(c)

            for l in info['linhas']:
                overlapping_line = self.__getLineOverlapping(l, lines)

                if (overlapping_line == -1):
                    lines.append(l)
                else:
                    newY = overlapping_line[1]
                    columns = self.__updateColumnsYAxis(l, columns, newY)
            
            if maxX < info['maxX']:
                maxX = info['maxX']
            if maxY < info['maxY']:
                maxY = info['maxY']
        
        #print "lines"
        #print lines
        
        #print "columns"
        #print columns
        
        mapWithNewAnswer = self.__transformSegmentsInLines(lines, columns)
        mapWithNewAnswer['maxX'] = maxX
        mapWithNewAnswer['maxY'] = maxY
        
        return mapWithNewAnswer

    def __getLineOverlapping(self, line, lines):
        MIN_GAP_BETWEEN_LINES = 5
        for i in range(0, len(lines)):
            other_line =  lines[i]
            
            if ((line[0] == other_line[0] or self.__insideOpenInterval(line[0], line[2], other_line[0]) or self.__insideOpenInterval(line[0], line[2], other_line[2])) and math.fabs((line[1] - other_line[1])) <= MIN_GAP_BETWEEN_LINES):
                return other_line
  
        return -1

    def __insideOpenInterval(self, init, final, element):
        return element > init and element < final

    """
      Transform segments in horizontal or vertical orientations
      in complete lines.
      
      lines: set of lines of all tasks similars to this
      columns: set of columns of all tasks similars to this
    """
    def __transformSegmentsInLines(self, lines, columns):
        
        mapGroupsOfColumns = {}
        for c1 in columns:
            idGroup = self.__identifyGroupIdInX(mapGroupsOfColumns, c1)
            
            if not mapGroupsOfColumns.has_key(idGroup):
                mapGroupsOfColumns[idGroup] = [c1]
            else:
                mapGroupsOfColumns[idGroup].append(c1)
        
        mapWithLinesAndColumns = self.__joinColumnsInGroup(mapGroupsOfColumns, lines)
        
        #print "mapWithLinesAndColumns"
        #print mapWithLinesAndColumns
        
        return mapWithLinesAndColumns
    
    def __identifyGroupIdInX(self, mapGroupsOfColumns, column):
        MIN_GAP_BETWEEN_COLUMNS_IN_X_AXIS = 10
        
        sortListOfGroupIds = []
        for identifier in mapGroupsOfColumns.keys():
            sortListOfGroupIds.append(float(identifier)) 
        
        sortListOfGroupIds.sort()
        
        for group in sortListOfGroupIds:
            if (math.fabs(column[0] - group) <= MIN_GAP_BETWEEN_COLUMNS_IN_X_AXIS):
                return str(group)
        
        return str(float(column[0]))
        
    """
     Join the columns in the same group to make
     a one or more columns consistents.
    """
    def __joinColumnsInGroup(self, mapGroupsOfColumns, lines):
        finalListOfColumns = []
        
        #print "mapGroupsOfColumns"
        #print mapGroupsOfColumns
        
        for groupOfColumns in mapGroupsOfColumns.values():
            transformationResult = self.__transformGroupInList(groupOfColumns, lines)
            lines = transformationResult['lines']
            columns = transformationResult['columns']
            
            for c in columns:
                finalListOfColumns.append(c)
                       
        #print "finalListOfColumns"
        #print finalListOfColumns

        joinResult = {}
        joinResult['lines'] = lines
        joinResult['columns'] = finalListOfColumns
        
        return joinResult
    
    """
     Transform group of columns in one list of consistent
     columns.
    """
    def __transformGroupInList(self, groupOfColumns, lines):
        MIN_GAP_BETWEEN_COLUMNS_IN_Y_AXIS = 5
        sortedGroupOfColumns = sorted(groupOfColumns, key=itemgetter(1))
        #print "sortedGroupOfColumns"
        #print sortedGroupOfColumns
        
        listOfColumns = []
        
        ptr1 = None
        ptr2 = None
        tmpCols = []

        for i in range(0, len(sortedGroupOfColumns)-1):   # find other columns to join
            ptr1 = sortedGroupOfColumns[i]
            ptr2 = sortedGroupOfColumns[i+1]

            if (ptr2[1] - ptr1[3] <= MIN_GAP_BETWEEN_COLUMNS_IN_Y_AXIS): # is a continuous column
                tmpCols.append(ptr1)
                if(i+1 == len(sortedGroupOfColumns)-1):
                    tmpCols.append(ptr2)
            else:
                if (len(tmpCols) == 0):
                    tmpCols.append(ptr1)

                newX = tmpCols[0][0]
                listOfColumns.append([newX, tmpCols[0][1],
                                      newX, tmpCols[-1][3]])
                lines = self.__updateLinesXAxis(tmpCols, lines, newX)

                tmpCols = [ptr2]
                #print "listOfColumns"
                #print listOfColumns
       
        if (len(sortedGroupOfColumns) == 1):
            tmpCols.append(sortedGroupOfColumns[0])

        newX = tmpCols[0][0]
        listOfColumns.append([newX, tmpCols[0][1],
                              newX, tmpCols[-1][3]])
        lines = self.__updateLinesXAxis(tmpCols, lines, newX)
     
        #print "listOfColumns"
        #print listOfColumns

        transformationResult = {}
        transformationResult['lines'] = lines
        transformationResult['columns'] = listOfColumns
        
        return transformationResult
    
    def __updateLinesXAxis(self, columns, lines, newX):
        for column in columns:
            for i in range(0, len(lines)):
                line = lines[i]
                if line[0] == column[0]:
                    lines[i] = [newX, line[1], line[2], line[3]]
                elif line[2] == column[0]:
                    lines[i] = [line[0], line[1], newX, line[3]]
        return lines

    def __updateColumnsYAxis(self, line, columns, newY):
        for i in range(0, len(columns)):
            column = columns[i]
            if column[1] == line[1]:
                columns[i] = [column[0], newY, column[2], column[3]]
            elif column[3] == line[1]:
                columns[i] = [column[0], column[1], column[2], newY]
        return columns

    def close_task(self):
        pass

    def check_answer(self):
        task_runs = self.get_task_runs()
        n_taskruns = len(task_runs)  # task_runs goes from 0 to n-1
        
        if(n_taskruns > 1):
            answer1 = task_runs[n_taskruns - 1].info
            answer2 = task_runs[n_taskruns - 2].info
            
            answer1_json = json.loads(answer1)
            answer2_json = json.loads(answer2)
            if(self.__compare_answers(answer1_json, answer2_json)):
                return True
            else:
                return False
        else:
            return False
        
        return False

    def get_next_app(self):
        curr_app_name = self.app_short_name
        next_app_name = curr_app_name[:-1] + "4"
        return ttapps.Apptt_transcribe(short_name=next_app_name)

    def __compare_answers(self, answer1, answer2):
        if len(answer1) != len(answer2):
            return False
        
        col1 = answer1['colunas']
        lin1 = answer1['linhas']
        
        col2 = answer2['colunas']
        lin2 = answer2['linhas']
        
        if (len(col1) != len(col2) or len(lin1) != len(lin2)):
            return False
        else:
            r1 = self.__compareCols(col1, col2) 
            r2 = self.__compareLin(lin1, lin2)
            #print ("r1: " + str(r1))
            #print ("r2: " + str(r2))
            
            if (r1 and r2):
                return True
            else:
                return False
    
    """
     Compare columns of different answers. Return true if <column1> and
     <column2> are the same.
    """
    def __compareCols(self, column1, column2):
        threshold = 5
        
        for i in range(0,len(column1)):
            for j in range(0, 4):
                if (column1[i][j] > (column2[i][j] + threshold) or column1[i][j] < (column2[i][j] - threshold)):
                    return False
                    
        return True
    
    """
     Compare lines of different answers. Return true if <line1> and
     <line2> are the same.
    """
    def __compareLin(self, line1, line2):
        threshold = 5
        
        for i in range(0, len(line1)):
            for j in range(0, 4):
                if (line1[i][j] > (line2[i][j] + threshold) or line1[i][j] < (line2[i][j] - threshold)):
                    return False
        
        return True

class TTTask4(pb_task):
    """
    Table Transcriber Task type 4
    """
    def __init__(self, task_id, app_short_name):
        super(TTTask4, self).__init__(task_id, app_short_name)
        
    def add_next_task(self):
        #TODO
        return
    
    def close_task(self):
        pass
    
    def check_answer(self):
        task_runs = self.get_task_runs()
        n_taskruns = len(task_runs)  # task_runs goes from 0 to n-1
        
        if (n_taskruns > 0):
            last_answer = task_runs[n_taskruns - 1].info
            last_answer_json = json.loads(last_answer)
            confirmations = last_answer_json['num_of_confirmations']

            for confirmation in confirmations:
                if (int(confirmation) < 2):
                    return False
            return True
        else:
            return False

    def __compare_answers(self, answer1, answer2):
        val1 = answer1['human_values']
        val2 = answer2['human_values']

        if len(val1) != len(val2):
            return False
        
        for i in range(0, len(val1)):
            if val1[i] != val2[i]:
                return False
        return True
    
    def get_next_app(self):
        return
