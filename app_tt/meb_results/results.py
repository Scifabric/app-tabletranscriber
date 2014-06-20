# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

import urllib2
import json

from app_tt.core import app as flask_app

import sys
import requests

blueprint = Blueprint('results', __name__)

pybossa_server = flask_app.config['PYBOSSA_URL']
max_limit = sys.maxint

def getAppData(app_short_name, pybossa_server):
    return json.load(urllib2.urlopen(pybossa_server + '/api/app?short_name='
         + app_short_name))[0]
 
 
def getAppTasks(app_id, pybossa_server):
     return json.load(urllib2.urlopen(pybossa_server + '/api/task?app_id=%d&limit=%d' %
             (app_id, max_limit)))

@blueprint.route('/book', methods=['GET'])
def book():
    # get info configs from default config file
    NUM_APPS = 4
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
    
    return render_template('/results.html',
            bookid=bookid_app,
            appTasks=app_tasks)