LING573SharedTask
=================

Repo for the LING573 Question Answering Shared Task
D1 report can be found at doc/reports/D1.pdf

Results for D2 can be reproduced by running ./D2_run_all.sh
D2 report can be found at doc/reports/D2.pdf

D3
Lenient Score: 0.3609
Strict Score: 0.2433
=======

D3 report can be found at doc/reports/D3.pdf


D4
======================
DevTest (TREC 2006)
Lenient Score: 0.390364270146
Strict Score: 0.268501844668

EvalTest (TREC 2007)
Lenient Score: 0.415578587723
Strict Score: 0.26704210807


Execute the following commands to reproduce the results:

# Dev Test
    ./GenerateParallelDevTestRunCondorScript.sh 

    condor_submit parallel_run_all.cmd

# Wait for all Condor jobs to finish

    ./AgregateDevTestResultsAndEvaluate.sh

# Eval Test
    ./GenerateParallelEvalTestRunCondorScript.sh 

    condor_submit parallel_run_all.cmd

# Wait for all Condor jobs to finish

    ./AgregateEvalTestResultsAndEvaluate.sh
