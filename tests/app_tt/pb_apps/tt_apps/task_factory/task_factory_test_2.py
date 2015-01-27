# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps import task_factory 
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.core import pbclient
from app_tt.meb_exceptions.meb_exception import Meb_task_factory_exception 

import unittest

class task_factory_test_2(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_meta = Apptt_meta(short_name="sh_tt2",title="title2")
    
    def tearDown(self):
        if not self.app_tt_meta == None:
            pbclient.delete_app(self.app_tt_meta.app_id)
    
    # testing functions

    def test_get_task_01(self):
        self.app_tt_meta.add_task(task_info={"answer":"Yes", "page":1})
        self.app_tt_meta.add_task(task_info={"answer":"Yes", "page":2})
        self.app_tt_meta.add_task(task_info={"answer":"No", "page":3})
        
        tasks = pbclient.get_tasks(self.app_tt_meta.app_id)
        
        try:
            for task in tasks:
                t2 = task_factory.get_task(task.id)
                if task.id == t2.task.id:
                    self.assertEquals(t2.task.info["page"], task.info["page"])
                    self.assertEquals(t2.task.info["answer"], task.info["answer"])
                    self.assertEquals(t2.app_short_name, self.app_tt_meta.short_name)
        
        except Exception as e:
            print e
            assert False

    def test_get_task_02(self):
        try:
            task_factory.get_task(-1)
        except Meb_task_factory_exception as e:
            self.assertEquals(e.code, 1)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(task_factory_test_2)
    return suite

if __name__ == '__main__':
    unittest.main()