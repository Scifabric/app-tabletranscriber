
import os, lucene, threading, sys, time

from java.io import File, StringReader
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader 
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write(' ... ')
            sys.stdout.flush()
            time.sleep(1.0)

class PyLucene:
    """
        PyLucene module api
    """
    
    def __init__(self, startJVM=False):
        if startJVM:
            lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        
        self.STORE_DIR = "index_dir"
        self.store = SimpleFSDirectory(File(self.STORE_DIR)) 
        
        tmp_analyzer = StandardAnalyzer(Version.LUCENE_CURRENT) 
        self.analyzer = LimitTokenCountAnalyzer(tmp_analyzer, 10000) 
        
        config = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.writer = IndexWriter(self.store, config)
    
    def close_store(self):
        self.store.close()

    def index_doc(self, doc_dict):
        """
          Index a doc to pylucene
          
          obs.: docid is a string not an integer
        """
        
        doc = Document()
        
        doc.add(Field("doc_id", doc_dict["doc_id"], TextField.TYPE_STORED))
        doc.add(Field("general_info", doc_dict["general_info"], TextField.TYPE_NOT_STORED))
        doc.add(Field("subject", doc_dict["subject"], TextField.TYPE_NOT_STORED))
        doc.add(Field("source", doc_dict["source"], TextField.TYPE_NOT_STORED))
        doc.add(Field("initial_date", doc_dict["initial_date"], TextField.TYPE_NOT_STORED))
        doc.add(Field("final_date", doc_dict["final_date"], TextField.TYPE_NOT_STORED))
        
        body_text = doc_dict["content"]
        body_reader = StringReader(body_text)
        doc.add(Field("content", body_reader))
        
        self.writer.addDocument(doc)
        
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        
        self.writer.commit()
        
        ticker.tick = False
        print 'done'
        
    def search_docs(self, value, field="general_info"):
        MAX_RESULTS = 1000
        searcher = IndexSearcher(DirectoryReader.open(self.store))
        query = QueryParser(Version.LUCENE_CURRENT, field,
                            self.analyzer).parse(value)
        topDocs = searcher.search(query, MAX_RESULTS)
        
        return [searcher.doc(hit.doc) for hit in topDocs.scoreDocs]
        
    
    #def get_doc(self, hit_doc):
    #    searcher = IndexSearcher(DirectoryReader.open(self.store))
    #    doc = searcher.doc(hit_doc)
    #    return doc
    
    
    
    