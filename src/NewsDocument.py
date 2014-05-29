# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# NewsDocument.py
# Provides the Document class that stores a news document.

from bs4 import BeautifulSoup
import os, re

class Document:
    def __init__(self):
        self.body = ''
        self.docid = ''
        self.headline = ''

    def loadDocumentFromID(self, docid, folderpath, datatype):
        # Takes the Document Number / Doc ID and the path to the LDC02T31 folder
        # and populates the object with the document
        # Returns True if successful and False if not
        #print folderpath
        if datatype == 'devtest':
            filepath = self.getFilePath(docid, folderpath, datatype)

            if os.path.exists(filepath):
                f = open(filepath, 'r')
                html_doc = '<SUPERDOC>' + f.read() + '</SUPERDOC>'
                f.close()
            else:
                return False
            soup = BeautifulSoup(html_doc, 'xml')
            for doc in soup.find_all('DOC'):
                cur_doc_no = doc.DOCNO.string.strip()
                if cur_doc_no != docid:
                    continue

                if (doc.HEADLINE != None):
                    headline = doc.HEADLINE.string.strip()
                else:
                    headline = ""
                if (doc.TEXT != None):
                    body = doc.TEXT.get_text().strip()
                else:
                    body = ""

                self.body = body
                self.docid = cur_doc_no
                self.headline = headline

                return True
        elif datatype == 'evaltest':
            filepath = self.getFilePath(docid, folderpath, datatype)

            if os.path.exists(filepath):
                f = open(filepath, 'r')
                html_doc = f.read()
                f.close()
            else:
                return False
            soup = BeautifulSoup(html_doc, 'xml')
            for doc in soup.find_all('DOC'):
                cur_doc_no = unicode(doc['id'])
                if cur_doc_no != docid:
                    continue

                if (doc.HEADLINE != None):
                    headline = doc.HEADLINE.string.strip().replace('\n', ' ')
                else:
                    headline = ""
                if (doc.TEXT != None):
                    body = doc.TEXT.get_text().strip()
                else:
                    body = ""

                self.body = body
                self.docid = cur_doc_no
                self.headline = headline
                return True

        return False


    def getFilePath(self, docid, folderpath, datatype):
        if datatype == 'devtest':
            matcher = re.match(r"(XIE|APW|NYT)(\d{4})(\d{4})\.(\d{4})", docid)
            suffix_dict = {'NYT':'NYT', 'APW':'APW_ENG', 'XIE':'XIN_ENG'}
            if matcher is not None:
                source = matcher.group(1)
                year = matcher.group(2)
                mmdd = matcher.group(3)
                id = matcher.group(4)
                return os.path.join(folderpath, source.lower(), year, year + mmdd + "_" + suffix_dict[source])
        elif datatype == 'evaltest':
            dirname = docid[:7].lower()
            filename = docid[:14].lower()
            return os.path.join(folderpath, 'data', dirname, filename + '.xml')



