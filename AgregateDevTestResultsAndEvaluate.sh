#!/bin/sh

python2.7 src/AgregateParallelRunResults.py ./parallel_run_output/ ./outputs/QA.outputs_2006

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt outputs/QA.outputs_2006 lenient > results/QA.results_2006_lenient

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt outputs/QA.outputs_2006 strict > results/QA.results_2006_strict
