# -*- coding: utf-8 -*-
from flask import Blueprint, abort
from tasks import check_task, create_apps, close_task, create_task

blueprint = Blueprint('api', __name__)


@blueprint.route('/')
def index():
    return 'API'


@blueprint.route('/<book_id>/init')
def book_init(book_id):
    result = create_apps.delay(book_id)
    return str(result.get(propagate=True))


@blueprint.route('/<task_id>/done')
def check_app_done(task_id):
    done = check_task.delay(task_id)
    done = done.get()
    print done
    if(done):
        close_task.delay(task_id)
        create_task.delay(task_id)
    
    return str(done)
