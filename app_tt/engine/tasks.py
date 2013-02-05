# -*- coding: utf-8 -*-
from celery import Celery
import urllib2
import requests
import json
import sys
from celery import task
from app_tt.core import pbclient
from app_tt.core import app
from requests import RequestException
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct
from subprocess import call

BROKER_URL = "amqp://celery:celery@localhost:5672/celery"
celery = Celery('tasks', backend='amqp', broker=BROKER_URL)
#celery.config_from_object('app_tt.engine.celeryconfig')


@task(name="app_tt.engine.tasks.check_task")
def check_task(task_id):
    pb_app= __find_app_by_taskid(task_id)

    if(pb_app):
        return __answer_ok(task_id, pb_app["short_name"][-3:])  # Verify if the answer completed the task
    else:
        raise ValueError("Task not found")


@task(name="app_tt.engine.tasks.create_apps")
def create_apps(book_id):
    """"
    Creates tt_apps and tt1 tasks
    :params book_id: Internet archive book id
    :returns: book indicating if the applications were created
    :rtype: bool
    """
    imgs = __get_tt_images(book_id)
    

    if(imgs):
        tt_select = Apptt_select(short_name=book_id + "_tt1")
        tt_meta = Apptt_meta(short_name=book_id + "_tt2")
        tt_struct = Apptt_struct(short_name=book_id + "_tt3")

        bookInfo = _archiveBookData(book_id)

        tt_meta.add_app_infos(dict(sched="incremental"))
        tt_meta.add_app_infos(bookInfo)
        tt_select.add_app_infos(bookInfo)

        if len(tt_select.get_tasks()) == 0:
            for img in imgs:
                tt_select.add_task(img)
        
        return True
    
    else:
        print "Error didn't find book id"
        return False
    
    return False


@task(name="app_tt.engine.tasks.close_task")
def close_task(task_id):
    r = requests.put("%s/api/task/%s?api_key=%s" % (app.config['PYBOSSA_URL'], task_id, app.config['API_KEY']),
            data=json.dumps(dict(state="completed")))  #  set task state to completed


@task(name="app_tt.engine.tasks.create_task")
def create_task(task_id, strategy=None):
        task = json.loads(requests.get("%s/api/task/%s?api_key=%s" % (app.config['PYBOSSA_URL'],
            task_id, app.config['API_KEY'])).content)
        pb_app= __find_app_by_taskid(task_id)  # get entrypoint app
        strategy = pb_app["short_name"][-3:]
        
        if(strategy == "tt1"):  # task from tt1 to tt2
            if(task["info"]["answer"] == "Yes"):  # Verify the answer of the questio to create a new task
                #TODO: apply strategy pattern
                info = dict(link=task["info"]["url_m"], page=task["info"]["page"])
                add_task = __add_task(pb_app, "tt2", info)# add the task to tt2

        elif(strategy == "tt2"):
            #Get the list of task_runs
            task_runs = json.loads(urllib2.urlopen("%s/api/taskrun?task_id=%s&limit=%d" % (app.config['PYBOSSA_URL'],
                                                    task_id, sys.maxint)).read())
            task_run = task_runs[len(task_runs) - 1] # Get the last answer
            answer = json.loads(task_run["info"])
            
            if(answer != 0):
                bookId = pb_app["short_name"][:-4]
                imgId = task["info"]["page"]
                
                __downloadArchiveImages(bookId, imgId)
                __runLinesRecognition(bookId, imgId, answer[0]["text"]["girar"] )

                try:
                    arch = open("%s/books/%s/metadados/saida/image%s.txt" % (app.config['TT3_BACKEND'], bookId, imgId)) # file with the lines recognitio
                    coord_matrices = __splitFile(arch) # get the lines recognitions
                    for matrix_index in range(len(coord_matrices)):
                        info = dict(coords=coord_matrices[matrix_index], page=imgId, img_url=__url_table(bookId, imgId, matrix_index))
                        add_task = __add_task(pb_app, "tt3", info) #add task to tt3
                except IOError,e: print str(e) #TODO: the task will not be created, a routine to solve this must be implemented
                except Exception,e: print str(e)


def __downloadArchiveImages(bookId, imgId, width=550, height=700):
    """
    Downloads internet archive images to tt3_backend project
    :returns: True if the download was successful
    :rtype: bool
    """
    
    try:
        url_request = requests.get("http://archive.org/download/%s/page/n%s" % (bookId, imgId))
        fullImgPath = "%s/books/%s/alta_resolucao/image%s.png" % (app.config['TT3_BACKEND'], bookId, imgId)
        fullImgFile = open(fullImgPath, "w")
        fullImgFile.write(url_request.content)
        fullImgFile.close()
    
        url_request = requests.get("http://archive.org/download/%s/page/n%s_w%d_h%d" % (bookId, imgId, width, height))
        lowImgPath = "%s/books/%s/baixa_resolucao/image%s.png" % (app.config['TT3_BACKEND'], bookId, imgId)
        lowImgFile = open(lowImgPath, "w")
        lowImgFile.write(url_request.content)
        lowImgFile.close()
        
        return True
    except IOError,e: print str(e)          #TODO: Implement strategies for exceptions cases
    except RequestException,e: print str(e)
    except Exception,e: print str(e)

    return False

def __runLinesRecognition(bookId, imgId, rotate="", model="1"):
    """
    Call cpp software that recognizes lines into the table and
    writes lines coords into <tt3_backend_dir>/books/bookId/metadata/saida/image<imgId>.txt
    :returns: True if the write was successful 
    :rtype: bool
    """
    if(rotate):
        rotate = "-r"
    
    #command shell to enter into the tt3 backend project and 
    #calls the lines recognizer software
    command = 'cd %s/TableTranscriber/; ./tabletranscriber "/books/%s/baixa_resolucao/image%s.png" "model%s" "%s"' % (app.config['TT3_BACKEND'],
            bookId, imgId, model, rotate)
    
    call([command], shell=True) #calls the shell command    
    #TODO: implements exception strategy


def __url_table(bookId, imgId, idx):
    """""
    Build a url of a splited image for the lines recognizer
    :returns: a indexed book table image
    :rtype: str
    """
    return "%s/books/%s/metadados/tabelasBaixa/image%s_%d.png" % (app.config['URL_TEMPLATES'], bookId, imgId, idx)


def __add_task(pb_app, strategy, info):
    pb_app =  __find_app(short_name=(pb_app["short_name"][:-3] + strategy))  #  app where will be added the task
    task = dict(app_id=pb_app["id"], state=0, calibration=0, priority_0=0, info=info)  #  dict with task data to be added
    add_task = requests.post("%s/api/task" % (app.config['PYBOSSA_URL']),
                        params=dict(api_key=app.config['API_KEY']), data=json.dumps(task)) # add the task


def __splitFile(arch):
    """""
    Splits a given file and return a matrices list where the lines with '#' are the index
    and the other lines with values separated with ',' are the vectors of the inner matrices
    :returns: a list of matrix
    :rtype: list
    """

    strLines = arch.read().strip().split("\n")
    matrix = []
    matrix_index = -1

    for line in strLines:
        if line.find("#") != -1:
            matrix_index +=1
            matrix.append([])
        else:
            line = line.split(",")
            for char_idx in range(len(line)):
                line[char_idx] = int(line[char_idx])

            matrix[matrix_index].append(line)
    arch.close()
    return matrix

def __find_app(**keyargs):
    """""
    Find one pybossa app by a given params
    :returns: One pybossa's app data
    :rtype: dict
    """
    return json.loads(requests.get("%s/api/app" % (app.config['PYBOSSA_URL']), params=keyargs).content)[0]  # get the pb_appdata dict

def __find_app_by_taskid(task_id):
    """""
    Find a pybossa app by a pybossa task id
    :returns: The pybossa's app data
    :rtype: dict
    """
    task = json.loads(urllib2.urlopen("%s/api/task/%s?api_key=%s" % (app.config['PYBOSSA_URL'], task_id, app.config['API_KEY'])).read())  # get task data
    return __find_app(id=task["app_id"])


def __answer_ok(task_id, strategy):
    """""
    Verify if the answers of a given task are ok to finish the task_runs
    :returns: A confirmation that the task is ready to be finished
    :rtype: boolean
    """
    task_runs = json.loads(urllib2.urlopen("%s/api/taskrun?task_id=%s" % (app.config['PYBOSSA_URL'], task_id)).read())  # get a list of taskruns
    task = json.loads(requests.get("%s/api/task/%s" % (app.config['PYBOSSA_URL'], task_id)).content)  # get task data
    task_info = task["info"]
    
    if(strategy == "tt1"):
        N_ANSWER = 2
        answers = {}
        for taskrun in task_runs:
            answer = taskrun["info"]
            if(answer not in answers.keys()):
                answers[answer] = 1
            else:
                answers[answer] += 1

            if(answers[answer] == N_ANSWER and answer != "NotKnown"):
                task_info["answer"] = answer
                r = requests.put("%s/api/task/%s?api_key=%s" % (app.config['PYBOSSA_URL'], task_id, app.config['API_KEY']),
            data=json.dumps(dict(info=task_info)))  # put the answer into task info

                return True
        return False
    
    elif(strategy == "tt2"):
        n_taskruns = len(task_runs)  # task_runs goes from 0 to n-1
        if(n_taskruns > 1):
            answer1 = json.loads(task_runs[n_taskruns - 1]["info"])
            answer2 = json.loads(task_runs[n_taskruns - 2]["info"])

            if answer1 == answer2:
                if answer2 != "0":
                    return __tt2FileOutput(task, answer2)
        else:
            return False


def __tt2FileOutput(task, answer):
    """""
    Writes tt2 answers into the file input for the lines recognitions
    :returns: True if the answer is saved at the file
    :rtype: bool
    """
    pb_app = __find_app_by_taskid(task["id"])
    bookId = pb_app["short_name"][:-4]
    imgId = task["info"]["page"]
    
    try:
        arch = open("%s/books/%s/metadados/entrada/image%s.txt" % (app.config["TT3_BACKEND"], bookId , imgId), "a")
        for table in answer:
            x0 = table["left"]
            x1 = table["width"] + x0
            y0 = table["top"]
            y1 = table["height"] + y0
            arch.write(str(x0) + "," + str(y0) + "," + str(x1) + "," + str(y1))
        arch.close()
        
        return True
    except IOError,e: print str(e) #TODO: see what to do with the flow in exceptions

    return False



def __get_tt_images(bookId):
    """
    Get public book images from internet archive server
    :returns: A list with dicts containing images urls and index.
    :rtype: list
    """
    WIDTH = 550
    HEIGHT = 700

    print('Contacting archive.org')

    url = "http://archive.org/metadata/"
    query = url + bookId
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    output = json.loads(data)
    imgList = []

    if output:
        try:
            imagecount = output['metadata']['imagecount']
        except KeyError:
            imagecount = output['metadata']['numero_de_paginas_do_item']

        imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"
        for idx in range(int(imagecount)):
            print 'Retrieved img: %s' % idx
            page = idx
            imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx, WIDTH, HEIGHT)
            imgUrl_b = imgUrls + str(idx)
            imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b, 'page': page})

    return imgList


def _archiveBookData(bookid):
    """"
        Get internet archive book infos
        :returns: A dict with metadata from internet archive
        :rtype: dict

    """
    query = "http://archive.org/metadata/" + bookid
    data = json.loads(requests.get(query).content)
    img = "http://www.archive.org/download/" + bookid + "/page/n7_w100_h100"
    default_dict = {"title" : None, "publisher" : None, "volume" : None, "contributor" : None}
    known_dict = dict(img=img, bookid=bookid)

    for key in default_dict:
        try:
            default_dict[key] = data["metadata"][key]
        except:
            print "This book does not have %s key" % key

    return dict(known_dict.items() + default_dict.items())
