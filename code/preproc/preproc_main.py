#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:24:02 2024

@author: Filippo Cerpelloni
"""

from preproc_option import preproc_option
from preproc_extract import preproc_extract

### VISUAL BRAILLE TRAINING - preproc DATA 
# 
# Main script to extract information from raw data
#
# From inputs data (extracted from Pavlovia), take the subjects that have
# completed the experiment and "preprocess" / clean the results and log
# tables.


# Get options
opt = preproc_option()


# Extract data from raw
# For each subject, extract data from the four different days of training
# - import each CSV and extract responses
# - import log file and extract timings
# - save relevant files in /outputs/extracted_data/subID
preproc_extract(opt)
