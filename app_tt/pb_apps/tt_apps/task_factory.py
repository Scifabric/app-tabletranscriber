from app_tt.core import app
import tt_tasks
import json
import requests
from app_tt.meb_exceptions.meb_exception import Meb_task_factory_exception
from app_tt.core import logger

def get_task(task_id):
    """
    Returns a specific task based in PyBossa task_id

    :params task_id: Pybossa's task_id
    """
    try:
        pb_app = __find_app_by_taskid(task_id)
        app_short_name = pb_app["short_name"]
        task_type = app_short_name[-1]
        task = None

        if task_type == "1":
            task = tt_tasks.TTTask1(task_id, app_short_name)

        elif task_type == "2":
            task = tt_tasks.TTTask2(task_id, app_short_name)

        elif task_type == "3":
            task = tt_tasks.TTTask3(task_id, app_short_name)

        elif task_type == "4":
            task = tt_tasks.TTTask4(task_id, app_short_name)

        return task
    
    except Exception:
        logger.error(Meb_task_factory_exception(1, task_id))
        raise Meb_task_factory_exception(1, task_id)

def __find_app(**keyargs):
    """""
    Find one pybossa app by a given params

    :returns: One pybossa's app data
    :rtype: dict
    """
    return json.loads(requests.get("%s/api/app" % (
        app.config['PYBOSSA_URL']),
        params=keyargs).content)[0]  # get the pb_appdata dict


def __find_app_by_taskid(task_id):
    """""
    Find a pybossa app by a pybossa task id

    :returns: The pybossa's app data
    :rtype: dict
    """

    meta_task = requests.get("%s/api/task/%s?api_key=%s" % (
        app.config['PYBOSSA_URL'],
        task_id, app.config['API_KEY'])).content

    try:
        task = json.loads(meta_task)  # get task data
        return __find_app(id=task["app_id"])
    except:
        raise
