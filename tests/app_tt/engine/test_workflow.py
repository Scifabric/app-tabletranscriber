from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.app_tt.base import delete_app, create_tt_apps, authenticate_fb_user, delete_book
from tests.app_tt.workflow_util_test import create_t2_task, create_t3_task, create_t4_task, close_t4_task
import unittest
import sys

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


    def test_01_t2_creation(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        create_t2_task(self, self.book_id, task_t1)

        
    def test_02_t3_creation(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        task_t2 = create_t2_task(self, self.book_id, task_t1)
        create_t3_task(self, self.book_id, task_t2)
        
        
    def test_03_t4_creation(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        task_t2 = create_t2_task(self, self.book_id, task_t1)
        task_t3 = create_t3_task(self, self.book_id, task_t2)
        create_t4_task(self, self.book_id, task_t3)
    
    
    def test_04_t4_close(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        task_t2 = create_t2_task(self, self.book_id, task_t1)
        task_t3 = create_t3_task(self, self.book_id, task_t2)
        task_t4 = create_t4_task(self, self.book_id, task_t3)
        close_t4_task(self, self.book_id, task_t4)
        

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_workflow)
    return suite

