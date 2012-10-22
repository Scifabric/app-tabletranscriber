from flask import Blueprint, abort
from tasks import check_task, create_apps

blueprint = Blueprint('api', __name__)

@blueprint.route('/')
def index():
    return 'API'


@blueprint.route('/<book_id>/init')
def book_init(book_id):
    TIMEOUT = 20
    result = create_apps.delay(book_id)
    if(result.ready()):
        return result
    else:
        result.get(timeout=TIMEOUT)
        if(result.ready()):
            return result
        else:
            abort(444)


@blueprint.route('/<task_id>/done')
def check_app_done(task_id):
    TIMEOUT = 10
    result = check_task.delay(task_id)
    if(result.ready()):
        return True
    else:
        result.get(timeout=TIMEOUT)
        if(result.ready()):
            return True
        else:
            abort(444)

