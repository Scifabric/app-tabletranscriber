import os
from app_tt.core import app as application
from unittest import TestCase
from app_tt.core import pbclient
import unittest
import app_tt.engine.tasks as engine 
from app_tt.meb_util import archiveBookData 

class test_application(TestCase):


    def setUp(self):
        app = application
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.new_ttapplications("10304diinaavanas033859mbp")
    
    def tearDown(self):
        self.del_ttapplications("10304diinaavanas033859mbp")


    def new_ttapplications(self, short_name):
        print self.app.application
        o = self.app.get("mb/api/%s/init" % short_name)
        print "o: " + str(o)
        return o
    

    def del_ttapplications(self, short_name):
        for i in range(1,5):
            tt_app = pbclient.find_app(short_name="%s_tt%d" % (short_name, i))[0]
            pbclient.delete_app(tt_app.id)


    def bookdata(self, book_id):
        return engine.archiveBookData(book_id)


    def test_home(self):
        rv = self.app.get('/')
        assert "<h1>Table Transcriber</h1>" in rv.data, rv


    def test_colabore(self):
        
        tt_apps = pbclient.get_apps()
        
        if len(tt_apps) > 0:
            tt_app = tt_apps[0]
            coll_request = self.app.get('/collaborate', follow_redirects=True)

            book_data = self.bookdata(tt_app.short_name[:-4])
            
            self.assertTrue(book_data["title"] in coll_request.data.decode("utf-8"),
                    "Error book title was not found in collaborate page")

            self.assertTrue(book_data["volume"] in coll_request.data.decode("utf-8"),
                    "Error book volume was not found in collaborate page")

            self.assertTrue(book_data["publisher"] in coll_request.data.decode("utf-8"),
                    "Error book publisher was not found in collaborate page")

            self.assertTrue(book_data["contributor"] in coll_request.data.decode("utf-8"),
                    "Error book contributor was not found in collaborate page" )

        else:
            raise AssertionError("Application was not created")


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_application)
    return suite


if __name__ == "__main__":
    unittest.main()
