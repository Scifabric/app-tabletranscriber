# -*- coding: utf-8 -*-
"""
"""

from app_tt.pb_apps.apps import Apptt
from app_tt.meb_exceptions.meb_exception import Meb_apps_exception

import pbclient

import unittest
import random

class Apps_TestCase(unittest.TestCase):
    
    def setUp(self):
        self.app_tt = Apptt("name1", "shortname1", "desc1")
    
    def tearDown(self):
        pbclient.delete_app(self.app_tt.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            app = Apptt("", "", "")
        except Meb_apps_exception as e:
            self.assertEquals(e.code, 1)
            self.assertEquals(e.msg, "MEB-APPS-1: App with empty name | app_id : %d | app_short_name : %s" % (app.app_id, app.short_name))

    def test_init_02(self):
        try:
            app = Apptt("name1", "", "")
        except Meb_apps_exception as e:
            self.assertEquals(e.code, 2)
            self.assertEquals(e.msg, "MEB-APPS-2: App with empty shortname | app_id : %d | app_short_name : %s" % (app.app_id, app.short_name))
    
    def test_init_03(self):
        try:
            app = Apptt("name1", "shortname1", "")
        except Meb_apps_exception as e:
            self.assertTrue(e.code == 3) 
            self.assertTrue(e.msg == "MEB-APPS-3: App with empty description | app_id : %d | app_short_name : %s" % (app.app_id, app.short_name))
    
    def test_init_04(self):
        try:
            app = Apptt("name1", "shortname1", "desc1")
        except Meb_apps_exception as e:
            assert False
        finally:
            self.assertTrue(pbclient.delete_app(app.app_id))
    
    def test_init_05(self):
        try:
            app1 = Apptt("name1", "shortname1", "desc1")
            app2 = Apptt("n1", "shortname1", "d1")
        except Meb_apps_exception as e:
            self.assertTrue(app1.app_id == app2.app_id)
        finally:
            self.assertTrue(pbclient.delete_app(app1.app_id))
            self.assertTrue(pbclient.delete_app(app2.app_id))
    
    def test_set_name_01(self):
        try:
            self.app_tt.set_name("name2")
            appPB = pbclient.get_app(self.app_tt.app_id)
            self.assertTrue(appPB.name == "name2")
        except Meb_apps_exception as e:
            assert False
    
    def test_set_template_01(self):
        try:
            content1 = "template content 1"
            self.app_tt.set_template(content1)
            app = pbclient.get_app(self.app_tt.app_id)
            self.assertEquals(app.info["task_presenter"], content1)
        except Meb_apps_exception as e:
            assert False
        
    def test_set_long_description_01(self):
        try:
            content_l_desc1 = "long description content 1"
            self.app_tt.set_long_description(content_l_desc1)
            app = pbclient.get_app(self.app_tt.app_id)
            self.assertEquals(app.long_description, content_l_desc1)
        except Meb_apps_exception as e:
            assert False
    
    def test_add_app_infos_02(self):
        try:
            self.app_tt.add_app_infos({"bla":"bbbbb"})
            app = pbclient.get_app(self.app_tt.app_id)
            self.assertTrue(app.info.has_key("bla"))
        except Meb_apps_exception as e:
            assert False
    
    def test_add_task_01(self):
        try:
            for i in range(0,15):
                self.app_tt.add_task({1: "info1", 2: "info2"})
            tasks = pbclient.find_tasks(self.app_tt.app_id)
            
            self.assertEquals(len(tasks), 15)
            
            for i in range(0,15):
                self.assertEquals(tasks[i].info['1'], unicode("info1", 'utf-8'))
                self.assertEquals(tasks[i].info['2'], unicode("info2", 'utf-8'))
        except Exception as e:
            assert False
    
    def test_add_task_02(self):
        try:
            for i in range(0,15):
                self.app_tt.add_task({1: "info1", 2: "info2"}, priority=random.randrange(0,1))
            tasks = pbclient.find_tasks(self.app_tt.app_id)
            
            self.assertEquals(len(tasks), 15)
            
            for i in range(0,15):
                self.assertEquals(tasks[i].info['1'], unicode("info1",'utf-8'))
                self.assertEquals(tasks[i].info['2'], unicode("info2",'utf-8'))
                self.assertTrue(tasks[i].priority_0 >= 0 and tasks[i].priority_0 <= 1)
        except Exception as e:
            print e
            assert False
    
    def test_add_task_03(self):
        try:
            self.app_tt.add_task({1: "info1", 2: "info2"}, priority=1.3)
            assert False
        except Meb_apps_exception as e:
            self.assertEquals(e.msg, "MEB-APPS-6: Task must be priority between 0 and 1 | app_id : %d | app_short_name : %s" % (app.app_id, app.short_name))
    
    def test_get_tasks_01(self):
        try:
            for i in range(0,15):
                self.app_tt.add_task({1: "info1", 2: "info2"})
            
            tasks = pbclient.find_tasks(self.app_tt.app_id)
            tasks2 = self.app_tt.get_tasks()
            
            self.assertEquals(len(tasks), 15)
            self.assertEquals(len(tasks2), 15)
            
            for t1 in tasks:
                for t2 in tasks2:
                    if t1.id == t2.id:
                        self.assertEquals(t1.info['1'], t2.info['1'])
                        self.assertEquals(t1.info['2'], t2.info['2'])
            
        except Exception as e:
            print e
            assert False
            
if __name__ == '__main__':
    unittest.main()