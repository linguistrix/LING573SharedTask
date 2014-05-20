LING573SharedTask
=================

Repo for the LING573 Question Answering Shared Task
D1 report can be found at doc/reports/D1.pdf

Results for D2 can be reproduced by running ./D2_run_all.sh
D2 report can be found at doc/reports/D2.pdf

D3
Lenient Score: 0.3609
Strict Score: 0.2433

Execute the following commands to reproduce the results:

./GenerateParallelDevTestRunCondorScript.sh 

condor_submit parallel_run_all.cmd

# Wait for all Condor jobs to finish

python2.7 src/AgregateParallelRunResults.py ./parallel_run_output/ ./outputs/D3.outputs 

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt outputs/D3.outputs strict > results/D3.results_strict

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt outputs/D3.outputs lenient > results/D3.results_lenient

