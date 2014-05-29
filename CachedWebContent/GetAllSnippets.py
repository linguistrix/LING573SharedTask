# GetAllSnippets.py
# Author: Julian Chan

import os 
import sys
import time
import urllib2
import nltk
import unicodedata
import codecs 
from BeautifulSoup import BeautifulSoup

def extract_snippets(htmlContent, maxCount):
    snippets = []
    soup = BeautifulSoup(htmlContent)
   
    numberOfSnippets = 0
    for element in soup.findAll('span',{'class':'nDesc'}):
        if (numberOfSnippets >= maxCount):
            break

        snippet = u""
        for c in element.contents:
            snippet += c.string.strip() + " "
        snippet = snippet.strip()
        snippet = snippet.replace('...','')
        snippet = snippet.replace('<b>','')
        snippet = snippet.replace('</b>','')
        snippet = snippet.replace('&middot','')
        snippet = snippet.replace('&nbsp','')
        snippet = snippet.replace('&quot','')
        snippet = snippet.replace('&amp','')
        snippet = snippet.replace('\n','')
        snippet = snippet.replace('&#39','')
        snippets.append(snippet)
        numberOfSnippets += 1
    
    return snippets

def fetch_snippet(html_prefix,q_id,query,count):
    return fetch_snippet_from_ask(html_prefix,q_id, query,count)

def fetch_snippet_from_ask(html_prefix,q_id,query,count):
    amount = 0
    url = 'http://www.search.ask.com/web?q=%s&page=%s'

    page = 1
    continued = True
    snippets = []

    temp = query.split()
    ask_query = "+".join(temp)
    
    allHtmlContent = "" 

    while continued:
        time.sleep(0.5)
        q = url%(ask_query,page)
        page += 1
        
        try:
            print q
            response = urllib2.urlopen(q)
            the_page = response.read()
            
            allHtmlContent += the_page + "\n"    
            
            soup = BeautifulSoup(the_page)
            amount += len(soup.findAll('div',{'id':'summary'}))
            print amount
            if amount >= count:
                print 'fetch %d snippets for %s'%(amount,q_id)
                continued = False
        except:
            html = html_prefix+ "_" + str(page-1)
            sys.stderr.write("Excpetion " + html + '\n')
            continued = False

    return extract_snippets(allHtmlContent, count)

if len(sys.argv) != 4:
    print("GetAllSnippets.py cacheDir queryFile count")
    sys.exit()

cache_dir = sys.argv[1]
query_file = sys.argv[2]
count = int(sys.argv[3])

if cache_dir.endswith('/') == False:
    cache_dir += '/'

with open(query_file,'r') as f:
    question_context = ''
    qid = ''
    quiz = ''
    for line in f:
        line = line.strip()
        tokens = line.split(':')
        query_id = tokens[0].strip()
        query = tokens[1].strip()
        html = cache_dir + query_id 
        print html
        snippets = fetch_snippet(html,qid,query,count)
			
        with codecs.open(os.path.join(cache_dir, query_id + ".snippets"),'w', 'utf-8') as f:
            output = "\n".join(snippets)
            f.write(output)
            #f.write(unicodedata.normalize('NFKD', output).encode("utf-8", "ignore"))





