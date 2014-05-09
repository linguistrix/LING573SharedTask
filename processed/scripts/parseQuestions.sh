#!/bin/bash

PARSER=/NLP_TOOLS/parsers/berkeleyparser/latest/
java -jar $PARSER/berkeleyParser.jar -gr $PARSER/eng_sm6.gr < $1 > $2
