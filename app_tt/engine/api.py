# -*- coding: utf-8 -*-
from flask import Blueprint
from tasks import check_task, create_apps, close_task
from tasks import create_task, available_tasks

blueprint = Blueprint('api', __name__)


@blueprint.route('/')
def index():
    """

    Memoria Brasil Api root entry point

    """
    return 'Memoria Brasil API'


@blueprint.route('/<book_id>/init')
def book_init(book_id):
    """

    Api entry point to create pybossa applications
    and tasks for a book at internet archive

    :arg book_id: Book id from internet archive,
    example: estatisticasdodi1950depa
    :returns: Creating status

    """
    result = create_apps.delay(book_id)
    return str(result.get(propagate=True))


@blueprint.route('/<task_id>/done')
def check_task_done(task_id):
    """

    Api entry point that checks if the given task is finished

    :arg task_id: Integer pybossa task id
    :returns: If task is finished

    """
    print("Teste 1: " + task_id)
    done = check_task.delay(task_id)
    done = done.get()
    print done
    if(done):  # if tasks is done, close it
        close_task.delay(task_id)
        create_task.delay(task_id)

    return str(done)


@blueprint.route('/<task_id>/available_tasks')
def are_there_tasks(task_id):
    """

    Api entry point to check if there are open
    tasks at next workflow applications

    :arg task_id: Task id from the current workflow app
    :returns: If there are available tasks in the workflow
    """
    available = available_tasks.delay(task_id)
    return str(available.get())
