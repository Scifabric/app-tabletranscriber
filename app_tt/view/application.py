from flask import Flask, render_template, request, url_for
from app_tt.engine.api import blueprint as api
from collaborate import blueprint as collaborate
import app_tt.default_settings as settings


app = Flask(__name__)
app.config.from_object(settings)

app.register_blueprint(collaborate, url_prefix='/collaborate')
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def home():
    return render_template("/home/index.html")


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

if(__name__ == "__main__"):
    app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
