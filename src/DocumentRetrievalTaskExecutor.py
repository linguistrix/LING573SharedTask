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
    
    def Execute(self, session):
        session.relevantDocuments = []
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

    with ix.searcher() as searcher:
        qp = QueryParser('body', schema=ix.schema)
        q = qp.parse(query_term)
        results = searcher.search(q, limit=N, terms=True)
        print ('Total results: {0}'.format(len(results)))
        for result in results:
            print ('{0}: {1}'.format(result['docno'], result['headline']))

if __name__ == '__main__':
    # Current test only for XIE documents!
    #  (DOC (DOCNO) (DATE_TIME) (BODY (HEADLINE) (TEXT) ) )

    if len(sys.argv) < 2:
        print('Usage:\n./script.py create <docpath> <indexpath>\n./script.py query <indexpath> <query_term> <N>')
        sys.exit(0)

    if sys.argv[1] == 'create':
        if len(sys.argv) != 4:
            print('Usage:\n./script.py create <docpath> <indexpath>')
            sys.exit(0)
        start_time = time.time()
        docpath = sys.argv[2]
        indexpath = sys.argv[3]
        print('Creating index at {0} using documents in {1}'.format(indexpath, docpath))
        doc2index(docpath, indexpath)
        end_time = time.time()
        print('Time taken: {0}'.format(end_time - start_time))

    elif sys.argv[1] == 'query':
        if len(sys.argv) != 5:
            print('Usage: ./script.py query <indexpath> <query_term> <N>')
            sys.exit(0)
        start_time = time.time()
        indexpath = sys.argv[2]
        queryterm = sys.argv[3]
        N = int(sys.argv[4])
        queryIndex(indexpath,queryterm,N)
        end_time = time.time()
        print('Time taken: {0:6.2f} sec'.format(end_time - start_time))







