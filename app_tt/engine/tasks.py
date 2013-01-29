# -*- coding: utf-8 -*-
from celery import Celery
import urllib2
import requests
import json
import sys
from celery import task
from app_tt.core import pbclient
from app_tt.core import app
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct

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
    imgs = __get_tt_images(book_id)
    

    if(imgs):
        tt_select = Apptt_select(book_id + "_tt1")
        tt_meta = Apptt_meta(book_id + "_tt2")
        tt_struct = Apptt_struct(book_id + "_tt3")

        bookInfo = _archiveBookData(book_id)

        tt_meta.add_app_infos(dict(sched="incremental"))
        tt_meta.add_app_infos(bookInfo)
        tt_select.add_app_infos(bookInfo)

        if len(tt_select.get_tasks()) == 0:
            for img in imgs:
                tt_select.add_task(img)
        
        return True
    
    else:
        raise ValueError("Error didn't find book id")
    
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
                pb_app=  __find_app(short_name=(pb_app["short_name"][:-3] + "tt2"))  #  app where will be added the task
                task = dict(app_id=pb_app["id"], state=0, calibration=0, priority_0=0, info=info)  #  dict with task data to be added
                
                add_task = requests.post("%s/api/task" % (app.config['PYBOSSA_URL']),
                        params=dict(api_key=app.config['API_KEY']), data=json.dumps(task))  # add the task to tt2

        else if(strategy == "tt2"):
            #Get the list of task_runs
            task_runs = json.loads(urllib2.urlopen("%s/api/taskrun?task_id=%s&limit=%d" % (app.config['PYBOSSA_URL'],
                                                    task_id, sys.maxint)).read())
            task_run = task_runs[len(task_runs) - 1] # Get the last answer
            answer = task_run["info"]
            print type(answer)
            print answer
            if(answer != 0):
                bookId = pb_app[:-4]
                imgId = task["info"]["page"]
                arch = open("%s/%s/metadados/baixa_resolucao/image%s" % (app.config['BOOKS_DIR'], bookId, imgId))
                dic_tables = __splitFile(arch)


def __splitFile(arch):
    """""
    Splits a given file and return a dic where the lines with '#' are the keys
    and the other lines with values separated with ',' are lists
    :returns: a dict with keys:str and values:lists
    :rtype: dict
    """

    strLines = arch.read().strip().split("\n")
    dic_keys = {}
    current_key = None

    for line in strLines:
        if line.find("#") != -1:
            current_key = line
            dic_keys[current_key] = []
        else:
            dic_keys[current_key].append(line.split(","))

    return dic_keys


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

            return answer1 == answer2
        else:
            return False


def __get_tt_images(bookId):
    """
    Get public book images from internet archive server
    :returns: A list with dicts with images urls and index.
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

    try:
        imagecount = output['metadata']['imagecount']
    except KeyError:
        imagecount = output['metadata']['numero_de_paginas_do_item']
    imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"

    imgList = []
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
    return dict(title=data["metadata"]["title"],
        publisher=data["metadata"]["publisher"],
        volume=data["metadata"]["volume"],
        contributor=data["metadata"]["contributor"],
        img=img,
        bookid=bookid)
