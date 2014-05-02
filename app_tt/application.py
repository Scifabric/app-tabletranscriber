from flask import render_template, request, url_for
from engine.api import blueprint as api
from meb.collaborate import blueprint as collaborate
from administration.admin import blueprint as admin
from meb_results.results import blueprint as results
from core import app, logger

app.register_blueprint(collaborate, url_prefix='/collaborate')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(results, url_prefix='/results')

@app.route('/')
def home():
    return render_template("/index.html")


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

# LEMBRAR DE TIRAR O DEBUG MODE QUANDO EM PRODUCAO ==> RISCO DE SEGURANCA
if(__name__ == "__main__"):
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
