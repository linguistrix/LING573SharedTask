#!/bin/sh

python2.7 src/AgregateParallelRunResults.py ./parallel_run_output_evaltest/ ./outputs/QA.outputs_2007

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/evaltest/factoid-docs.litkowski.2007.txt outputs/QA.outputs_2007 lenient > results/QA.results_2007_lenient

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/evaltest/factoid-docs.litkowski.2007.txt outputs/QA.outputs_2007 strict > results/QA.results_2007_strict

