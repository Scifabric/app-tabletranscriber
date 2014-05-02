# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask1
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask2
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask3
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask4
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select

from app_tt.core import pbclient
import unittest

from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception

class TT_Task1_TestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = Apptt_select(short_name="sh_tt1", title="title1")
        self.app.add_task(task_info={"info1":1, "info2":2})
        self.app.add_task(task_info={"info3":3, "info4":4})
        
        tasks = pbclient.get_tasks(app_id=self.app.app_id)
        
        self.task1 = TTTask1(tasks[0].id, app_short_name=self.app.short_name)
        self.task2 = TTTask1(tasks[1].id, app_short_name=self.app.short_name)

    def tearDown(self):
        pbclient.delete_task(self.task1.task.id)
        pbclient.delete_task(self.task2.task.id)
        pbclient.delete_app(self.app.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            t1 = TTTask1( "-1", "sh")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
            self.assertEquals(e.msg, "MEB-PB-TASK-FACTORY-1: Cannot find task | task_id : -1")


if __name__ == '__main__':
    unittest.main()