#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:34:15 2024

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob

def stats_summarize_accuracy_timing(opt):
    
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
            print(f'- adding data from {sesName}\n')

            # Find elements in the folder
            sesFiles = glob.glob(os.path.join(opt['dir']['extracted'], subName, sesName, '*'))

            # Based on session, distinguish which routines were presented
            if sesName in ['ses-001', 'ses-003', 'ses-004']:
                # Load the tables from the folder
                train, test, _ = load_results(sesFiles)

                # Process the results (e.g. compute means) and add them to the
                # right columns of the entry
                entry = add_results_to_entry(entry, sesName, train, test, [])

            elif sesName == 'ses-002':
                # Load the tables from the folder
                train, test, ref = load_results(sesFiles)

                entry = add_results_to_entry(entry, sesName, train, test, ref)

        # Add the entry to the summary
        summary = pd.concat([summary, entry])


    # Save table
    if not os.path.exists(opt['dir']['stats']):
        os.makedirs(opt['dir']['stats'])


    summary.to_csv(os.path.join(opt['dir']['stats'], 'VBT_results-accuracy-timing.csv'), index=False)



### Subfunctions

# from a folder, load the corresponding results for each part of the training
def load_results(files):
    # init outputs to avoid errors
    tr = pd.DataFrame()
    te = pd.DataFrame()
    re = pd.DataFrame()

    # find positions of files
    trPos = [i for i, file in enumerate(files) if file.endswith('training.csv')]
    tePos = [i for i, file in enumerate(files) if file.endswith('test.csv')]

    # Load files
    tr = pd.read_csv(files[trPos[0]])
    te = pd.read_csv(files[tePos[0]])

    # Load extra file if we are in session 2
    if 'ses-002' in files[0]:
        rePos = [i for i, file in enumerate(files) if file.endswith('refresh.csv')]
        re = pd.read_csv(files[rePos[0]])

    return tr, te, re


# Initialize custom dataframe / table
def init_entry(opt, subID):
    tableOut = pd.DataFrame(columns=['subject', 'script',
                                     'ses-1_test-accuracy', 'ses-1_test-reading', 'ses-1_test-writing',
                                     'ses-1_train-reading', 'ses-1_train-checking',
                                     'ses-2_test-accuracy', 'ses-2_test-reading', 'ses-2_test-writing',
                                     'ses-2_train-accuracy', 'ses-2_train-reading', 'ses-2_train-checking',
                                     'ses-2_train-writing', 'ses-2_ref-reading', 'ses-2_ref-checking',
                                     'ses-3_test-accuracy', 'ses-3_test-reading', 'ses-3_test-writing',
                                     'ses-3_train-accuracy', 'ses-3_train-reading', 'ses-3_train-checking',
                                     'ses-3_train-writing', 'ses-4_test-accuracy', 'ses-4_test-reading',
                                     'ses-4_test-writing', 'ses-4_train-accuracy', 'ses-4_train-reading',
                                     'ses-4_train-checking', 'ses-4_train-writing'])

    # Add subject
    tableOut.loc[0, "subject"] = subID

    # Find and add script
    scriptID = opt['subList'].index(subID)
    tableOut.loc[0, "script"] = opt['scriptList'][scriptID]

    return tableOut


# Extract subject's means and add them to the corresponding line in the table
def add_results_to_entry(tableIn, sesName, tr, te, re):
    tableOut = tableIn.copy()

    if sesName == 'ses-001':
        
        # Need to assign the following variables
        # - 'ses-1_test-accuracy'
        # - 'ses-1_test-reading'
        # - 'ses-1_test-writing'
        # - 'ses-1_train-reading'
        # - 'ses-1_train-checking'
        tableOut.loc[0, "ses-1_test-accuracy"] = sum(te['score']) / 60
        tableOut.loc[0, "ses-1_test-reading"] = te['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-1_test-writing"] = te['writingTime'].mean(skipna=True)

        tableOut.loc[0, "ses-1_train-reading"] = tr['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-1_train-checking"] = tr['checkingTime'].mean(skipna=True)

    elif sesName == 'ses-002':
        
        # Need to assign the following variables
        # - 'ses-2_test-accuracy'
        # - 'ses-2_test-reading'
        # - 'ses-2_test-writing'
        # - 'ses-2_train-accuracy'
        # - 'ses-2_train-reading'
        # - 'ses-2_train-checking'
        # - 'ses-2_train-writing'
        # - 'ses-2_ref-reading'
        # - 'ses-2_ref-checking'
        tableOut.loc[0, "ses-2_test-accuracy"] = sum(te['score']) / 60
        tableOut.loc[0, "ses-2_test-reading"] = te['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-2_test-writing"] = te['writingTime'].mean(skipna=True)

        tableOut.loc[0, "ses-2_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-2_train-reading"] = tr['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-2_train-checking"] = tr['checkingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-2_train-writing"] = tr['writingTime'].mean(skipna=True)

        tableOut.loc[0, "ses-2_ref-reading"] = re['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-2_ref-checking"] = re['checkingTime'].mean(skipna=True)

    elif sesName == 'ses-003':
        
        # Need to assign the following variables
        # - 'ses-3_test-accuracy'
        # - 'ses-3_test-reading'
        # - 'ses-3_test-writing'
        # - 'ses-3_train-accuracy'
        # - 'ses-3_train-reading'
        # - 'ses-3_train-checking'
        # - 'ses-3_train-writing'
        tableOut.loc[0, "ses-3_test-accuracy"] = sum(te['score']) / 60
        tableOut.loc[0, "ses-3_test-reading"] = te['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-3_test-writing"] = te['writingTime'].mean(skipna=True)

        tableOut.loc[0, "ses-3_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-3_train-reading"] = tr['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-3_train-checking"] = tr['checkingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-3_train-writing"] = tr['writingTime'].mean(skipna=True)

    elif sesName == 'ses-004':
        
        # Need to assign the following variables
        # - 'ses-4_test-accuracy'
        # - 'ses-4_test-reading'
        # - 'ses-4_test-writing'
        # - 'ses-4_train-accuracy'
        # - 'ses-4_train-reading'
        # - 'ses-4_train-checking'
        # - 'ses-4_train-writing'
        tableOut.loc[0, "ses-4_test-accuracy"] = sum(te['score']) / 60
        tableOut.loc[0, "ses-4_test-reading"] = te['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-4_test-writing"] = te['writingTime'].mean(skipna=True)

        tableOut.loc[0, "ses-4_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-4_train-reading"] = tr['readingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-4_train-checking"] = tr['checkingTime'].mean(skipna=True)
        tableOut.loc[0, "ses-4_train-writing"] = tr['writingTime'].mean(skipna=True)


    return tableOut

