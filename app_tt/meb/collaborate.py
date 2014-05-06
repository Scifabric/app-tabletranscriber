# -*- coding:utf-8 -*-
import json

from app_tt.core import app as flask_app
from app_tt.core import pbclient
from flask import Blueprint, render_template
from app_tt.pagination import Pagination
import sys
import requests


blueprint = Blueprint('collaborate', __name__)
pybossa_server = flask_app.config['PYBOSSA_URL']

api_key = flask_app.config['API_KEY']
max_limit = sys.maxint

@blueprint.route('/', defaults={'page': 1})
@blueprint.route('/page/<int:page>')
def index(page):
    per_page = 5
    apps = json.loads(requests.get(pybossa_server + '/api/app?api_key=%s&limit=%d' % (api_key, max_limit)).content)
    book_stack = []
    book_data = []
    
    valid_books = ['estatisticasdodi1950depa', 'mensagemdogovern1912gove','caracterizaoeten2001bras', 'MemmoriaParaiba1841A1847', 'anuario1916pb']
    
    for app in apps:
        book_id = app["short_name"][:-4]

        if(book_id not in book_stack and app["hidden"] == 0):
            try:
                app["info"]["title"]
                app["info"]["newtask"] = pybossa_server + '/app/' + book_id + '_tt1/newtask'
                book_stack.append(book_id)
                
                if app["short_name"][:-4] in valid_books:
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

    return render_template('/collaborate.html',
            books=books,
            pagination=pagination)


@blueprint.route('/progress/<string(maxlength=255):bookid>')
def progress(bookid):

    tt_suffix = ['_tt1', '_tt2', '_tt3', '_tt4']
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
    
