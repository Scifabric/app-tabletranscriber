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


@app.route('/colabore', methods=['GET'])
def index():
    # get info configs from default config file
    pybossa_host = app.config['PYBOSSA_HOST']
    pybossa_port = app.config['PYBOSSA_PORT']
    pybossa_server = 'http://%s:%d' % (pybossa_host, pybossa_port)

    bookid = title = volume = error = None

    # get app's short name from form
    pybossa_app_tt1 = request.args.get('tt1', '')
    pybossa_app_tt2 = request.args.get('tt2', '')
    pybossa_app_tt3 = request.args.get('tt3', '')
    pybossa_app_tt4 = request.args.get('tt4', '')

    # get app data info for each app
    data_tt1 = getAppData(pybossa_app_tt1, pybossa_server)
    data_tt2 = getAppData(pybossa_app_tt2, pybossa_server)
    data_tt3 = getAppData(pybossa_app_tt3, pybossa_server)
    data_tt4 = getAppData(pybossa_app_tt4, pybossa_server)

    if(data_tt1 and data_tt2 and data_tt3 and data_tt4):
        # use app1 infos to feed the page
        bookid = data_tt1[0]['info']['bookId']
        title = data_tt1[0]['info']['title']
        volume = data_tt1[0]['info']['volume']
        tt1_tasks = getAppTasks(data_tt1[0]['id'], pybossa_server)
        tt2_tasks = getAppTasks(data_tt2[0]['id'], pybossa_server)
        tt3_tasks = getAppTasks(data_tt3[0]['id'], pybossa_server)
        tt4_tasks = getAppTasks(data_tt4[0]['id'], pybossa_server)

    else:
        error = "Erro, algum erro inesperado ocorreu, \
                por favor contate o administrador."
        return render_template('/error.html', error=error)

    return render_template('/index.html', bookname=title,
            bookid=bookid, volume=volume,
            tt1=json.dumps(tt1_tasks),
            tt2=json.dumps(tt2_tasks),
            tt3=json.dumps(tt3_tasks),
            tt4=json.dumps(tt4_tasks),
            tt1_url=pybossa_server + "/app/" + pybossa_app_tt1,
            tt2_url=pybossa_server + "/app/" + pybossa_app_tt2,
            tt3_url=pybossa_server + "/app/" + pybossa_app_tt3,
            tt4_url=pybossa_server + "/app/" + pybossa_app_tt4)

if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
