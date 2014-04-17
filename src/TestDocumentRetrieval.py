from DocumentRetrievalTaskExecutor import * 
import os, os.path, sys, time

if __name__ == '__main__':
    # Current test only for XIE documents!
    #  (DOC (DOCNO) (DATE_TIME) (BODY (HEADLINE) (TEXT) ) )

    if len(sys.argv) < 2:
        print('Usage:\n./TestDocumentRetrieval.py create <docpath> <indexpath>\n./script.py query <indexpath> <query_term> <N>')
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
         
        relevantDocs = queryIndex(indexpath,queryterm,N)
        print("\n".join(map(lambda x: str(x), relevantDocs)))
        
        end_time = time.time()
        print('Time taken: {0:6.2f} sec'.format(end_time - start_time))








