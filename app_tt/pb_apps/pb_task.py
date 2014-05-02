import pbclient
import requests
import json
from app_tt.core import app


class pb_task(object):
    """
    Abstract Pybossa's Workflow Task class
    """
    def __init__(self, task_id, app_short_name):
        """
        Constructor of pb_task
        
        :params task_id: Pybossa Task Id
        """
        self.task = self.__get_pbtask(task_id)
        self.app_short_name = app_short_name

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
        
        #requests.put("%s/api/task/%s?api_key=%s" % 
        #             (app.config['PYBOSSA_URL'], self.task.id, app.config['API_KEY']),
        #                data=json.dumps(dict(state='completed')))

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
        data = json.loads(requests.get("%s/api/task/%s?api_key=%s" % (
            app.config['PYBOSSA_URL'], task_id,
            app.config['API_KEY'])).content)

        return pbclient.Task(data)

    def get_book_id(self):
        return self.app_short_name[:-4]
    
