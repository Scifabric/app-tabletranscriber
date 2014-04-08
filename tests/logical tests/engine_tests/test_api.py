from unittest import TestCase
import sys
import unittest
from app_tt.core import app as application
from app_tt.core import pbclient
import app_tt.engine.api as api
import requests
import json


class test_api(TestCase):
    def setUp(self):
        app = application
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rtester:rtester@localhost/pybossa_test'
        
        self.app = application.test_client()
        
        print type(self.app)
        
        try:
            pybossa_api = requests.get(app.config['PYBOSSA_URL'] + "/api")
        except:
            raise AssertionError("Pybossa's not working")
        if not pybossa_api.content:
            raise AssertionError("Pybossa's api is not working")

    def test_00_init(self):
        # Creating new tt applications
        pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
        if len(pb_app) == 0:
            a = self.app.get("/mb/api/custodevida1946bras/init", follow_redirects=True)
            print "app.config: " + str(self.app.name())
            print "a: " + str(a)
            pb_app = pbclient.find_app(short_name="custodevida1946bras_tt1")
            
            self.assertTrue(len(pb_app) > 0, "Error tt_app was not created")
        
        else:   # application is already created
            n_app_tasks = len(pbclient.get_tasks(pb_app[0].id, sys.maxint))
            rv = self.app.get("mb/api/custodevida1946bras/init")

            self.assertTrue(rv.data, "Error tt_app was not created")
            
            # if application is already created init cant duplicate the tasks
            self.assertEqual(n_app_tasks,
                    len(pbclient.get_tasks(pb_app[0].id, sys.maxint)),
                    "Error duplicated tasks")


    def test_01_init(self):
        # Creating tt_app where book_id does not exist

        inexistent_id = "XX_does_not_exist_XX"
        init_req = self.app.get("mb/api/%s/init" % inexistent_id)

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
