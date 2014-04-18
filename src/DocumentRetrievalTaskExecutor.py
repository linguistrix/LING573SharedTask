# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# DocumentRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from bs4 import BeautifulSoup
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh.qparser import QueryParser
from whoosh.searching import Hit
import os, os.path, sys, time


class DocumentRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "DocumentRetrievalTaskExecutor")
        self.indexPath = "/home2/abothale/ling573/LING573SharedTask/src/index" 
    
    def Execute(self, session):
        query = session.questionProcessor.GetDocumentRetrievalQuery()
        
        session.relevantDocuments = queryIndex(
            self.indexPath,
            query, 
            N=session.maxNumberOfReturnedDocuments)
        
        for relevantDoc in session.relevantDocuments:
            session.logs.append("{0} - {1}".format(relevantDoc[0], relevantDoc[1]))
        
        self.LogTaskCompletion(session)
        return True


def generateSchema():
    schema = Schema(docno=ID(unique=True, stored=True), headline=TEXT(stored=True), body=TEXT)
    return schema

def generateIndex(schema, folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        ix = index.create_in(folderpath, schema)

    return ix

def getIndex(folderpath):
    if os.path.exists(folderpath):
        ix = index.open_dir(folderpath)
    else:
        ix = None
    return ix

def addFolderToIndex(ix, folderpath):
    count = 0
    for root, _, files in os.walk(folderpath):
        for f in files:
            fullpath = os.path.join(root, f)
            addFileToIndex(ix, fullpath)
            count += 1

    print('Added {0} files to the Index'.format(count))

def addFileToIndex(ix, filepath):
    f = open(filepath)
    html_doc = '<SUPERDOC>' + f.read() + '</SUPERDOC>'
    soup = BeautifulSoup(html_doc, 'xml')

    with ix.writer() as writer:
        for doc in soup.find_all('DOC'):
            doc_no = doc.DOCNO.string.strip()
            headline = doc.HEADLINE.string.strip()
            body = doc.TEXT.get_text().strip()
            writer.add_document(docno=doc_no, headline=headline, body=body)

def doc2index(docpath, indexpath):
    ix = generateIndex(generateSchema(), indexpath)
    addFolderToIndex(ix, docpath)

def queryIndex(indexpath, query_term, N=20):
    ix = getIndex(indexpath)

    relevantDocuments = []
    
    with ix.searcher() as searcher:
        qp = QueryParser('body', schema=ix.schema)
        q = qp.parse(query_term)
        print(q)
        results = searcher.search(q, limit=N, terms=True)
    
        for result in results:
            relevantDocuments.append((result['docno'], result['headline']))
    
    return relevantDocuments 


