from flask import Blueprint, abort
from tasks import check_app_done

blueprint = Blueprint('api', __name__)


@blueprint.route('/')
def index():
    return 'API'


@blueprint.route('/app/<short_name>/done')
def check_app_done(short_name):
    TIMEOUT = 10
    result = check_app_done(short_name)
    if(result.ready()):
        return result
    else:
        result.get(timeout=TIMEOUT)
        if(result.ready()):
            return result
        else:
            abort(444)
