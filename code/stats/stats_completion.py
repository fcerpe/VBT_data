#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:40:46 2024

@author: cerpelloni
"""

import os
import pandas as pd
import pingouin as pg
from dfply import group_by, summarize
import scipy.stats as stats
from statsmodels.stats.multitest import *


def stats_completion(opt):
    
    # Load table
    summary = pd.DataFrame()
    summary = pd.read_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-completion-time.csv'))
    
    sums = pd.DataFrame()
    
    # Session sums
    session_columns = {
        "ses-1": ["ses-1_train", "ses-1_break", "ses-1_test"],
        "ses-2": ["ses-2_refresh", "ses-2_train", "ses-2_break", "ses-2_test"],
        "ses-3": ["ses-3_train", "ses-3_break", "ses-3_test"],
        "ses-4": ["ses-4_train", "ses-4_break", "ses-4_test"]}

    # Create a new DataFrame with summed session columns
    for session, cols in session_columns.items():
        sums[session + '_sum'] = summary[cols].sum(axis = 1)

    # Phases sums
    phases_columns = {
        "letter-training": ["ses-1_train"],
        "letter-refresh": ["ses-2_refresh"],
        "word-training": ["ses-2_train", "ses-3_train", "ses-4_train"],
        "word-test": ["ses-1_test", "ses-2_test", "ses-3_test", "ses-4_test"]}
    
    # Create a new DataFrame with summed session columns
    for phase, cols in phases_columns.items():
        sums[phase + '_sum'] = summary[cols].sum(axis = 1)
        
        
    # Averages
    mean_row = sums.mean(numeric_only = True)
    sums = pd.concat([sums, mean_row.to_frame().T], ignore_index = True)
    
    # Save averages
    sums.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-completion-average.csv'), index = False)


    