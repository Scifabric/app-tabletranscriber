from unittest import TestCase
from app_tt.application import app as application
from app_tt.core import pbclient
from tests.app_tt.base import delete_app, create_tt_apps
import unittest
import sys

class test_api(TestCase):
    def setUp(self):
        self.app = application.test_client()
        pybossa_api = self.app.get("/api")
        
        if pybossa_api.data.find('404') != -1:
            raise AssertionError("Pybossa's not working")
        
        delete_app("custodevida1946bras")
        
        
    def test_00_init(self):
        # Creating new tt applications
        create_tt_apps(self.app, "custodevida1946bras")
        pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
        self.assertTrue(len(pb_app) > 0, "Error tt_app was not created")
        

    def test_02_init(self):
        # Creating new tt applications
        create_tt_apps(self.app, "custodevida1946bras")
        pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
        
        # application is already created
        n_app_tasks = len(pbclient.get_tasks(pb_app[0].id, sys.maxint))
        rv = self.app.get("/api/custodevida1946bras/init")

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


    def test_check_app_done(self):
        return True

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_api)
    return suite
