#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:18:54 2024

@author: Filippo Cerpelloni
"""


from viz_option import viz_option
from viz_accuracy_timing import * 
from viz_stimuli_statistics import *

### VISUAL BRAILLE TRAINING - VISUALIZATION
# 
# Main script to make plots 

# Get options
opt = viz_option()


## Analyses on overall accuracy and timings 
#
# Are there differences between groups in terms of
# - accuracy across test sessions
# - accuracy across training sessions 
# - reading time during training sessions
# - writing times during training and test sessions
#viz_accuracy_timing(opt)


## Analyses on stimuli scores: accuracy and timings related to language statistics
#
# Correlation between 
# - test sessions accuracy, writing time, distance from answer
# - training sessions reading and writing time, accuracy in tested items
# - letter session reading time
# and
# - word length, number of syllables, frequency, orthographic and phonological neighbours
# - letter frrequency 
viz_stimuli_statistics(opt)


# viz_scatter(opt)