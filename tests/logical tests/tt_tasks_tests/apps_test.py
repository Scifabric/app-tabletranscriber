# -*- coding: utf-8 -*-
"""
"""

from app_tt.pb_apps.apps import Apptt
import unittest
from app_tt.meb_exceptions import meb_exception
import os
import tempfile
import pbclient

class Apps_TestCase(unittest.TestCase):
    
    def setUp(self):
        self.app_tt = Apptt("name1", "shortname1", "desc1")
    
    def tearDown(self):
        pbclient.delete_app(self.app_tt.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            app = Apptt("", "", "")
        except meb_exception as e:
            assert e.code == 1
            assert e.msg == "MEB-1: App with empty name"

    def test_init_02(self):
        try:
            app = Apptt("name1", "", "")
        except meb_exception as e:
            assert e.code == 2
            assert e.msg == "MEB-2: App with empty shortname" 
    
    def test_init_03(self):
        try:
            app = Apptt("name1", "shortname1", "")
        except meb_exception as e:
            self.assertTrue(e.code == 3) 
            self.assertTrue(e.msg == "MEB-3: App with empty description")
    
    def test_init_04(self):
        try:
            app = Apptt("name1", "shortname1", "desc1")
        except meb_exception as e:
            assert False
        finally:
            self.assertTrue(pbclient.delete_app(app.app_id))
    
    def test_init_05(self):
        try:
            app1 = Apptt("name1", "shortname1", "desc1")
            app2 = Apptt("n1", "shortname1", "d1")
        except meb_exception as e:
            self.assertTrue(app1.app_id == app2.app_id)
        finally:
            self.assertTrue(pbclient.delete_app(app1.app_id))
            self.assertTrue(pbclient.delete_app(app2.app_id))
    
    def test_set_name_01(self):
        try:
            self.app_tt.set_name("name2")
            appPB = pbclient.get_app(self.app_tt.app_id)
            self.assertTrue(appPB.name == "name2")
        except meb_exception as e:
            assert False
    
    def test_set_template_01(self):
        try:
            self.app_tt.set_template("http://localhost/mb-static2/templates/template.html")
        except meb_exception as e:
            assert False
    
    def test_set_long_description_01(self):
        try:
            self.app_tt.set_long_description("http://localhost/mb-static2/long-description")
        except meb_exception as e:
            assert False
    
    def test_add_app_infos_01(self):
        try:
            self.app_tt.add_app_infos({})
        except meb_exception as e:
            assert False
            
if __name__ == '__main__':
    unittest.main()