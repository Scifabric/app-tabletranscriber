from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.app_tt.base import delete_app, create_tt_apps, create_and_close_t1
import unittest
import sys
import time

class test_api(TestCase):
    def setUp(self):
        self.app = application.test_client()
        pybossa_api = self.app.get("/api")
        
        if pybossa_api.data.find('404') != -1:
            raise AssertionError("Pybossa's not working")
        
        delete_app("rpparaiba1918")
        
        
    def test_01_init(self):
        # Creating new tt applications
        create_tt_apps(self.app, "rpparaiba1918")
        pb_app = pbclient.find_app(short_name="rpparaiba1918_tt1")
        self.assertTrue(len(pb_app) > 0, "Error tt_app was not created")
        

    def test_02_init(self):
        # Creating new tt applications
        create_tt_apps(self.app, "rpparaiba1918")
        pb_app = pbclient.find_app(short_name="rpparaiba1918_tt1")
        
        # application is already created
        n_app_tasks = len(pbclient.get_tasks(pb_app[0].id, sys.maxint))
        rv = self.app.get("/api/rpparaiba1918/init")

        self.assertTrue(rv.data, "Error tt_app was not created")
            
        # if application is already created init cant duplicate the tasks
        self.assertEqual(n_app_tasks,
                    len(pbclient.get_tasks(pb_app[0].id, sys.maxint)),
                    "Error duplicated tasks")
        

    def test_03_init(self):
        # Creating tt_app where book_id does not exist
        inexistent_id = "XX_does_not_exist_XX"
        init_req = create_tt_apps(self.app, inexistent_id)

        self.assertEqual(init_req.data, "False",
                "Error application can not be created")
        
        search_list = pbclient.find_app(short_name=inexistent_id + "_tt1")

        self.assertTrue(len(search_list) == 0,
                "Error application with inexistent id was found")
        
    def test_04_init_and_close(self):
        # Creating new tt applications
        create_and_close_t1(self.app, "rpparaiba1918")
        time.sleep(15)
        pb_app = pbclient.find_app(short_name="rpparaiba1918_tt1")
        tasks_t1 = pbclient.get_tasks(pb_app[0].id, sys.maxint)
        
        for task in tasks_t1:
            self.assertTrue(task.state == "completed")
        
        pb_app = pbclient.find_app(short_name="rpparaiba1918_tt2")
        tasks_t2 = pbclient.get_tasks(pb_app[0].id, sys.maxint)
        self.assertTrue(len(tasks_t1) == len(tasks_t2))
    
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_api)
    return suite

