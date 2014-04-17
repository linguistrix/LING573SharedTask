# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# CreateIndex.py
# Generates Whoosh index of the given data files

import os, os.path
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