# -*- coding:utf-8 -*-

import urllib2
import json

from app_tt.core import app as flask_app
from app_tt.core import pbclient
from flask import Blueprint, render_template, request
from app_tt.util import Pagination
import sys
import requests


blueprint = Blueprint('collaborate', __name__)
pybossa_server = flask_app.config['PYBOSSA_URL']

api_key = flask_app.config['API_KEY']
max_limit = sys.maxint


def getAppData(app_short_name, pybossa_server):
    return json.load(urllib2.urlopen(pybossa_server + '/api/app?short_name='
        + app_short_name))[0]


def getAppTasks(app_id, pybossa_server):
    return json.load(urllib2.urlopen(pybossa_server + '/api/task?app_id=%d&limit=%d' %
            (app_id, max_limit)))


@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/page/<int:page>')
def index(page):
    per_page = 5
    apps = json.loads(requests.get(pybossa_server + '/api/app?api_key=%s&limit=%d' % (api_key, max_limit)).content)
    book_stack = []
    book_data = []

    for app in apps:
        book_id = app["short_name"][:-4]

        if(book_id not in book_stack and app["hidden"] == 0):
            try:
                app["info"]["title"]
                book_stack.append(book_id)
                book_data.append(app)
            except KeyError:
                print "It's not a tt app"
            except Exception, e:
                print str(e)

    count = len(book_data)
    books = []
    for index in range((page - 1) * per_page, page * per_page):
        if(index < count):
            books.append(book_data[index])

    if(not book_data and page != 1):
        error = "Oops! Essa página não existe, contate o administrador"
        return render_template('/error.html', error=error)

    pagination = Pagination(page, per_page, count)

    return render_template('/collaborate/index.html',
            books=books,
            pagination=pagination)


@blueprint.route('/progress/<string(maxlength=255):bookid>')
def progress(bookid):

    tt_suffix = ['_tt1', '_tt2', '_tt3']  #TODO: Add tt4 when it's ready
    overall = 0
    overall_completed = 0
    for suffix in tt_suffix:
        completed = 0
        app = pbclient.find_app(short_name=str(bookid) + suffix)[0]
        tasks = pbclient.get_tasks(app.id, limit=max_limit)
        overall += len(tasks)
        for task in tasks:
            if task.state == 'completed':
                completed += 1
        
        overall_completed += completed

    try:
        progress = (overall_completed/float(overall)) * 100
    except:
        return render_template('/progress.html', progress=0)

    return render_template('/progress.html', progress=progress)


@blueprint.route('/book', methods=['GET'])
def book():
    # get info configs from default config file
    NUM_APPS = 2
    error = None

    # get app's short name from form
    bookid_app = request.args.get('bookid','')
    apps = []

    for i in range(NUM_APPS):
        app_uri = "%s_tt%d" % (bookid_app, (i+1))
        app_data = getAppData(app_uri, pybossa_server )
        tasks = getAppTasks(app_data["id"], pybossa_server)
        apps.append({
                "name" : app_data["name"],
                "img_url": str(i+1),
                "tasks": tasks,
                "finished": [task for task in tasks if task["state"] == "completed"],
                "url": pybossa_server + "/app/" + app_uri})

    if(apps):
        app_tasks = apps

    else:
        error = "Erro, algum erro inesperado ocorreu, \
                por favor contate o administrador."
        return render_template('/error.html', error=error)
    return render_template('/collaborate/book.html',
            bookid=bookid_app,
            appTasks=app_tasks)
