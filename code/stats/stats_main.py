#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:24:02 2024

@author: Filippo Cerpelloni
"""

from stats_option import stats_option
from stats_accuracy_and_timing import stats_accuracy_and_timing

### VISUAL BRAILLE TRAINING - MAKE SUMMARY TABLES
# 
# Main script to create different summary tables 
# 
# From pre-processed data, take each subject and extract values for the 
# following parameters: 
# - accuracies
# - timings
# - qualitative analyses (type of mistakes)


# Get options
opt = stats_option()


## Summarize accuracy and timing
#
# For each subject, extract and save 
# - accuracies (test and training) 
# - timings (reading, checking, writing) 
# Save a summary csv in
# outputs/derivatives/summary/VBT_summary_results-accuracies-timings.csv
stats_accuracy_and_timing(opt)


