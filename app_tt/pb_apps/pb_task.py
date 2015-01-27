import pbclient
import requests
import json

from app_tt.core import app, logger
from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception

class pb_task(object):
    """
    Abstract Pybossa's Workflow Task class
    """
    def __init__(self, task_id, app_short_name):
        """
        Constructor of pb_task
        
        :params task_id: Pybossa Task Id
        """
        self.app_short_name = None
        try:
            self.__set_app_shortname(task_id, app_short_name)
            self.task = self.__get_pbtask(task_id)
        except Meb_pb_task_exception as e:
            logger.error(e)
            raise e
    
    def __set_app_shortname(self, task_id, app_sh_name):
        if len(app_sh_name) >= 4:
            validExts = ["_tt1", "_tt2", "_tt3", "_tt4"]
            for ext in validExts:
                if ext in app_sh_name:
                    self.app_short_name = app_sh_name
                    return
            raise Meb_pb_task_exception(2, task_id, app_sh_name)
        else:
            raise Meb_pb_task_exception(2, task_id, app_sh_name)
        
    
    def add_next_task(self):
        """
        Add a next task at pybossa, following the workflow
        """
        raise NotImplemented("Should have implemented this")

    def close_task(self):
        """
        Closes current task at pybossa
        """
        
        self.task.state = "completed"
        pbclient.update_task(self.task)
        
    def check_answer(self):
        """
        Verify if the task's answers are ok to finish it

        :returns: A confirmation that the task is ready to be finished
        :rtype: boolean
        """
        raise NotImplemented("Should have implemented this")

    def get_next_app(self):
        raise NotImplemented("Should have implemented this")

    def get_task_runs(self):
        """
        Get all the task runs for this task

        :returns: A list with TaskRun objects
        :rtype: list
        """
        data = json.loads(requests.get("%s/api/taskrun?task_id=%s" % (
            app.config['PYBOSSA_URL'], self.task.id)).content)
        return [pbclient.TaskRun(taskrun) for taskrun in data]

    def __get_pbtask(self, task_id):
        try:
            data = json.loads(requests.get("%s/api/task/%s?api_key=%s" % (
                app.config['PYBOSSA_URL'], task_id,
                app.config['API_KEY'])).content)
        
            if data.has_key("status") and data["status"] == "failed":
                raise Meb_pb_task_exception(1, task_id, self.app_short_name)

            return pbclient.Task(data)
        
        except Exception:
            raise Meb_pb_task_exception(1, task_id, self.app_short_name)

    def get_book_id(self):
        return self.app_short_name[:-4]
    
