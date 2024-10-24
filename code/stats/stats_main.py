#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:24:02 2024

@author: Filippo Cerpelloni
"""

from stats_option import stats_option
from stats_accuracy_timing import *
from stats_stimuli_properties import * 

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


## Analyses on overall accuracy and timings 
#
# Are there differences between groups in terms of
# - accuracy across test sessions
# - accuracy across training sessions 
# - reading time during training sessions
# - writing times during training and test sessions
stats_accuracy_timing(opt)


## Analyses on stimuli scores: accuracy and timings related to language statistics
#
# Correlation between 
# - test sessions accuracy, writing time, distance from answer
# - training sessions reading and writing time, accuracy in tested items
# - letter session reading time
# and
# - word length, number of syllables, frequency, orthographic and phonological neighbours
# - letter frrequency 
stats_stimuli_properties(opt)


## Sums and averages about the completion time of each session
stats_completion(opt)
