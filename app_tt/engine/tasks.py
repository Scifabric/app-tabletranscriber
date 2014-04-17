# -*- coding: utf-8 -*-
from celery import Celery
import urllib2
import requests
import json
import psycopg2
import datetime
from celery import task
from app_tt.core import app, pbclient
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct
from app_tt.pb_apps.tt_apps.ttapps import Apptt_transcribe
from app_tt.meb_util import archiveBookData
from app_tt.pb_apps.tt_apps import task_factory
from app_tt.data_mngr import data_manager as data_mngr

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
        bookInfo = archiveBookData(book_id)
        
        app_tt_select = Apptt_select(short_name=book_id + "_tt1", title=bookInfo['title'])
        app_tt_meta = Apptt_meta(short_name=book_id + "_tt2", title=bookInfo['title'])
        app_tt_struct = Apptt_struct(short_name=book_id + "_tt3", title=bookInfo['title'])
        app_tt_transcribe = Apptt_transcribe(short_name=book_id + "_tt4", title=bookInfo['title'])
        
        app_tt_select.add_app_infos(
            dict(
                 thumbnail=app.config['URL_TEMPLATES']
                 + "/images" 
                 + "/long_description_selection.png"))

        app_tt_meta.add_app_infos(
            dict(
                sched="incremental",
                thumbnail=app.config['URL_TEMPLATES']
                + "/images"
                + "/long_description_meta.png"))

        app_tt_struct.add_app_infos(
            dict(
                sched="incremental",
                thumbnail=app.config['URL_TEMPLATES']
                + "/images"
                + "/long_description_struct.png"))
        
        app_tt_transcribe.add_app_infos(
            dict(
                 sched="incremental",
                 thumbnail=app.config['URL_TEMPLATES']
                 + "/images"
                 + "/long_description_transcribe.png"))

                
        app_tt_select.add_app_infos(bookInfo)
        app_tt_meta.add_app_infos(bookInfo)
        app_tt_struct.add_app_infos(bookInfo)
        app_tt_transcribe.add_app_infos(bookInfo)
        
        data_mngr.record_book_info_mbdb(bookInfo)
        
        if len(app_tt_select.get_tasks()) == 0:
            for img in imgs:
                app_tt_select.add_task(img)

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


@task(name="app_tt.engine.tasks.close_t1")
def close_t1(book_id):
    tt_select = Apptt_select(short_name=book_id + "_tt1")
    tasks = tt_select.get_tasks()
    
    for task in tasks:
        
        if ('answer' in task.info.keys()):
            continue
        
        task.info["answer"] = 'Yes'
        # put the answer into task info
        requests.put("%s/api/task/%s?api_key=%s" % (
            app.config['PYBOSSA_URL'], task.id,
            app.config['API_KEY']),
            data=json.dumps(dict(info=task.info, state="completed")))
        
        tt_task = task_factory.get_task(task.id)
        tt_task.add_next_task()
    


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
            raise
            
        imgUrls = "http://www.archive.org/download/" + bookId + "/page/n"
        for idx in range(int(imagecount)):
            print 'Retrieved img: %s' % idx
            page = idx
            imgUrl_m = imgUrls + "%d_w%d_h%d" % (idx, WIDTH, HEIGHT)
            imgUrl_b = imgUrls + str(idx)
            imgList.append({'url_m':  imgUrl_m, 'url_b': imgUrl_b,
                            'page': page})

    return imgList

@task(name="app_tt.engine.tasks.save_fact")
def save_fact(factInfo):
    taskFacade = task_factory.get_task(factInfo['task_id'])

    user_id = factInfo['user_id']
    book_id = taskFacade.get_book_id()
    page_id = taskFacade.task.info['page']
    top_pos = factInfo['top_pos']
    left_pos = factInfo['left_pos']
    bottom_pos = factInfo['bottom_pos']
    right_pos = factInfo['right_pos']

    isUpdate = 'id' in factInfo
    post_id = factInfo['post_id'] if 'post_id' in factInfo else ''
    fact_text = factInfo['fact_text'] if 'fact_text' in factInfo else ''
    fact_id = factInfo['id'] if isUpdate else -1

    con = None

    try:
        con = __create_db_connection(app.config['DB_NAME'])
        cursor = con.cursor()
        query = ""

        if (isUpdate):
            query = "UPDATE facts SET (user_id, book_id, page_id, top_pos, left_pos, bottom_pos, right_pos, post_id, fact_text) = ('" + user_id + "', '" + book_id + "', " + str(page_id) + ", " + str(top_pos) + ", "+ str(left_pos) + ", " + str(bottom_pos) + ", " + str(right_pos) + ", '" + post_id + "', '" + fact_text + "') WHERE id = " + str(fact_id)
        else:
            query = "BEGIN; INSERT INTO facts(user_id, book_id, page_id, top_pos, left_pos, bottom_pos, right_pos, post_id, fact_text) values ('" + user_id + "', '" + book_id + "', " + str(page_id) + ", " + str(top_pos) + ", "+ str(left_pos) + ", " + str(bottom_pos) + ", " + str(right_pos) + ", '" + post_id + "', '" + fact_text + "') RETURNING id;"

        print(query)
        cursor.execute(query)

        if not isUpdate:
            rows = cursor.fetchone()
            fact_id = rows[0]

        con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if con:
            con.close()
        return fact_id

@task(name="app_tt.engine.tasks.submit_report")
def submit_report(a_shortname, t_id, msg, u_ident):
    print "a_shortname: " + a_shortname
    print "t_id: " + str(t_id)
    print "msg: " + str(msg)
    print "u_ident: " + str(u_ident)
    
    a_id = pbclient.find_app(short_name=a_shortname)[0].id
    
    infos = {}
    infos['msg'] = json.dumps(msg, ensure_ascii=False)
    infos['app_id'] = a_id
    infos['task_id'] = t_id
    infos['user_id'] = str(u_ident)
    infos['created'] = datetime.datetime.now()
    
    try:
        data_mngr.record_report(infos)
        return True
    except Exception as e:
        print e
        return False  # TODO: send exception to log


def __create_db_connection(db_name):
    conn_string = "host='"+ app.config['DB_HOST'] + "' dbname='" + db_name + "' user='" + app.config['DB_USER'] + "' password='" + app.config['DB_USER_PASSWD'] + "'"
    return psycopg2.connect(conn_string)

@task(name="app_tt.engine.tasks.get_fact_page")
def get_fact_page(fact_id):
    con = None
    result = ""
    try:
        con = __create_db_connection(app.config['DB_NAME'])
        cursor = con.cursor()
        query = "SELECT id, user_id, book_id, page_id, top_pos, left_pos, bottom_pos, right_pos FROM facts WHERE id = " + str(fact_id)
        print(query)

        cursor.execute(query)

        rows = cursor.fetchone()
        result = __createFactPage(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7])

        con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if con:
            con.close()
        return result

def __createFactPage(fact_id, user_id, book_id, page_id, top_pos, left_pos, bottom_pos, right_pos):
    user_name = __get_user_name(user_id)
    server_url = app.config['URL_TEMPLATES']
    fact_url = "http://" + app.config['PYBOSSA_HOST'] + "/mb/api/fact/" + str(fact_id)
    book_list_url = "http://" + app.config['PYBOSSA_HOST'] + "/mb/collaborate/"
    book_app_url=  "http://" + app.config['PYBOSSA_HOST'] + "/pybossa/app/" + book_id + "_tt1/newtask"
    page_url = "http://www.archive.org/download/%s/page/n%d_w%d_h%d" % (book_id, page_id, 550, 700)
    
    bookInfo = archiveBookData(book_id)
    book_title = bookInfo['title'].encode('utf-8')
    top_pos = str(top_pos)
    left_pos = str(left_pos)
    bottom_pos = str(bottom_pos)
    right_pos = str(right_pos)

    text = ""
    templateArch = urllib2.urlopen(urllib2.Request(server_url + "/templates/facts-template.html"))

    for line in templateArch.readlines():
        line = line.replace("#server", server_url)
        line = line.replace("#book_app_url", book_app_url)
        line = line.replace("#book_list_url", book_list_url)
        line = line.replace("#fact_url", fact_url)
        line = line.replace("#page_url", page_url)
        
        line = line.replace("#user_name", user_name)
        line = line.replace("#book_title", book_title)
        line = line.replace("#top_pos", top_pos)
        line = line.replace("#left_pos", left_pos)
        line = line.replace("#bottom_pos", bottom_pos)
        line = line.replace("#right_pos", right_pos)

        text += line
    return text

def __get_user_name(user_id):
    con = None
    result = "Um voluntário"
    try:
        con = __create_db_connection("pybossa")
        cursor = con.cursor()
        query = "SELECT fullname FROM \"user\" WHERE id = " + str(user_id)
        print(query)
        cursor.execute(query)
        rows = cursor.fetchone()
        result = rows[0].split(" ")[0]

        con.commit()
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
    finally:
        if con:
            con.close()
        return result

@task(name="app_tt.engine.tasks.render_template")
def render_template(app_shortname, page):
    server_url = app.config['URL_TEMPLATES']
    templateArch = urllib2.urlopen(urllib2.Request(server_url + "/templates/" + page))
    
    text = ""
    for line in templateArch.readlines():
        line = line.replace("#server", server_url)
        line = line.replace("#app_shortname#", app_shortname.encode('utf-8'))
        text += line
    return text    

