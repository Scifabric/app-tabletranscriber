# -*- coding: utf-8 -*-

from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception

from app_tt.core import app

import pbclient

import unittest
import os
import tempfile
import random

class ttapps_meta_test(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_meta = None
    
    def tearDown(self):
        if not self.app_tt_meta == None:
            pbclient.delete_app(self.app_tt_meta.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            self.app_tt_meta = Apptt_meta(short_name="sh_tt2")
            
            self.assertEquals(self.app_tt_meta.short_name, "sh_tt2")
            self.assertEquals(self.app_tt_meta.name, unicode("Marcação", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
        except Exception as ex:
            assert False
    
    def test_init_02(self):
        try:
            self.app_tt_meta = Apptt_meta(short_name="sh_tt2",title="title2")
            
            self.assertEquals(self.app_tt_meta.short_name, "sh_tt2")
            self.assertEquals(self.app_tt_meta.name, unicode("title2 Marcação", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
    
    def test_init_03(self):
        try:
            self.app_tt_meta = Apptt_meta(title="title2")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 2)

    def test_init_04(self):
        try:
            self.app_tt_meta = Apptt_meta(short_name="sh2")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 6)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ttapps_meta_test)
    return suite

            
if __name__ == '__main__':
    unittest.main()