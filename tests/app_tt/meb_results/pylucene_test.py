
from app_tt.meb_results.pylucene import PyLucene

import unittest

import os, shutil

FLAG_TO_CONTROL_JVM = 0

def set_FLAG_TO_CONTROL_JVM():
    global FLAG_TO_CONTROL_JVM
    FLAG_TO_CONTROL_JVM = 1

class pylucene_test(unittest.TestCase):
    
    def setUp(self):
        if FLAG_TO_CONTROL_JVM == 0:
            self.pylucene = PyLucene(startJVM=True)
            set_FLAG_TO_CONTROL_JVM()
        else:
            self.pylucene = PyLucene(startJVM=False)
    
    def tearDown(self):
        shutil.rmtree(self.pylucene.STORE_DIR)
    
    # testing functions
    
    def test_pylucene_01(self):
        """
          test in search in general_info field
        """
        
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject",
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs(value="title", field="general_info")
        
        self.assertEquals(3, docs.totalHits)
    
    
    
    def test_pylucene_02(self):
        """
          test match with field tokenized and in general search field
        """
        
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject",
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs("title")
        
        self.assertEquals(3, docs.totalHits)
    
    
    def test_pylucene_03(self):
        """
          test perfect match with a specific field
        """
        
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject%d" % (i),
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs(value="subject1", field="subject")
        
        self.assertEquals(1, docs.totalHits)
    
    
    def test_pylucene_04(self):
        """
          test search for date fields (year/month/day)
        """
        
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject%d" % (i),
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs(value="1900", field="final_date")
        
        self.assertEquals(3, docs.totalHits)
    
    
    def test_pylucene_05(self):
        """
          test search for number
        """
        
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject%d" % (i),
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs(value="19", field="final_date")
        
        self.assertEquals(0, docs.totalHits)
    
    
    def test_pylucene_06(self):
        """
          test search in content field
        """
         
        for i in range(0, 3):
            doc_dict = {
                         "general_info" : "title subtitle",
                         "subject" : "subject%d" % (i),
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : "%d/%d/1900" % (i, i),
                         "content" : "content1"
                         }
             
            self.pylucene.index_doc(doc_dict)
         
        docs = self.pylucene.search_docs(value="1900", field="content")
         
        self.assertEquals(3, docs.totalHits)
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(pylucene_test)
    return suite


if __name__ == '__main__':
    unittest.main()
        