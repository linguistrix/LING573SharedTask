# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# DocumentRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from CreateIndex import *
from NewsDocument import Document
from bs4 import BeautifulSoup
from whoosh import index
from whoosh import highlight
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.qparser import QueryParser
from whoosh.searching import Hit
import os, os.path, sys, time


class DocumentRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "DocumentRetrievalTaskExecutor")

    def Execute(self, session):
        query = session.questionProcessor.GetDocumentRetrievalQuery()
        session.logs.append("Query: {0}".format(query))
        
        session.query, session.relevantDocuments = self.__queryIndex(
            session.indexPath,
            query, 
            N=session.maxNumberOfReturnedDocuments)
        
        for relevantDoc in session.relevantDocuments:
            session.logs.append("{0} - {1}".format(relevantDoc[0], relevantDoc[1]))
        
        self.LogTaskCompletion(session)
        return True

    def __getIndex(self, folderpath):
        if os.path.exists(folderpath):
            ix = index.open_dir(folderpath)
        else:
            ix = None
        return ix

    def __queryIndex(self, indexpath, query_term, N=20):
        relevantDocuments = []
        
        ix = self.__getIndex(indexpath)
        
        with ix.searcher() as searcher:
            qp = QueryParser('body', schema=ix.schema)
            q = qp.parse(query_term)
            results = searcher.search(q, limit=N, terms=True)
            
            for result in results:
                relevantDocuments.append((result['docno'], result['headline']))

        return q, results#relevantDocuments 

