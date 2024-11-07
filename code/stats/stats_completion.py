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
    
    phases = summary
    
    # Extract and split per script
    totals = ['subject', 'script'] + [col for col in summary.columns if 'total' in col]

    # Keep only the desired columns
    summary = summary[totals]
    
    # Save totals
    summary.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-total-time.csv'), index = False)
    
    # Display the resulting DataFrame for each script value
    br_totals = summary[summary['script'] == 'br']
    cb_totals = summary[summary['script'] == 'cb']
    
    # Compute means and stds for each script
    br_totals_only = br_totals.filter(regex="^ses-\d+_total$")
    cb_totals_only = cb_totals.filter(regex="^ses-\d+_total$")
    phases_time = phases.filter(regex="^ses-\d+_[A-Za-z]+$")
    
    # Calculate means and standard deviations for br and cb tables on ses-X_total columns
    br_means = br_totals_only.mean()
    br_stds = br_totals_only.std()
    cb_means = cb_totals_only.mean()
    cb_stds = cb_totals_only.std()
    phases_means = phases_time.mean()
    phases_stds = phases_time.std()
    
    # Create a summary DataFrame for br script
    br_summary = pd.DataFrame({'script': 'br', 'session': br_means.index, 
                               'mean': br_means.values, 'std_dev': br_stds.values})

    cb_summary = pd.DataFrame({'script': 'cb', 'session': cb_means.index,
                               'mean': cb_means.values, 'std_dev': cb_stds.values})
    phases_summary = pd.DataFrame({'session': phases_means.index, 'mean': phases_means.values, 'std_dev': phases_stds.values})

    # Combine the br and cb summaries into a single table
    descriptive = pd.concat([br_summary, cb_summary], ignore_index = True)
    
    # Save descriptives
    descriptive.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-total-time-descriptives.csv'), index = False)
    phases_summary.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-phases-time-descriptives.csv'), index = False)
    
    # Make stats over the group differences
    sessions = []
    ttests = []
    dofs = []
    pvals = []
    for i in range(1,5):
        
        session_col = f'ses-{i}_total'
        
        # Select data for br and cb scripts for the current session column
        br_data = summary[summary['script'] == 'br'][session_col]
        cb_data = summary[summary['script'] == 'cb'][session_col]
        
        # Perform t-test between br and cb scripts for the given session
        stat, pval = stats.ttest_ind(br_data, cb_data)
        
        # Calculate degrees of freedom
        dof = len(br_data) + len(cb_data) - 2
            
        # Store the results
        sessions.append(session_col)
        ttests.append(stat)
        pvals.append(pval)
        dofs.append(dof)

    
    # Apply Bonferroni correction to the p-values
    _, bonf_pvals, _, _ = multipletests(pvals, alpha = 0.05, method = 'bonferroni')
    
    # Create a DataFrame with the results
    ttest_results = pd.DataFrame({
        'session': sessions,
        't_statistic': ttests,
        'deg_freedom': dofs,
        'p_value': pvals,
        'bonferroni_p_value': bonf_pvals
    })
    
    # Save the results
    ttest_results.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-total-time-stats.csv'), index = False)




    