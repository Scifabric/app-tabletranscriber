# -*- coding: utf-8 -*-
from app_tt.pb_apps.tt_apps.tt_tasks import TTTask1
from app_tt.pb_apps.tt_apps.ttapps import Apptt_select

from app_tt.core import pbclient, app as app_flask
import unittest
import requests
import json
import time

from tests.app_tt.base import delete_book, authenticate_fb_user, submit_answer
import app_tt.data_mngr.data_manager as data_mngr 

from app_tt.meb_exceptions.meb_exception import Meb_pb_task_exception, Meb_exception_tt1, Meb_exception

class TT_Task1_TestCase(unittest.TestCase):
    
    def setUp(self):
        bookinfo = dict(
                        bookid="sh", 
                        title="title1",
                        contributor="cont1", 
                        publisher="pub1",
                        volume="1",
                        img="http://archive.org/download/livro1/n1"
                        )
        
        self.app = Apptt_select(short_name="sh_tt1", title="title1", book_info=bookinfo)
        self.app.add_task(task_info=dict(url_m="http://archive.org/download/livro1/n1", url_b="http://archive.org/download/livro1/n1",page=1))
        self.app.add_task(task_info=dict(url_m="http://archive.org/download/livro1/n2", url_b="http://archive.org/download/livro1/n2",page=2))
        
        tasks = pbclient.get_tasks(app_id=self.app.app_id)
        
        self.task1 = TTTask1(tasks[0].id, app_short_name=self.app.short_name)
        self.task2 = TTTask1(tasks[1].id, app_short_name=self.app.short_name)
        
        self.base_url = app_flask.config['PYBOSSA_URL']
        self.fb_user = authenticate_fb_user(self.base_url)
        
    def tearDown(self):
        next_app = None 
        next_app_list = pbclient.find_app(short_name=self.app.short_name[:-1] + "2")
        
        if len(next_app_list) > 0:
            next_app = next_app_list[0]
        
            next_task = None
            tasks = pbclient.get_tasks(next_app.id)
            for t in tasks:
                if t.info["page"] == self.task1.task.info["page"]: 
                    pbclient.delete_task(task_id=t.id)
         
            pbclient.delete_app(app_id=next_app.id)
        
        pbclient.delete_task(self.task1.task.id)
        pbclient.delete_task(self.task2.task.id)
        pbclient.delete_app(self.app.app_id)
        
        data_mngr.delete_book(self.task1.get_book_id())
    
    # testing functions

    def test_init_01(self):
        try:
            t1 = TTTask1( -1, "sh_tt1")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 1)
      
    def test_init_02(self):
        try:
            t1 = TTTask1( self.app.app_id, "sh_t")
        except Meb_pb_task_exception as e:
            self.assertEquals(e.code, 2)
    
    def test_init_03(self):
        try:
            book_mb = data_mngr.get_book(self.task1.get_book_id())
            
            self.assertEquals(book_mb.id, "sh")
            self.assertEquals(book_mb.title, "title1")
            self.assertEquals(book_mb.publisher, "pub1")
            self.assertEquals(book_mb.contributor, "cont1")
            self.assertEquals(book_mb.volume, "1")
            self.assertEquals(book_mb.img_url, "http://archive.org/download/livro1/n1")
            
        except Exception as e:
            print e
            assert False
    
    def test_get_next_app_01(self):
        try:
            nx_app = self.task1.get_next_app()
            self.assertEquals(nx_app.short_name, self.app.short_name[:-1] + "2")
        except Exception:
            assert False
     
    def test_check_answer_01(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            trs = self.task1.get_task_runs()
 
            self.assertEquals(trs[0].info, "Yes")
            self.assertEquals(trs[1].info, "Yes")
            self.assertTrue(self.task1.check_answer())
 
        except Exception as e:
            print e
            assert False
     
    def test_check_answer_02(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="No")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            self.assertFalse(self.task1.check_answer())
             
            trs = self.task1.get_task_runs()
             
            self.assertEquals(trs[0].info, "Yes")
            self.assertEquals(trs[1].info, "No")
             
        except Exception as e:
            print e
            assert False
     
    def test_check_answer_03(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="BLA")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="No")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            self.task1.check_answer()
             
        except Meb_exception_tt1 as e:
            self.assertEquals(e.code, 2)
     
    def test_add_next_task_01(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            self.assertTrue(self.task1.check_answer())
            self.assertTrue(self.task1.add_next_task())
             
        except Exception as e:
            print e
            assert False
     
    def test_add_next_task_02(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="No")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            self.assertFalse(self.task1.check_answer())
            self.assertFalse(self.task1.add_next_task())
             
        except Meb_exception_tt1 as e:
            self.assertEquals(e.code, 1)
     
    def test_add_next_task_03(self):
        try:
            task_run1 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
            task_run2 = dict(app_id=self.app.app_id, task_id=self.task1.task.id, info="Yes")
     
            # Anonymous submission
            submit_answer(self.base_url, task_run1)
             
            # FB authenticated user submission
            task_run2['facebook_user_id'] = '12345'
            submit_answer(self.base_url, task_run2)
             
            time.sleep(2)
             
            self.assertTrue(self.task1.check_answer())
            self.assertTrue(self.task1.add_next_task())
             
            self.task1.add_next_task()
             
            assert False
             
        except Meb_exception_tt1 as e:
            self.assertEquals(e.code, 3)
    
if __name__ == '__main__':
    unittest.main()

