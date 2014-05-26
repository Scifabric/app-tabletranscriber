# -*- coding: utf-8 -*-

from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct
from app_tt.meb_exceptions.meb_exception import Meb_ttapps_exception

from app_tt.core import app

import pbclient

import unittest
import os
import tempfile
import random

class ttapps_struct_test(unittest.TestCase):
    
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

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(ttapps_struct_test)
    return suite

            
if __name__ == '__main__':
    unittest.main()