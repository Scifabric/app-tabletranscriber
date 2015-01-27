# -*- coding: utf-8 -*-

from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception

from app_tt.core import app

import pbclient

import unittest
import os
import tempfile
import random

class ttapps_select_test(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_select = None
    
    def tearDown(self):
        if not self.app_tt_select == None:
            pbclient.delete_app(self.app_tt_select.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            self.app_tt_select = Apptt_select(short_name="sh_tt1")
            
            self.assertEquals(self.app_tt_select.short_name, "sh_tt1")
            self.assertEquals(self.app_tt_select.name, unicode("Seleção", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
        except Exception as ex:
            assert False
    
    def test_init_02(self):
        try:
            self.app_tt_select = Apptt_select(short_name="sh_tt1",title="title1")
            
            self.assertEquals(self.app_tt_select.short_name, "sh_tt1")
            self.assertEquals(self.app_tt_select.name, unicode("title1 Seleção", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
    
    def test_init_03(self):
        try:
            self.app_tt_select = Apptt_select(title="title1")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 1)
    
    def test_init_04(self):
        try:
            self.app_tt_select = Apptt_select(short_name="sh1")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 5)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ttapps_select_test)
    return suite

            
if __name__ == '__main__':
    unittest.main()