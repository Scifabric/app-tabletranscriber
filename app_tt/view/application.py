import sys
import os
import urllib2
import json

from flask import Flask, render_template, request
from app_tt.engine.api import blueprint as api
import app_tt.default_settings as settings


app = Flask(__name__)
app.config.from_object(settings)

app.register_blueprint(api, url_prefix='/api')

def getAppData(app_short_name, pybossa_server):
    return json.load(urllib2.urlopen(pybossa_server + '/api/app?short_name='
        + app_short_name))


def getAppTasks(app_id, pybossa_server):
    return json.load(urllib2.urlopen(pybossa_server + '/api/task?app_id=%d' %
            app_id))

@app.route('/')
def home():
    return render_template("/home/index.html")

@app.route('/colabore', methods=['GET'])
def index():
    # get info configs from default config file
    NUM_APPS = 2
    pybossa_server = app.config['PYBOSSA_URL']

    bookid = error = None

    # get app's short name from form
    bookid_app = request.args.get('bookid', '')
    apps = []

    for i in range(NUM_APPS):
        app_uri = "%s_tt%d" % (bookid_app, (i+1))
        app_data = getAppData(app_uri, pybossa_server )

        apps.append({
                "num": i+1,
                "tasks": getAppTasks(app_data[0]["id"], pybossa_server),
                "url": pybossa_server + "/app/" + app_uri}
                )

    if(apps):
        app_tasks = [[this_app["num"], this_app["tasks"], this_app["url"]] for this_app in apps]

    else:
        error = "Erro, algum erro inesperado ocorreu, \
                por favor contate o administrador."
        print error
        return render_template('/error.html', error=error)
    print "passou"
    return render_template('/index.html',
            bookid=bookid_app,
            tasks=json.dumps(app_tasks))


if(__name__ == "__main__"):
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
