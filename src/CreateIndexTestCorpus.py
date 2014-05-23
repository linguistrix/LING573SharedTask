# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# CreateIndex.py
# Generates Whoosh index of the given data files

import os, os.path, sys, time
from bs4 import BeautifulSoup
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME

def generateSchema():
    schema = Schema(docno=ID(unique=True, stored=True), headline=TEXT(stored=True), body=TEXT)
    return schema

def generateIndex(schema, folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        ix = index.create_in(folderpath, schema)
        print ('Index folder not found. Creating new index.')
    else:
        print ('Index folder found. Updating index.')
        ix = index.open_dir(folderpath)

    return ix

def addFolderToIndex(ix, folderpath):
    count = 0

    for root, _, files in os.walk(folderpath):
        for f in files:
            if f[-3:] != 'xml':
                continue
                print ('Skipping ' + f)
            print (f)
            fullpath = os.path.join(root, f)
            addFileToIndex(ix, fullpath)
            count += 1
            print count

    print('Added {0} files to the Index'.format(count))

def addFileToIndex(ix, filepath):

    f = open(filepath)
    html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'xml')

    with ix.writer() as writer:
        for doc in soup.find_all('DOC'):
            doc_no = unicode(doc['id'])
            #doc_no = unicode(doc.DOCNO.string.strip())
            if doc.HEADLINE is not None:
                headline = unicode(doc.HEADLINE.string.strip().replace('\n', ' '))
            else:
                headline = u''
            body = unicode(doc.TEXT.get_text().strip())
            #print ('{0}, {1}'.format(doc_no, headline))
            writer.add_document(docno=doc_no, headline=headline, body=body)

def doc2index(docpath, indexpath):
    ix = generateIndex(generateSchema(), indexpath)
    addFolderToIndex(ix, docpath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ./CreateIndex.py <docpath> <indexpath>')
        sys.exit(0)

    start_time = time.time()
    docpath = sys.argv[1]
    indexpath = sys.argv[2]
    print('Creating index at {0} using documents in {1}'.format(indexpath, docpath))
    doc2index(docpath, indexpath)
    end_time = time.time()
    print('Time taken: {0}'.format(end_time - start_time))
