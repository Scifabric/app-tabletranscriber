# -*- coding: utf-8 -*-
from celery import Celery
import urllib2
import requests
import json
from celery import task
from app_tt.core import app
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct
from app_tt.pb_apps.tt_apps import task_factory

BROKER_URL = "amqp://celery:celery@localhost:5672/celery"
celery = Celery('tasks', backend='amqp', broker=app.config['BROKER_URL'])
#celery.config_from_object('app_tt.engine.celeryconfig')


@task(name="app_tt.engine.tasks.check_task")
def check_task(task_id):
    """
    Celery queued task that check pybossa's tasks status

    :arg task_id: Integer pybossa task id
    :returns: If the given pybossa task is finished
    :rtype: bool

    """
    task = task_factory.get_task(task_id)
    return task.check_answer()


@task(name="app_tt.engine.tasks.available_tasks")
def available_tasks(task_id):
    """
    Celery queued task that verify if there next available
    tasks at the workflow for a given pybossa task

    :arg task_id: Integer pybossa task id
    :returns: If there are available tasks
    :rtype: bool

    """
    current_task = task_factory.get_task(task_id)

    if(current_task):
        next_app = current_task.get_next_app()
        available_tasks = next_app.get_tasks()

        for task in available_tasks:
            if task.state != "completed":
                return True

    return False


@task(name="app_tt.engine.tasks.create_apps")
def create_apps(book_id):
    """
    Celery queued task that creates tt_apps and tt1 tasks

    :arg book_id: Internet archive book id
    :returns: book indicating if the applications were created
    :rtype: bool

    """
    imgs = __get_tt_images(book_id)

    if(imgs):
	book_title = __get_book_title(book_id);

        tt_select = Apptt_select(short_name=book_id + "_tt1", title=book_title)
        tt_meta = Apptt_meta(short_name=book_id + "_tt2", title=book_title)
        tt_struct = Apptt_struct(short_name=book_id + "_tt3", title=book_title)
        tt_transcribe = Apptt_transcribe(short_name=book_id + "_tt4", title=book_title)
        
        bookInfo = _archiveBookData(book_id)

        tt_select.add_app_infos(dict(thumbnail=bookInfo["img"]))

        tt_meta.add_app_infos(
            dict(
                sched="incremental",
                thumbnail=app.config['URL_TEMPLATES']
                + "/images"
                + "/long_description.png"))

        tt_struct.add_app_infos(
            dict(
                sched="incremental",
                thumbnail=app.config['URL_TEMPLATES']
                + "/images/tutorial-meta-struct"
                + "/model0_1.png"))

        tt_meta.add_app_infos(bookInfo)
        tt_select.add_app_infos(bookInfo)
        tt_struct.add_app_infos(bookInfo)
        tt_transcribe.add_app_infos(bookInfo)
        
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
    """
    Celery queued task that set's pybossa task state to completed

    :arg task_id: Integer pybossa task id

    """
    requests.put("%s/api/task/%s?api_key=%s" % (
        app.config['PYBOSSA_URL'], task_id, app.config['API_KEY']),
        data=json.dumps(dict(state="completed")))


@task(name="app_tt.engine.tasks.create_task")
def create_task(task_id):
    """
    Celery queued task that creates a next task following the workflow.
    For example, if the input is a task_id from a tt1 task,
    this method will create one tt2 task

    :arg task_id: Integer pybossa task id
    """
    task = task_factory.get_task(task_id)
    task.add_next_task()



def __get_book_title(bookId):

    print('Contacting archive.org')

    url = "http://archive.org/metadata/"
    query = url + bookId
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    output = json.loads(data)
    title = ""

    if output:
        title = output['metadata']['title']

    return title

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
            imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b,
                            'page': page})

    return imgList


def _archiveBookData(bookid):
    """
    Get internet archive book infos

    :arg book_id: Internet archive book id
    :returns: A dict with metadata from internet archive
    :rtype: dict

    """
    query = "http://archive.org/metadata/" + bookid
    data = json.loads(requests.get(query).content)
    img = "http://www.archive.org/download/" + bookid + "/page/n7_w100_h100"
    default_dict = {"title": None, "publisher": None,
                    "volume": None, "contributor": None}
    known_dict = dict(img=img, bookid=bookid)

    for key in default_dict:
        try:
            default_dict[key] = data["metadata"][key]
        except:
            print "This book does not have %s key" % key

    return dict(known_dict.items() + default_dict.items())
