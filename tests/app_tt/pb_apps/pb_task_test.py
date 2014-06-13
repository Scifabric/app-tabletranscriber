# -*- coding: utf-8 -*-

from app_tt.pb_apps.pb_task import pb_task
from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select

import pbclient

import unittest

class pb_task_test(unittest.TestCase):
    
    def setUp(self):
        self.app = Apptt_select(short_name="sh_tt1", title="title1")
        self.app.add_task(task_info={"info1":1, "info2":2})
        self.app.add_task(task_info={"info3":3, "info4":4})
        
        tasks = pbclient.get_tasks(app_id=self.app.app_id)
        
        self.pb_task1 = pb_task(tasks[0].id, app_short_name=self.app.short_name)
        self.pb_task2 = pb_task(tasks[1].id, app_short_name=self.app.short_name)

    def tearDown(self):
        pbclient.delete_task(self.pb_task1.task.id)
        pbclient.delete_task(self.pb_task2.task.id)
        pbclient.delete_app(self.app.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            t1 = pb_task( -1, "sh_tt1")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
            self.assertEquals(e.msg, "MEB-PB-TASK-1: Cannot find task | task_id : -1 | app_short_name : sh_tt1")
    
    def test_init_02(self):
        try:
            t1 = pb_task( self.pb_task1.task.id, "sh")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)
            msg = "MEB-PB-TASK-2: Invalid shortname | task_id : %d | app_short_name : %s" % (self.pb_task1.task.id, "sh")
            self.assertEquals(e.msg, msg)
    
    def test_init_03(self):
        try:
            t1 = pb_task( self.pb_task1.task.id, "sh_tt")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)
            msg = "MEB-PB-TASK-2: Invalid shortname | task_id : %d | app_short_name : %s" % (self.pb_task1.task.id, "sh_tt")
            self.assertEquals(e.msg, msg)
    
    def test_get_book_id_01(self):
        try:
            self.assertEquals(self.pb_task1.app_short_name, self.app.short_name)
            self.assertEquals(self.pb_task1.get_book_id(), "sh")
        except Exception as e:
            assert False
    
    def test_close_task_01(self):
        try:
            self.pb_task1.close_task()
            self.assertEquals(self.pb_task1.task.state, 'completed')
        except Exception:
            assert False
    
    def test_get_task_runs_01(self):
        try:
            trs = self.pb_task1.get_task_runs()
            self.assertEquals(len(trs), 0)
            self.assertFalse(self.pb_task1.task.info.has_key('answer'))
            self.assertFalse(self.pb_task2.task.info.has_key('answer'))
        except Exception:
            assert False
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(pb_task_test)
    return suite
    
if __name__ == '__main__':
    unittest.main()