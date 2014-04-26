#!/bin/sh

./EvaluateSystem.sh D2 /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml ./outputs/D2.outputs 

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt ./outputs/D2.outputs strict > outputs/D2.results_strict

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt ./outputs/D2.outputs lenient > outputs/D2.results_lenient
