# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# DocumentRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from CreateIndex import *
from NewsDocument import Document
from whoosh import index
import os, os.path, sys, time


class DocumentRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "DocumentRetrievalTaskExecutor")

    def Execute(self, session):
            
        session.logs.append("Query: {0}".format(session.query))
        
        results = self.__queryIndex(
            session.index,
            session.query, 
            N=session.maxNumberOfReturnedDocuments)

        session.relevantDocuments = results

        for result in results:
            session.logs.append("{0} - {1}".format(result[0], result[1]))
        
        self.LogTaskCompletion(session)
        return True

    def __getIndex(self, folderpath):
        if os.path.exists(folderpath):
            ix = index.open_dir(folderpath)
        else:
            ix = None
        return ix

    def __queryIndex(self, index, query, N=20):
        relevantDocuments = []
        
        #ix = self.__getIndex(indexpath)
        
        with index.searcher() as searcher:
            results = searcher.search(query, limit=N, terms=True)
            
            for result in results:
                relevantDocuments.append((result['docno'], result['headline']))

        return relevantDocuments

