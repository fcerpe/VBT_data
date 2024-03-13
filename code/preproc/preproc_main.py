#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 2024

Main function to preprocess data downloaded from Pavlovia
From raw data for results (.csv) and timings (.log), will extract:
1. clean tables for each subject (1..80) / session (1..4) / data type (accuacy or timing)
   saved in outputs/derivatives/extracted-data
   
2. one summary table containing average accuracies and timings for
   each subject and session, to be used in stats
   
3. 

@author: Filippo Cerpelloni
"""

from preproc_option import preproc_option
from preproc_extract import preproc_extract
from make_accuracy_timing import make_accuracy_timing
from make_stimuli_statistics import *


# Get options
opt = preproc_option()


### Clean tables for each individual subject / session

# Extract data from raw
# For each subject, extract data from the four different days of training
# - import each CSV and extract responses
# - import log file and extract timings
# - save relevant files in /outputs/extracted_data/subID
preproc_extract(opt)


### Create tables for analyses

## Summarize accuracy and timing
# for each subject, save accuracies (test and training) and timings (reading, checking, writing) 
# as a summary in: outputs/derivatives/summary/VBT_summary_results-accuracies-timings.csv
make_accuracy_timing(opt)


## Extract statistics of stimuli presented
# If not prsent, load the statistics of stimuli (from DLP2, and SUBTLEX) and 
# merge it with the stimuli used in the experiment
# Then, create tables for each important statistic (full list inside the function)
make_stimuli_statistics(opt)



