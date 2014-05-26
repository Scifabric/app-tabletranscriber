# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask3
from app_tt.pb_apps.tt_apps.ttapps import Apptt_struct

from app_tt.core import pbclient, app as app_flask
import unittest
import requests
import json
import time

from tests.app_tt.base import delete_book, authenticate_fb_user, submit_answer
from app_tt.data_mngr import data_manager as data_mngr 

from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception, Meb_exception_tt3

class tt3_task_with_zoom_test(unittest.TestCase):
    
    def setUp(self):
        book_title = "rpparaiba1918_title"
        self.app = Apptt_struct(short_name="rpparaiba1918_tt3", title=book_title)
        
        self.app.add_task(task_info=dict(
                                         hasZoom=True,
                                         zoom=[0, 0, 489, 168], 
                                         coords=[[0, 0, 7, 9], [7, 0, 37, 9], [37, 0, 118, 9], [118, 0, 251, 9], [251, 0, 489, 9], [0, 9, 7, 53], [7, 9, 37, 53], [37, 9, 118, 53], [118, 9, 251, 53], [251, 9, 489, 53], [0, 53, 7, 61], [7, 53, 37, 61], [37, 53, 118, 61], [118, 53, 251, 61], [251, 53, 489, 61], [0, 61, 7, 100], [7, 61, 37, 100], [37, 61, 118, 100], [118, 61, 251, 100], [251, 61, 489, 100], [0, 100, 7, 144], [7, 100, 37, 144], [37, 100, 118, 144], [118, 100, 251, 144], [251, 100, 489, 144], [0, 144, 7, 153], [7, 144, 37, 153], [37, 144, 118, 153], [118, 144, 251, 153], [251, 144, 489, 153], [0, 153, 7, 181], [7, 153, 37, 181], [37, 153, 118, 181], [118, 153, 251, 181], [251, 153, 489, 181], [0, 181, 7, 239], [7, 181, 37, 239], [37, 181, 118, 239], [118, 181, 251, 239], [251, 181, 489, 239], [0, 239, 7, 280], [7, 239, 37, 280], [37, 239, 118, 280], [118, 239, 251, 280], [251, 239, 489, 280], [0, 280, 7, 289], [7, 280, 37, 289], [37, 280, 118, 289], [118, 280, 251, 289], [251, 280, 489, 289], [0, 289, 7, 506], [7, 289, 37, 506], [37, 289, 118, 506], [118, 289, 251, 506], [251, 289, 489, 506]], 
                                         table_id=0, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image1_0.png", 
                                         page=1
                                         )
                          )
        
        self.app.add_task(task_info=dict(
                                         hasZoom=True,
                                         zoom=[0, 0, 100, 168], 
                                         coords=[[0, 0, 7, 9], [7, 0, 37, 9], [37, 0, 118, 9], [118, 0, 251, 9], [251, 0, 489, 9], [0, 9, 7, 53], [7, 9, 37, 53], [37, 9, 118, 53], [118, 9, 251, 53], [251, 9, 489, 53], [0, 53, 7, 61], [7, 53, 37, 61], [37, 53, 118, 61], [118, 53, 251, 61], [251, 53, 489, 61], [0, 61, 7, 100], [7, 61, 37, 100], [37, 61, 118, 100], [118, 61, 251, 100], [251, 61, 489, 100], [0, 100, 7, 144], [7, 100, 37, 144], [37, 100, 118, 144], [118, 100, 251, 144], [251, 100, 489, 144], [0, 144, 7, 153], [7, 144, 37, 153], [37, 144, 118, 153], [118, 144, 251, 153], [251, 144, 489, 153], [0, 153, 7, 181], [7, 153, 37, 181], [37, 153, 118, 181], [118, 153, 251, 181], [251, 153, 489, 181], [0, 181, 7, 239], [7, 181, 37, 239], [37, 181, 118, 239], [118, 181, 251, 239], [251, 181, 489, 239], [0, 239, 7, 280], [7, 239, 37, 280], [37, 239, 118, 280], [118, 239, 251, 280], [251, 239, 489, 280], [0, 280, 7, 289], [7, 280, 37, 289], [37, 280, 118, 289], [118, 280, 251, 289], [251, 280, 489, 289], [0, 289, 7, 506], [7, 289, 37, 506], [37, 289, 118, 506], [118, 289, 251, 506], [251, 289, 489, 506]], 
                                         table_id=1, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image2_0.png", 
                                         page=1
                                         )
                          )
        self.app.add_task(task_info=dict(
                                         hasZoom=True,
                                         zoom=[100, 0, 200, 168], 
                                         coords=[[0, 0, 7, 9], [7, 0, 37, 9], [37, 0, 118, 9], [118, 0, 251, 9], [251, 0, 489, 9], [0, 9, 7, 53], [7, 9, 37, 53], [37, 9, 118, 53], [118, 9, 251, 53], [251, 9, 489, 53], [0, 53, 7, 61], [7, 53, 37, 61], [37, 53, 118, 61], [118, 53, 251, 61], [251, 53, 489, 61], [0, 61, 7, 100], [7, 61, 37, 100], [37, 61, 118, 100], [118, 61, 251, 100], [251, 61, 489, 100], [0, 100, 7, 144], [7, 100, 37, 144], [37, 100, 118, 144], [118, 100, 251, 144], [251, 100, 489, 144], [0, 144, 7, 153], [7, 144, 37, 153], [37, 144, 118, 153], [118, 144, 251, 153], [251, 144, 489, 153], [0, 153, 7, 181], [7, 153, 37, 181], [37, 153, 118, 181], [118, 153, 251, 181], [251, 153, 489, 181], [0, 181, 7, 239], [7, 181, 37, 239], [37, 181, 118, 239], [118, 181, 251, 239], [251, 181, 489, 239], [0, 239, 7, 280], [7, 239, 37, 280], [37, 239, 118, 280], [118, 239, 251, 280], [251, 239, 489, 280], [0, 280, 7, 289], [7, 280, 37, 289], [37, 280, 118, 289], [118, 280, 251, 289], [251, 280, 489, 289], [0, 289, 7, 506], [7, 289, 37, 506], [37, 289, 118, 506], [118, 289, 251, 506], [251, 289, 489, 506]], 
                                         table_id=1, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image2_0.png", 
                                         page=1
                                         )
                          )
        self.app.add_task(task_info=dict(
                                         hasZoom=True,
                                         zoom=[200, 0, 489, 168], 
                                         coords=[[0, 0, 7, 9], [7, 0, 37, 9], [37, 0, 118, 9], [118, 0, 251, 9], [251, 0, 489, 9], [0, 9, 7, 53], [7, 9, 37, 53], [37, 9, 118, 53], [118, 9, 251, 53], [251, 9, 489, 53], [0, 53, 7, 61], [7, 53, 37, 61], [37, 53, 118, 61], [118, 53, 251, 61], [251, 53, 489, 61], [0, 61, 7, 100], [7, 61, 37, 100], [37, 61, 118, 100], [118, 61, 251, 100], [251, 61, 489, 100], [0, 100, 7, 144], [7, 100, 37, 144], [37, 100, 118, 144], [118, 100, 251, 144], [251, 100, 489, 144], [0, 144, 7, 153], [7, 144, 37, 153], [37, 144, 118, 153], [118, 144, 251, 153], [251, 144, 489, 153], [0, 153, 7, 181], [7, 153, 37, 181], [37, 153, 118, 181], [118, 153, 251, 181], [251, 153, 489, 181], [0, 181, 7, 239], [7, 181, 37, 239], [37, 181, 118, 239], [118, 181, 251, 239], [251, 181, 489, 239], [0, 239, 7, 280], [7, 239, 37, 280], [37, 239, 118, 280], [118, 239, 251, 280], [251, 239, 489, 280], [0, 280, 7, 289], [7, 280, 37, 289], [37, 280, 118, 289], [118, 280, 251, 289], [251, 280, 489, 289], [0, 289, 7, 506], [7, 289, 37, 506], [37, 289, 118, 506], [118, 289, 251, 506], [251, 289, 489, 506]], 
                                         table_id=1, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image2_0.png", 
                                         page=1
                                         )
                          )
        
        tasks = pbclient.get_tasks(app_id=self.app.app_id)
        
        self.task1 = TTTask3(tasks[0].id, app_short_name=self.app.short_name)
        
        self.task2 = TTTask3(tasks[1].id, app_short_name=self.app.short_name)
        self.task3 = TTTask3(tasks[2].id, app_short_name=self.app.short_name)
        self.task4 = TTTask3(tasks[3].id, app_short_name=self.app.short_name)
        
        self.base_url = app_flask.config['PYBOSSA_URL']
        self.fb_user = authenticate_fb_user(self.base_url)
        
        
    def tearDown(self):
        next_app = None 
        next_app_list = pbclient.find_app(short_name=self.app.short_name[:-1] + "4")
        
        if len(next_app_list) > 0:
            next_app = next_app_list[0]
        
            next_task = None
            tasks = pbclient.get_tasks(next_app.id)
            for t in tasks:
                if t.info["img_url"] == self.task1.task.info["img_url"]: 
                    pbclient.delete_task(task_id=t.id)
         
            pbclient.delete_app(app_id=next_app.id)
         
        pbclient.delete_task(self.task1.task.id)
        pbclient.delete_task(self.task2.task.id)

        pbclient.delete_app(self.app.app_id)
        
        delete_book(self.task1.get_book_id())
    
    # testing functions

    def test_init_01(self):
        try:
            t1 = TTTask3( -1, "sh_tt3")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
          
    def test_init_02(self):
        try:
            t1 = TTTask3( self.app.app_id, "sh_t")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)
       
    def test_get_next_app_01(self):
        try:
            nx_app = self.task1.get_next_app()
            self.assertEquals(nx_app.short_name, self.app.short_name[:-1] + "4")
        except Exception as ex:
            print ex
            assert False
          
    def test_check_answer_01(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
                  
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                    
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                    
            time.sleep(2)
                   
            self.assertTrue(self.task1.check_answer())
                    
            trs = self.task1.get_task_runs()
        
            self.assertEquals(trs[0].info, '{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            self.assertEquals(trs[1].info, '{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
                  
            self.assertTrue(self.task1.check_answer())
            self.assertEquals(self.task1.task.state, '0')
                  
            self.task1.close_task()
                  
            self.assertEquals(self.task1.task.state, 'completed')
                  
        except Exception as e:
            print e
            assert False
            
      
    def test_check_answer_02(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
                  
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                    
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                    
            time.sleep(2)
                   
            self.assertFalse(self.task1.check_answer())
                  
        except Exception as e:
            print e
            assert False
  
      
    def test_check_answer_03(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
                  
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                    
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                    
            time.sleep(2)
                   
            self.task1.check_answer()
              
        except Meb_exception_tt3 as e:
            self.assertEquals(e.code, 2)
      
      
    def test_check_answer_04(self):
        """
          Detecting the fault of a field in info
        """
          
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image1_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image1_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
                  
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                    
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                    
            time.sleep(2)
                   
            self.task1.check_answer()
              
        except Meb_exception_tt3 as e:
            self.assertEquals(e.code, 2)
    
    
    def test_add_next_task_01(self):
        """
          Detection of invalid task group
        """
        
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
         
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                 
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                 
            time.sleep(2)
                 
            self.assertTrue(self.task1.check_answer())
                
            self.assertFalse(self.task1.add_next_task())
                 
        except Exception as e:
            print e
            assert False
    
    
    def test_add_next_task_02(self):
        """
          Valid task group
        """
        
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task2.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task2.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
         
            task_run3 = dict(app_id=self.app.app_id, task_id=self.task3.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run4 = dict(app_id=self.app.app_id, task_id=self.task3.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            
            task_run5 = dict(app_id=self.app.app_id, task_id=self.task4.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            task_run6 = dict(app_id=self.app.app_id, task_id=self.task4.task.id, info='{\"img_url\":\"https://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image0_0.png\",\"linhas\":[[0,0,507,0],[0,54,507,54],[0,103,507,103],[0,178,507,178]],\"colunas\":[[0,0,0,178],[239,0,239,178],[507,0,507,178]],\"maxX\":507,\"maxY\":178}')
            
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
            submit_answer(self.base_url, task_run3)
            submit_answer(self.base_url, task_run5)
                 
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            task_run4['facebook_user_id'] = '12345'
            task_run6['facebook_user_id'] = '12345'
            
            submit_answer(self.base_url, task_run2)
            submit_answer(self.base_url, task_run4)
            submit_answer(self.base_url, task_run6)
                 
            time.sleep(2)
            
            self.assertTrue(self.task2.check_answer())
            self.assertTrue(self.task3.check_answer())
            self.assertTrue(self.task4.check_answer())
            
            self.task2.close_task()
            self.task3.close_task()
            self.task4.close_task()
            
            self.task4.add_next_task()
            
        except Meb_exception_tt3 as e:
            self.assertEquals(e.code, 5)  # didnt found images to run tesseract executor

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(tt3_task_with_zoom_test)
    return suite

if __name__ == '__main__':
    unittest.main()

