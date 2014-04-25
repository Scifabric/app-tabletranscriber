# -*- coding: utf-8 -*-
"""
"""

from app_tt.core import app as flask_app
from app_tt.pb_apps.apps import Apptt
import unittest
from app_tt.meb_exceptions import meb_exception
import os
import tempfile

class Apps_TestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, flask_app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flask_app.test_client()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(flask_app.config['DATABASE'])
        
    # testing functions

    def test_init_01(self):
        try:
            app_id = Apptt("", "", "")
        except meb_exception as e:
            assert e.code == 1
            assert e.msg == "MEB-1: App with empty name"

    def test_init_02(self):
        try:
            app_id = Apptt("name1", "", "")
        except meb_exception as e:
            assert e.code == 2
            assert e.msg == "MEB-2: App with empty shortname" 
    
    def test_init_03(self):
        try:
            app_id = Apptt("name1", "shortname1", "")
        except meb_exception as e:
            assert e.code == 3
            assert e.msg == "MEB-3: App with empty description"
    
    def test_init_04(self):
        try:
            app_id = Apptt("name1", "shortname1", "desc1")
        except meb_exception as e:
            assert False
    
    def test_init_05(self):
        try:
            app_id1 = Apptt("name1", "shortname1", "desc1")
            app_id2 = Apptt("n1", "shortname1", "d1")
        except meb_exception as e:
            assert app_id1 == app_id2
    
    def test_set_name_01(self):
        try:
            app_id1 = Apptt("name1", "shortname1", "desc1")
            
        except meb_exception as e:
            assert app_id1 == app_id2
    
if __name__ == '__main__':
    unittest.main()