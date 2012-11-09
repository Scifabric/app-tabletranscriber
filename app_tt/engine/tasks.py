# -*- coding: utf-8 -*-
from celery import Celery
import urllib2
import requests
import json
from celery import task
import app_tt.default_settings as settings
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta

BROKER_URL = "amqp://celery:celery@localhost:5672/celery"

celery = Celery('tasks', backend='amqp', broker=BROKER_URL)
#celery.config_from_object('app_tt.engine.celeryconfig')

@task(name="app_tt.engine.tasks.check_task")
def check_task(task_id, strategy):
    task = json.loads(urllib2.urlopen("%s/api/task/%s?api_key=%s" % (settings.PYBOSSA_URL, task_id, settings.API_KEY)).read())

    if(task):
        return __answer_ok(task_id, strategy)  # Verify if the answer completed the task
    else:
        raise ValueError("Task not found")


@task(name="app_tt.engine.tasks.create_apps")
def create_apps(book_id):
    imgs = __get_tt_images(book_id)
    
    if(imgs):
        tt_select = Apptt_select(book_id + "_tt1")
        tt_meta = Apptt_meta(book_id + "_tt2")
        tt_meta.add_app_infos(dict(sched="incremental"))
        
        for img in imgs:
            tt_select.add_task(img)
        
        return True
    
    else:
        raise ValueError("Error didn't find book id")
    
    return False


@task(name="app_tt.engine.tasks.close_task")
def close_task(task_id):
    r = requests.put("%s/api/task/%s?api_key=%s" % (settings.PYBOSSA_URL, task_id, settings.API_KEY),
            data=json.dumps(dict(state="completed")))  #  set task state to completed


@task(name="app_tt.engine.tasks.create_task")
def create_task(task_id, strategy):
        task = json.loads(requests.get("%s/api/task/%s?api_key=%s" % (settings.PYBOSSA_URL,
            task_id, settings.API_KEY)).content)
        app = __find_app(id=str(task["app_id"]))  # get entrypoint app
        
        if(app["short_name"][-3:] == "tt1"):  # task from tt1 to tt2
            if(task["info"]["answer"] == "Yes"):  # Verify the answer of the questio to create a new task
                #TODO: apply strategy pattern
                info = dict(link=task["info"]["url_m"])
                app =  __find_app(short_name=(app["short_name"][:-3] + "tt2"))  #  app where will be added the task
                task = dict(app_id=app["id"], state=0, calibration=0, priority_0=0, info=info)  #  dict with task data to be added
                
                add_task = requests.post("%s/api/task" % (settings.PYBOSSA_URL),
                        params=dict(api_key=settings.API_KEY), data=json.dumps(task))  # add the task to tt2


def __find_app(**keyargs):
    return json.loads(requests.get("%s/api/app" % (settings.PYBOSSA_URL), params=keyargs).content)[0]  # get the app data dict



def __answer_ok(task_id, strategy):
    task_runs = json.loads(urllib2.urlopen("%s/api/taskrun?task_id=%s" % (settings.PYBOSSA_URL, task_id)).read())  # get a list of taskruns
    task = json.loads(requests.get("%s/api/task/%s" % (settings.PYBOSSA_URL, task_id)).content)  # get task data
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
                r = requests.put("%s/api/task/%s?api_key=%s" % (settings.PYBOSSA_URL, task_id, settings.API_KEY),
            data=json.dumps(dict(info=task_info)))  # put the answer into task info

                return True

        return False


def __get_tt_images(bookId):
    """
    Gets public book images from internet archive server
    :returns: A list of book images.
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
        imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx, WIDTH, HEIGHT)
        imgUrl_b = imgUrls + str(idx)
        imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b})

    return imgList
