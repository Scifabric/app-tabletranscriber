# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask4
from app_tt.pb_apps.tt_apps.ttapps import Apptt_transcribe

from app_tt.core import pbclient, app as app_flask
import unittest
import requests
import json
import time

from tests.app_tt.base import delete_book, authenticate_fb_user, submit_answer
from app_tt.data_mngr import data_manager as data_mngr 

from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception, Meb_exception_tt4

class tt4_task_test(unittest.TestCase):
    
    def setUp(self):
        book_title = "rpparaiba1918_title"
        self.app = Apptt_transcribe(short_name="rpparaiba1918_tt4", title=book_title)
        
        self.app.add_task(task_info=dict(confidences=[43, 57, 95, 54], 
                                         maxX=483, 
                                         maxY=399, 
                                         cells=[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]], 
                                         values=[".. 1\u00ed\u00c9\u00c9s.:n::l-A-l\u00ed\u00c9:\u00ed-", 
                                                  ". IX/I\u00daJSTICI-FI\u00d4S", "", "\u00c0 numzno u\u00a1\\ ELEITIJRES"], 
                                         table_id=0, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image85_0.png",
                                         page=85))
        
        self.app.add_task(task_info=dict(confidences=[43, 57, 95, 54], 
                                         maxX=483, 
                                         maxY=399, 
                                         cells=[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]], 
                                         values=[".. 1\u00ed\u00c9\u00c9s.:n::l-A-l\u00ed\u00c9:\u00ed-", 
                                                  ". IX/I\u00daJSTICI-FI\u00d4S", "", "\u00c0 numzno u\u00a1\\ ELEITIJRES"], 
                                         table_id=0, 
                                         img_url="http://localhost/mb-static/books/rpparaiba1918/metadados/tabelasBaixa/image85_0.png",
                                         page=85))
        
        tasks = pbclient.get_tasks(app_id=self.app.app_id)
        
        self.task1 = TTTask4(tasks[0].id, app_short_name=self.app.short_name)
        self.task2 = TTTask4(tasks[1].id, app_short_name=self.app.short_name)
        
        self.base_url = app_flask.config['PYBOSSA_URL']
        self.fb_user = authenticate_fb_user(self.base_url)
        
        
    def tearDown(self):
       #next_app = None 
       #next_app_list = pbclient.find_app(short_name=self.app.short_name[:-1] + "3")
       
       #if len(next_app_list) > 0:
       #    next_app = next_app_list[0]
       # 
       #     next_task = None
       #     tasks = pbclient.get_tasks(next_app.id)
       #     for t in tasks:
       #         if t.info["page"] == self.task1.task.info["page"]: 
       #             pbclient.delete_task(task_id=t.id)
       #  
       #     pbclient.delete_app(app_id=next_app.id)
         
        pbclient.delete_task(self.task1.task.id)
        pbclient.delete_task(self.task2.task.id)

        pbclient.delete_app(self.app.app_id)
         
        delete_book(self.task1.get_book_id())
    
    # testing functions

    def test_init_01(self):
        try:
            t1 = TTTask4( -1, "sh_tt4")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
        
    def test_init_02(self):
        try:
            t1 = TTTask4( self.app.app_id, "sh_t")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)
     
    def test_get_next_app_01(self):
        try:
            nx_app = self.task1.get_next_app()
            self.assertEquals(nx_app, None)
        except Exception as ex:
            print ex
            assert False
        
    def test_check_answer_01(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[2,2,2,2]}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[2,2,2,2]}')
                
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
                  
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
                  
            time.sleep(2)
                 
            self.assertTrue(self.task1.check_answer())
                  
            trs = self.task1.get_task_runs()
      
            self.assertEquals(trs[0].info, '{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[2,2,2,2]}')
            self.assertEquals(trs[1].info, '{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[2,2,2,2]}')
                
            self.assertTrue(self.task1.check_answer())
            self.assertEquals(self.task1.task.state, '0')
                
            self.task1.close_task()
                
            self.assertEquals(self.task1.task.state, 'completed')
                
        except Exception as e:
            print e
            assert False
          
    
    def test_check_answer_02(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[1,1,1,1]}')
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info='{\"cells\":[[0, 0, 34, 60], [34, 0, 227, 60], [227, 0, 300, 60], [300, 0, 374, 60]],\"computer_values\":[\"PARA\u00cdBA ( ESTADO )\",\"PRES IDENTE\",\"( FRANC|SCO CAM!\",\"\u00a1LLO DE HOLLANDA )\"],\"human_values\":[\"PARAIBA ( ESTADO )\",\"PRESIDENTE\",\"( FRANCISCO CAMILLO DE HOLLANDA )\",\"MENSAGEM 19 DE SETEMBRO DE 1918.\"],\"confidences\":[83,88,83,81],\"num_of_confirmations\":[2,2,2,1]}')
                
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
            

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(tt4_task_test)
    return suite
            
if __name__ == '__main__':
    unittest.main()

