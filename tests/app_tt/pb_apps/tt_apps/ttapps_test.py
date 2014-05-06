# -*- coding: utf-8 -*-
"""
"""

from app_tt.pb_apps.tt_apps.ttapps import Apptt_select
from app_tt.pb_apps.tt_apps.ttapps import Apptt_meta
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct
from app_tt.pb_apps.tt_apps.ttapps import Apptt_transcribe
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception

from app_tt.core import app

import pbclient

import unittest
import os
import tempfile
import random

class TTApp_select_TestCase(unittest.TestCase):
    
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

class TTApp_meta_TestCase(unittest.TestCase):
     
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

class TTApp_struct_TestCase(unittest.TestCase):
    
    def setUp(self):
        self.app_tt_struct = None
    
    def tearDown(self):
        if not self.app_tt_struct == None:
            pbclient.delete_app(self.app_tt_struct.app_id)
    
    # testing functions

    def test_init_01(self):
        try:
            self.app_tt_struct = Apptt_struct(short_name="sh_tt3")
            
            self.assertEquals(self.app_tt_struct.short_name, "sh_tt3")
            self.assertEquals(self.app_tt_struct.name, unicode("Estrutura", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
        except Exception as ex:
            assert False
    
    def test_init_02(self):
        try:
            self.app_tt_struct = Apptt_struct(short_name="sh_tt3",title="title3")
            
            self.assertEquals(self.app_tt_struct.short_name, "sh_tt3")
            self.assertEquals(self.app_tt_struct.name, unicode("title3 Estrutura", "utf-8"))
            
        except Meb_ttapps_exception as e:
            assert False
    
    def test_init_03(self):
        try:
            self.app_tt_struct = Apptt_struct(title="title3")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 3)

    def test_init_04(self):
        try:
            self.app_tt_struct = Apptt_struct(short_name="sh3")
            assert False
            
        except Meb_ttapps_exception as e:
            self.assertEquals(e.code, 7)

    def test_create_dirs_01(self):
        try:
            self.app_tt_struct = Apptt_struct(short_name="sh_tt3",title="title3")
            
            self.assertEquals(self.app_tt_struct.short_name, "sh_tt3")
            self.assertEquals(self.app_tt_struct.name, unicode("title3 Estrutura", "utf-8"))
            
            dirs = ["alta_resolucao",
                "baixa_resolucao",
                "metadados/entrada",
                "metadados/saida",
                "metadados/tabelasAlta",
                "metadados/tabelasBaixa",
                "metadados/respostaUsuarioTT",
                "metadados/modelPreview",
                "transcricoes",
                "transcricoes/texts",
                "transcricoes/confidences",
                "selections"]

            for d in dirs:
                p = "%s/books/%s/%s" % (app.config['CV_MODULES'], self.app_tt_struct.short_name[:-4], d)
                self.assertTrue(os.path.exists(p))
            
        except Meb_ttapps_exception as e:
            assert False
 
class TTApp_transcribe_TestCase(unittest.TestCase):
    
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
            
if __name__ == '__main__':
    unittest.main()