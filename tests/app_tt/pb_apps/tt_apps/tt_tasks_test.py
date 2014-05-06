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
            t1 = TTTask1( -1, "sh_tt1")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
    
    def test_init_02(self):
        try:
            t1 = TTTask1( self.app.app_id, "sh_t")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)

    def test_get_next_app_01(self):
        try:
            nx_app = self.task1.get_next_app()
            self.assertEquals(nx_app.short_name, self.app.short_name[:-1] + "2")
        except Exception:
            assert False
    
    def test_check_answer_01(self):
        try:
            trs = self.task1.get_task_runs()
            
            for i in range(0,2):
                trs[i] = pbclient.TaskRun()
                trs[i].info["answer"] = "Yes"
            
            self.assertTrue(self.task1.check_answer())
        
        except Exception as e:
            print e
            assert False
    
    def test_check_answer_02(self):
        try:
            trs = self.task1.get_task_runs()
            
            for i in range(0,2):
                trs[i] = pbclient.TaskRun()
                if i == 0:
                    trs[i].info["answer"] = "Yes"
                else:
                    trs[i].info["answer"] = "No"
            
            self.assertFalse(self.task1.check_answer())
        
        except Exception as e:
            print e
            assert False


if __name__ == '__main__':
    unittest.main()

