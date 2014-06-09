
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
          test in search in general_info field with a big set of docs
        """
        
        for i in range(0, 200):
            finalDate = "%d/%d/1900" % (i, i)
            doc_dict = {
                         "doc_id" : i,
                         "general_info" : "title subtitle",
                         "subject" : "subject",
                         "source" : "source",
                         "initial_date" : "1800",
                         "final_date" : finalDate,
                         "content" : "content1"
                         }
            
            self.pylucene.index_doc(doc_dict)
        
        docs = self.pylucene.search_docs(value="title", field="general_info")
        
        self.assertEquals(200, len(docs)) 
        
        for i in range(len(docs)):
            self.assertEquals(docs[i].get("general_info"), "title subtitle")
            self.assertEquals(docs[i].get("subject"), "subject")
            self.assertEquals(docs[i].get("source"), "source")
            self.assertEquals(docs[i].get("initial_date"), "1800")
            
            # no guaranteed order
            #self.assertEquals(docs[i].get("final_date"), "%d/%d/1900" % (i,i))
            
            self.assertEquals(docs[i].get("content"), None)
    
    
def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(pylucene_test)
    return suite


if __name__ == '__main__':
    unittest.main()
        