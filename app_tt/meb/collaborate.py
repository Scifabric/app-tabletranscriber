# -*- coding:utf-8 -*-
import json

from app_tt.core import app as flask_app
from app_tt.core import pbclient
from flask import Blueprint, render_template
from app_tt.meb.util import crossdomain
from app_tt.pagination import Pagination
import sys
import requests

blueprint = Blueprint('collaborate', __name__)
pybossa_server = flask_app.config['PYBOSSA_URL']
pybossa_host = flask_app.config['PYBOSSA_HOST']
cors_headers = ['Content-Type', 'Authorization']

api_key = flask_app.config['API_KEY']
max_limit = sys.maxint

@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/page/<int:page>')
@crossdomain(origin='*', headers=cors_headers)
def index(page):
    per_page = 5
    apps = json.loads(requests.get(pybossa_server + '/api/app?api_key=%s&limit=%d' % (api_key, max_limit)).content)
    book_stack = []
    book_data = []
    
    valid_books = ['estatisticasdodi1950depa', 'mensagemdogovern1912gove','caracterizaoeten2001bras', 'MemmoriaParaiba1841A1847', 'anuario1916pb', 'sinopse1937pb', 'rpparaiba1918']
    
    for app in apps:
        print(app["short_name"])
        book_id = app["short_name"][:-4]

        if(book_id not in book_stack and app["short_name"][:-4] in valid_books):
            try:
                app["info"]["title"]
                book_progress = get_book_progress(book_id)
                app["info"]["progress"] = book_progress["overall_progress"]
                app["info"]["newtask"] = get_new_task_link(book_progress["tasks_progress"], book_id)
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

    return render_template('/collaborate.html', books=books, pagination=pagination)

def get_new_task_link(tasks_progress, bookid):
    app_with_available_task = 'tt1'
    tt_suffix = ['tt1', 'tt2', 'tt3', 'tt4']

    for suffix in tt_suffix:
        if (tasks_progress[suffix]['total'] > tasks_progress[suffix]['completed']):
            app_with_available_task = suffix
            break
    return pybossa_server + '/app/' + bookid + '_' + app_with_available_task + '/newtask'

def get_tasks_progress(bookid):
    tt_suffix = ['tt1', 'tt2', 'tt3', 'tt4']
    result = dict(tt1=dict(total=0, completed=0), tt2=dict(total=0, completed=0), tt3=dict(total=0, completed=0), tt4=dict(total=0, completed=0))
    
    for suffix in tt_suffix:
        app = pbclient.find_app(short_name=str(bookid) + "_" + suffix)[0]
        tasks = pbclient.get_tasks(app.id, limit=max_limit)
        result[suffix]['total'] = len(tasks)
        
        for task in tasks:
            if task.state == 'completed':
                result[suffix]['completed'] += 1
                
    return result

def get_book_progress(bookid):
    t_progress = get_tasks_progress(bookid)
    tt_suffix = ['tt1', 'tt2', 'tt3', 'tt4']
    overall = 0
    overall_completed = 0
    for suffix in tt_suffix:
        overall += t_progress[suffix]['total']       
        overall_completed += t_progress[suffix]['completed']
    
    book_progress = dict(tasks_progress=t_progress, overall_progress=round((overall_completed/float(overall)) * 100, 2))
    return book_progress
