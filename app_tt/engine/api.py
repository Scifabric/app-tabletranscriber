# -*- coding: utf-8 -*-
from flask import Blueprint, request
from tasks import check_task, create_apps, close_task, close_t1
from tasks import create_task, available_tasks, save_fact, submit_report, get_fact_page, render_template, book_progress
import json

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

@blueprint.route('/<book_id>/init_and_close_t1')
def book_init_close_t1(book_id):
    
    result = create_apps.delay(book_id)
    success = result.get(propagate=True)
    
    if success:
        close_t1.delay(book_id)
    return str(success)

@blueprint.route('/<task_id>/done')
def check_task_done(task_id):
    """

    Api entry point that checks if the given task is finished

    :arg task_id: Integer pybossa task id
    :returns: If task is finished

    """
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

@blueprint.route('/save_fact', methods=['POST'])
def execute_save_fact():
    factInfo = json.loads(request.data)
    done = save_fact.delay(factInfo)
    return str(done.get())

@blueprint.route('/<app_shortname>/<task_id>/report', methods=['POST'])
def report(app_shortname, task_id):
    reportInfo = json.loads(request.data)
    done = submit_report.delay(app_shortname, task_id,
                               reportInfo['message'],
                               reportInfo['u_id'])
    return str(done.get())

@blueprint.route('/fact/<fact_id>')
def fact_page(fact_id):
    page = get_fact_page.delay(fact_id)
    return page.get()

@blueprint.route('/render_template/<task_shortname>/<page>')
def render_pages_template(task_shortname, page):
    rendered_page = render_template.delay(task_shortname, page)
    return rendered_page.get()

@blueprint.route('/get_book_progress/<string(maxlength=255):bookid>')
def get_book_progress(bookid):
    progress = book_progress.delay(bookid)
    return progress.get()
