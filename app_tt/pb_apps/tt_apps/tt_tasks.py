# -*- coding: utf-8 -*-

from app_tt.pb_apps.pb_task import pb_task
import ttapps
from app_tt.core import app
from subprocess import call
import requests
import urllib2
from requests import RequestException
import json
import sys
import os


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
        #Verify the answer of the question to create a new task
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
                #put the answer into task info
                requests.put("%s/api/task/%s?api_key=%s" % (
                    app.config['PYBOSSA_URL'], self.task.id,
                    app.config['API_KEY']),
                    data=json.dumps(dict(info=self.task.info)))
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
        #Get the list of task_runs
        task_runs = json.loads(urllib2.urlopen(
            "%s/api/taskrun?task_id=%s&limit=%d" % (
                app.config['PYBOSSA_URL'], self.task.id, sys.maxint)).read())

        task_run = task_runs[len(task_runs) - 1]  # Get the last answer
        answer = json.loads(task_run["info"])

        if(answer != 0):

            tt3_app_short_name = self.app_short_name[:-1] + "3"
            tt3_app = ttapps.Apptt_struct(short_name=tt3_app_short_name)

            bookId = self.app_short_name[:-4]
            imgId = self.task.info["page"]

            self.__downloadArchiveImages(bookId, imgId)
            self.__runLinesRecognition(bookId, imgId,
                                       answer[0]["text"]["girar"])

            try:
                # file with the lines recognized
                arch = open(
                    "%s/books/%s/metadados/saida/image%s_model%s.txt" % (
                    app.config['TT3_BACKEND'], bookId, imgId, "1"))
                #get the lines recognitions
                tables_coords = self.__splitFile(arch)
                for tableId in range(len(tables_coords)):
                    self.__runAreaSelection(
                        bookId, imgId, tableId)

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
            #TODO: the task will not be created,
            # routine to solve this must be implemented
            except Exception, e:
                print str(e)

    def close_task(self):
        pass

    def check_answer(self):
        task_runs = self.get_task_runs()
        n_taskruns = len(task_runs)  # task_runs goes from 0 to n-1
        if(n_taskruns > 1):
            answer1 = json.loads(task_runs[n_taskruns - 1].info)
            answer2 = json.loads(task_runs[n_taskruns - 2].info)

	    print(answer1)
	    print(answer2)

            if self.__compare_answers(answer1, answer2):
                if answer2 != "0":
                    return self.__fileOutput(answer2)
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

    def __downloadArchiveImages(self, bookId, imgId, width=550, height=700):
        """
        Download internet archive images to tt3_backend project
        :returns: True if the download was successful
        :rtype: bool
        """

        try:
            url_request = requests.get(
                "http://archive.org/download/%s/page/n%s" % (
                bookId, imgId))
            fullImgPathInit = "%s/books/%s/alta_resolucao/image%s.jpg" % (
                app.config['TT3_BACKEND'], bookId, imgId)
            fullImgPathFinal = "%s/books/%s/alta_resolucao/image%s.png" % (
                app.config['TT3_BACKEND'], bookId, imgId)

            fullImgFile = open(fullImgPathInit, "w")
            fullImgFile.write(url_request.content)
            fullImgFile.close()
	    
	    # shell command to convert jpg to png
            command = 'convert %s %s; rm %s' % (
                fullImgPathInit, fullImgPathFinal, fullImgPathInit)

	    print("Command: " + command)
            call([command], shell=True)  # calls the shell command

            lowImgPath = "%s/books/%s/baixa_resolucao/image%s.png" % (
                app.config['TT3_BACKEND'], bookId, imgId)
            
            command = 'convert %s -resize %dx%d %s' % (
                fullImgPathFinal, width, height, lowImgPath)

            call([command], shell=True)  # calls the shell command

            return True
        except IOError, e:
            print str(e)
        #TODO: Implement strategies for exceptions cases
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
        #command shell to enter into the tt3 backend project and
        #calls the lines recognizer software

        if rotate:
            rotate = "-r"
        else:
            rotate = "-nr"
            
        command = 'cd %s/TableTranscriber2/; ./tabletranscriber2 ' \
            '"/books/%s/baixa_resolucao/image%s.png" "model%s" "%s"' % (
            app.config['TT3_BACKEND'], bookId, imgId, model, rotate)
            
        print("command: " + command)
            
        call([command], shell=True)  # calls the shell command
        #TODO: implements exception strategy

        return self.__checkFile(bookId, imgId)

    def __checkFile(self, bookId, imgId):
        directory = "%s/books/%s/metadados/saida/" % (
            app.config['TT3_BACKEND'], bookId)
        output_files = os.listdir(directory)
        images = [file.split('_')[0] for file in output_files]

        return ("image%s" % imgId) in images

    def __runAreaSelection(self, bookId, imgId, tableId):
        """
        Call cpp ZoomingSelection software that splits the
        tables and write the pieces at
        <tt3_backend_id>/books/bookId/selections/image<imgId>_tableId.txt

        :returns: True if the execution was ok
        :rtype: bool
        """

        command = 'cd %s/ZoomingSelector/; ./zoomingselector ' \
            '"/books/%s/metadados/tabelasAlta/image%s_%d.png"' % (
                app.config['TT3_BACKEND'], bookId, imgId, tableId)

        call([command], shell=True)

    def __getAreaSelection(self, bookId, imgId, tableId):

        selections = []

        try:
            filepath = "%s/books/%s/selections/image%s_%d.txt" % (
                app.config['TT3_BACKEND'], bookId, imgId, tableId)
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

    def __scale(point, src, dest):
        scaleX = lambda x, src_w, dest_w: round((dest_w * x)/float(src_w))
        scaleY = lambda y, src_h, dest_h: round((dest_h * y)/float(src_h))

        return [scaleX(point[0], src[0], dest[0]),
                scaleY(point[1], src[1], dest[1])]

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
                app.config["TT3_BACKEND"], bookId, imgId), "a")
            arch = open("%s/books/%s/metadados/entrada/image%s.txt" % (
                app.config["TT3_BACKEND"], bookId, imgId), "w")
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

class TTTask3(pb_task):
    """
    Table Transcriber Task type 3
    """
    def __init__(self, task_id, app_short_name):
        super(TTTask3, self).__init__(task_id, app_short_name)

    def add_next_task(self):
        #Verify the answer of the question to create a new task
	#TODO create TT4 tasks
	pass
 

    def close_task(self):
        pass

    def check_answer(self):
	#TODO check if all zoom areas were completed
        return False

    def get_next_app(self):
        curr_app_name = self.app_short_name
        next_app_name = curr_app_name[:-1] + "4"
        return ttapps.Apptt_meta(short_name=next_app_name)


