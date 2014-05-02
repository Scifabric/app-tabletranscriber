# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps import task_factory 
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.core import pbclient

import unittest

class TaskFactory_TestCase(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_select = Apptt_select(short_name="sh_tt1",title="title1")
    
    def tearDown(self):
        if not self.app_tt_select == None:
            pbclient.delete_app(self.app_tt_select.app_id)
    
    # testing functions

    def test_get_task_01(self):
        self.app_tt_select.add_task(task_info={"answer":"Yes", "page":1})
        self.app_tt_select.add_task(task_info={"answer":"Yes", "page":2})
        self.app_tt_select.add_task(task_info={"answer":"No", "page":3})
        
        tasks = pbclient.get_tasks(self.app_tt_select.app_id)
        
        for task in tasks:
            t2 = task_factory.get_task(task.id)
            if task.id == t2.id:
                self.assertEquals(t2.info["page"], task.info["page"])
                self.assertEquals(t2.info["answer"], task.info["answer"]) 



if __name__ == '__main__':
    unittest.main()