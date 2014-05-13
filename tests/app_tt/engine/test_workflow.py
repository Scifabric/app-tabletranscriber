from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.app_tt.base import delete_app, create_tt_apps, authenticate_fb_user, submit_answer, delete_book
import unittest
import sys
import json
import time

class test_workflow(TestCase):
    
    def setUp(self):
        self.app = application.test_client()
        pybossa_api = self.app.get("/api")
        
        if pybossa_api.data.find('404') != -1:
            raise AssertionError("Pybossa's not working")
        
        self.book_id = "rpparaiba1918"
        
        delete_app(self.book_id)
        delete_book(self.book_id)
        
        # create/authenticate a fb user
        self.base_url = application.config['PYBOSSA_URL']
        self.fb_user = authenticate_fb_user(self.base_url)

    def create_t2_task(self, book_id, app_t1, task_t1):
        # creating an answer for the T1 app
        task_run = dict(app_id=task_t1.app_id, task_id=task_t1.id, info="Yes")
        print(json.dumps(task_run));

        # Anonymous submission
        submit_answer(self.base_url, task_run)
        
        # FB authenticated user submission
        task_run['facebook_user_id'] = '12345'
        submit_answer(self.base_url, task_run)
        
        # Signalling the T1 task completion
        self.app.get("/api/" + str(task_t1.id) + "/done")
        time.sleep(2)
        
        # check if T1 task is closed
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        self.assertTrue(task_t1.state == "completed")
        
        # one task from T2 app should exist
        app_t2 = pbclient.find_app(short_name=book_id + "_tt2")
        self.assertTrue(len(app_t2) > 0, "Error tt_app was not created")
        
        t2_tasks = pbclient.get_tasks(app_t2[0].id, sys.maxint)
        self.assertTrue(len(t2_tasks) == 1)
        
        return t2_tasks[0]
        

    def test_01_t2_creation(self):
        # Creating new tt applications
        book_id = "rpparaiba1918"
        create_tt_apps(self.app, book_id)
        app_t1 = pbclient.find_app(short_name=book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        self.create_t2_task(book_id, app_t1, task_t1)

        
    def test_01_t3_creation(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        task_t2 = self.create_t2_task(self.book_id, app_t1, task_t1)
        print(task_t2.info)
        

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_workflow)
    return suite

