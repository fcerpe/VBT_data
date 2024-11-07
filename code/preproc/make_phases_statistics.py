#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:12:43 2024

@author: cerpelloni
"""

import os
import pandas as pd
import glob

def make_phases_statistics(opt):
    
    #  MAKE SUMMARY TABLE 
    # Organize infromation about accuracy and timing for each subjects and day of training
    
    # Import data

    # Get "preproc" folder
    # Glob is used to find specific patterns within a path (e.g. 'sub-*')
    subjects = glob.glob(os.path.join(opt['dir']['extracted'], 'sub-*'))

    # Initialize summary table
    summary = pd.DataFrame()


    # Extract data participant by participant
    for sub in subjects:
        
        # Get subject path
        subPath = sub

        # Extract sub name and ID to compose the subject's entry
        subID = subPath.split('-')[2]
        subName = 'sub-' + subID

        # Compose new entry for table
        entry = init_entry(opt, subID)
        
        # Notify the user
        print(f'\n\nWorking on {subName}\n')
        
        # Get the different session folders
        sessions = glob.glob(os.path.join(opt['dir']['extracted'], subName, 'ses-*'))


        # Work on each file
        for ses in sessions:
            
            # Get session
            sesPath = ses
            
            # Extract sub name and ID to compose the subject's entry
            sesID = sesPath.split('-')[3]
            sesName = 'ses-' + sesID

            # Notify the user
            print(f'- adding data from {sesName}')

            # Find elements in the folder
            sesFiles = glob.glob(os.path.join(opt['dir']['extracted'], subName, sesName, '*_phases-time*'))
            
            scriptID = sesFiles[0].split('-')[7][:2]
        
            # Load the tables from the folder
            timings = pd.read_csv(sesFiles[0])
            
            # Process the results (e.g. compute means) and add them to the
            # right columns of the entry
            entry = add_results_to_entry(entry, sesName, timings)

        
        # Add the entry to the summary
        summary = pd.concat([summary, entry])
        
    
    # Save table
    if not os.path.exists(opt['dir']['stats']):
        os.makedirs(opt['dir']['stats'])


    summary.to_csv(os.path.join(opt['dir']['stats'], 'VBT_experiment-completion-time.csv'), index = False)
    
    # Notify the user
    print(f"\n\nCREATED TABLE FOR ACCURACY AND TIMING \nResults are stored in: {os.path.join(opt['dir']['stats'])}")


### Subfunctions

# from a folder, load the corresponding results for each part of the training

# Initialize custom dataframe / table
def init_entry(opt, subID):
    tableOut = pd.DataFrame(columns=['subject', 'script',
                                     'ses-1_total', 'ses-1_training', 'ses-1_break','ses-1_test', 
                                     'ses-2_total', 'ses-2_refresh', 'ses-2_instructions', 'ses-2_training', 'ses-2_break','ses-2_test', 
                                     'ses-3_total', 'ses-3_training', 'ses-3_break','ses-3_test', 
                                     'ses-4_total', 'ses-4_training', 'ses-4_break','ses-4_test'])

    # Add subject
    tableOut.loc[0, "subject"] = subID

    # Find and add script
    scriptID = opt['subList'].index(subID)
    tableOut.loc[0, "script"] = opt['scriptList'][scriptID]

    return tableOut


# Extract subject's means and add them to the corresponding line in the table
def add_results_to_entry(tableIn, sesName, timings):
    tableOut = tableIn.copy()

    if sesName == 'ses-001':
        
        tableOut.loc[0, "ses-1_total"] = timings.Timing[0]
        tableOut.loc[0, "ses-1_test"] = timings.Timing[1]
        tableOut.loc[0, "ses-1_break"] = timings.Timing[2]
        tableOut.loc[0, "ses-1_training"] = timings.Timing[3]

    elif sesName == 'ses-002':
        
        tableOut.loc[0, "ses-2_total"] = timings.Timing[0]
        tableOut.loc[0, "ses-2_test"] = timings.Timing[1]
        tableOut.loc[0, "ses-2_break"] = timings.Timing[2]
        tableOut.loc[0, "ses-2_training"] = timings.Timing[3]
        tableOut.loc[0, "ses-2_instructions"] = timings.Timing[4]
        tableOut.loc[0, "ses-2_refresh"] = timings.Timing[5]

    elif sesName == 'ses-003':
        
        tableOut.loc[0, "ses-3_total"] = timings.Timing[0]
        tableOut.loc[0, "ses-3_test"] = timings.Timing[1]
        tableOut.loc[0, "ses-3_break"] = timings.Timing[2]
        tableOut.loc[0, "ses-3_training"] = timings.Timing[3]

    elif sesName == 'ses-004':
        
        tableOut.loc[0, "ses-4_total"] = timings.Timing[0]
        tableOut.loc[0, "ses-4_test"] = timings.Timing[1]
        tableOut.loc[0, "ses-4_break"] = timings.Timing[2]
        tableOut.loc[0, "ses-4_training"] = timings.Timing[3]


    return tableOut

