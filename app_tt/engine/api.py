from flask import Blueprint, abort
from tasks import check_task, create_apps

blueprint = Blueprint('api', __name__)


@blueprint.route('/')
def index():
    return 'API'


@blueprint.route('/<book_id>/init')
def book_init(book_id):
    result = create_apps.delay(book_id)
    return str(result.get())


@blueprint.route('/<task_id>/done')
def check_app_done(task_id):
    result = check_task.delay(task_id)
    return str(result.get())
