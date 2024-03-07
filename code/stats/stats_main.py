#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:24:02 2024

@author: Filippo Cerpelloni
"""

from stats_option import stats_option
from stats_summarize_accuracy_timing import stats_summarize_accuracy_timing
from stats_anova_accuracy_timing import stats_anova_accuracy_timing

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


### First analyses - accuracy and timings

## Summarize accuracy and timing
#
# for each subject, extract and save 
# - accuracies (test and training) 
# - timings (reading, checking, writing) 
# Save a summary csv in
# outputs/derivatives/summary/VBT_summary_results-accuracies-timings.csv
stats_summarize_accuracy_timing(opt)

## Perform first anovas
#
# Are there differences between groups in terms of
# - accuracy across test sessions
# - accuracy across training sessions 
# - reading time during training sessions
# - writing times during training and test sessions
stats_anova_accuracy_timing(opt)

