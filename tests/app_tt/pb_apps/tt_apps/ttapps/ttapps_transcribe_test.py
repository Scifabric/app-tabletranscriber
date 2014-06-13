# -*- coding: utf-8 -*-

from app_tt.pb_apps.tt_apps.ttapps import Apptt_transcribe
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception

from app_tt.core import app

import pbclient

import unittest
import os
import tempfile
import random

class ttapps_transcribe_test(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_transcribe = None
    
    def tearDown(self):
        if not self.app_tt_transcribe == None:
            pbclient.delete_app(self.app_tt_transcribe.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            self.app_tt_transcribe = Apptt_transcribe(short_name="sh_tt4")
            
            self.assertEquals(self.app_tt_transcribe.short_name, "sh_tt4")
            self.assertEquals(self.app_tt_transcribe.name, unicode("Transcrição", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
        except Exception as ex:
            assert False
    
    def test_init_02(self):
        try:
            self.app_tt_transcribe = Apptt_transcribe(short_name="sh_tt4",title="title4")
            
            self.assertEquals(self.app_tt_transcribe.short_name, "sh_tt4")
            self.assertEquals(self.app_tt_transcribe.name, unicode("title4 Transcrição", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
    
    def test_init_03(self):
        try:
            self.app_tt_transcribe = Apptt_transcribe(title="title4")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 4)

    def test_init_04(self):
        try:
            self.app_tt_transcribe = Apptt_transcribe(short_name="sh4")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 8)

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ttapps_transcribe_test)
    return suite

            
if __name__ == '__main__':
    unittest.main()