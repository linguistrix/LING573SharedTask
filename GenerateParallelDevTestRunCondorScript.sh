#!/bin/sh

mkdir -p parallel_run_output_devtest

python2.7 src/GenerateParallelEvaluationScript.py QA devtest ./devtest/TREC-2006.xml ./parallel_run_output_devtest/ parallel_run_all_devtest.cmd

