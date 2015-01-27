from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.app_tt.base import delete_app, create_tt_apps, authenticate_fb_user, delete_book, delete_workflow_transactions, get_book, get_page, get_page_table, get_metadata, get_cell, get_workflow_transaction
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
        
        # create/authenticate a fb user
        self.base_url = application.config['PYBOSSA_URL']
        self.fb_user = authenticate_fb_user(self.base_url)
        
        #delete_workflow_transactions(self.book_id)
        #delete_app(self.book_id)
        #delete_book(self.book_id)
        
    def tearDown(self):
        delete_workflow_transactions(self.book_id)
        delete_app(self.book_id)
        delete_book(self.book_id)
        #pass

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
        create_t4_task(self, self.book_id, task_t3[0], 1)
    
    
    def test_04_t4_close(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        
        task_t2 = create_t2_task(self, self.book_id, task_t1)
        task_t3 = create_t3_task(self, self.book_id, task_t2)
        task_t4 = create_t4_task(self, self.book_id, task_t3[0], 1)
        close_t4_task(self, self.book_id, task_t4[0])
    

    def test_05_mbdb_loading(self):
        # Creating new tt applications
        create_tt_apps(self.app, self.book_id)
        app_t1 = pbclient.find_app(short_name=self.book_id + "_tt1")
        self.assertTrue(len(app_t1) > 0, "Error tt_app was not created")
        
        # check if the book was created
        self.assertTrue(get_book(self.book_id))
        
        # check if the workflow transaction (T1) was created
        task_t1 = pbclient.get_tasks(app_t1[0].id, sys.maxint)[0]
        self.assertTrue(len(get_workflow_transaction()) == 74)
        
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=None, task_id_3=None, task_id_4=None)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        
        task_t2 = create_t2_task(self, self.book_id, task_t1)
        
        # check if the workflow transaction (T2) was created
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=task_t2.id, task_id_3=None, task_id_4=None)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        
        # check if the page was created
        page = get_page(self.book_id, task_t2.info['page'])
        self.assertTrue(page)
        
        tasks_t3 = create_t3_task(self, self.book_id, task_t2)
        
        # check if the workflow transactions (T3) were created
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=task_t2.id, task_id_3=tasks_t3[0].id, task_id_4=None)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=task_t2.id, task_id_3=tasks_t3[1].id, task_id_4=None)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        
        # check if the page tables were created
        page_tables = get_page_table(self.book_id, page.id)
        self.assertTrue(len(page_tables) == 2)
        
        # check if the metadata was created
        self.assertTrue(get_metadata(page_tables[0].id))
        self.assertTrue(get_metadata(page_tables[1].id))
        
        tasks_t4 = create_t4_task(self, self.book_id, tasks_t3[0], 1)
        close_t4_task(self, self.book_id, tasks_t4[0])
        
        # check if the workflow transactions (T4) were created
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=task_t2.id, task_id_3=tasks_t3[0].id, task_id_4=tasks_t4[0].id)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        
        tasks_t4 = create_t4_task(self, self.book_id, tasks_t3[1], 2)
        close_t4_task(self, self.book_id, tasks_t4[1])
        
        # check if the workflow transactions (T4) were created
        workflow_transaction_info = dict(task_id_1=task_t1.id, task_id_2=task_t2.id, task_id_3=tasks_t3[1].id, task_id_4=tasks_t4[1].id)
        self.assertTrue(get_workflow_transaction(workflow_transaction_info))
        
        # check if the cells were created
        self.assertTrue(len(get_cell(page_tables[0].id)) == 6)
        self.assertTrue(len(get_cell(page_tables[1].id)) == 6)
        
        
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_workflow)
    return suite

