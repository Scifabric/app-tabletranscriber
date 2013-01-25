import os
import application
from unittest import TestCase
import unittest
import app_tt.engine.tasks as engine 

class test_application(TestCase):


    def setUp(self):
        app = application.app
        app.config['TESTING'] = True
        self.app = app.test_client()

    def new_ttapplications(self, short_name):
        return self.app.get("/api/%s/init" % short_name)


    def bookdata(self, book_id):
        return engine._archiveBookData(book_id)



    def test_home(self):
        rv = self.app.get('/')
        assert "<h1>Table Transcriber</h1>" in rv.data, rv

    def test_colabore(self):
        # Creating tt applications
        init = self.new_ttapplications("discursopro1936bras")
        if init:
            rv = self.app.get('/collaborate', follow_redirects=True)
            book_data = self.bookdata("discursopro1936bras")
            
            assert book_data["title"] in rv.data.decode("utf-8") , rv
            assert book_data["volume"] in rv.data.decode("utf-8") , rv
            assert book_data["publisher"] in rv.data.decode("utf-8") , rv
            assert book_data["contributor"] in rv.data.decode("utf-8") , rv

        else:
            raise AssertionError("Applications shall be created")



def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_application)
    return suite


if __name__ == "__main__":
    unittest.main()
