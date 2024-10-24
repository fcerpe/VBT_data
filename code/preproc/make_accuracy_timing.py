#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:34:15 2024

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob

def make_accuracy_timing(opt):
    
    #  MAKE SUMMARY TABLE 
    # Organize infromation about accuracy and timing for each subjects and day of training
    
    # Import data

    # Get "preproc" folder
    # Glob is used to find specific patterns within a path (e.g. 'sub-*')
    subjects = glob.glob(os.path.join(opt['dir']['extracted'], 'sub-*'))

    # Initialize summary table
    summary = pd.DataFrame()
    
    outliersWR = pd.DataFrame(columns = ['sub', 'ses', 'nlWrd', 'writingTime', 'score'])
    outliersRD = pd.DataFrame(columns = ['sub', 'ses', 'nlWrd', 'readingTime'])

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
            sesFiles = glob.glob(os.path.join(opt['dir']['extracted'], subName, sesName, '*_beh-*'))
            
            scriptID = sesFiles[0].split('-')[7][:2]
        

            # Based on session, distinguish which routines were presented
            if sesName in ['ses-001', 'ses-003', 'ses-004']:
                # Load the tables from the folder
                train, test, _ = load_results(sesFiles)
                
                # Save timings to investigate outliers
                outliersWR, outliersRD = add_outliers(train, test, outliersWR, outliersRD, subID, sesID, scriptID)
                
                # Exclude outliers based on sperate investigation from previous line
                train, test = exclude_outliers(train, test)
                
                # Process the results (e.g. compute means) and add them to the
                # right columns of the entry
                entry = add_results_to_entry(entry, sesName, train, test, [])

            elif sesName == 'ses-002':
                # Load the tables from the folder
                train, test, ref = load_results(sesFiles)
                
                # Save timings to investigate outliers
                outliersWR, outliersRD = add_outliers(train, test, outliersWR, outliersRD, subID, sesID, scriptID)
                
                # Exclude outliers based on sperate investigation from previous line
                train, test = exclude_outliers(train, test)

                entry = add_results_to_entry(entry, sesName, train, test, ref)
                

            

        # Add the entry to the summary
        summary = pd.concat([summary, entry])
        
    
    # Save table
    if not os.path.exists(opt['dir']['stats']):
        os.makedirs(opt['dir']['stats'])


    summary.to_csv(os.path.join(opt['dir']['stats'], 'VBT_results-accuracy-timing.csv'), index = False)
    outliersWR.to_csv(os.path.join(opt['dir']['stats'], 'VBT_investigation-outliers-writing.csv'), index = False)
    outliersRD.to_csv(os.path.join(opt['dir']['stats'], 'VBT_investigation-outliers-reading.csv'), index = False)
    

    # Notify the user
    print(f"\n\nCREATED TABLE FOR ACCURACY AND TIMING \nResults are stored in: {os.path.join(opt['dir']['stats'], 'VBT_results-accuracy-timing.csv')}")


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
        tableOut.loc[0, "ses-1_test-accuracy"] = sum(te['score']) / len(te)
        tableOut.loc[0, "ses-1_test-reading"] = te['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-1_test-writing"] = te['writingTime'].mean(skipna = True)

        tableOut.loc[0, "ses-1_train-reading"] = tr['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-1_train-checking"] = tr['checkingTime'].mean(skipna = True)

    elif sesName == 'ses-002':
        
        # Cut possible outliers in the train-reading and in test-writing
        
        
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
        tableOut.loc[0, "ses-2_test-accuracy"] = sum(te['score']) / len(te)
        tableOut.loc[0, "ses-2_test-reading"] = te['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-2_test-writing"] = te['writingTime'].mean(skipna = True)

        tableOut.loc[0, "ses-2_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-2_train-reading"] = tr['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-2_train-checking"] = tr['checkingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-2_train-writing"] = tr['writingTime'].mean(skipna = True)

        tableOut.loc[0, "ses-2_ref-reading"] = re['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-2_ref-checking"] = re['checkingTime'].mean(skipna = True)

    elif sesName == 'ses-003':
        
        # Need to assign the following variables
        # - 'ses-3_test-accuracy'
        # - 'ses-3_test-reading'
        # - 'ses-3_test-writing'
        # - 'ses-3_train-accuracy'
        # - 'ses-3_train-reading'
        # - 'ses-3_train-checking'
        # - 'ses-3_train-writing'
        tableOut.loc[0, "ses-3_test-accuracy"] = sum(te['score']) / len(te)
        tableOut.loc[0, "ses-3_test-reading"] = te['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-3_test-writing"] = te['writingTime'].mean(skipna = True)

        tableOut.loc[0, "ses-3_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-3_train-reading"] = tr['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-3_train-checking"] = tr['checkingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-3_train-writing"] = tr['writingTime'].mean(skipna = True)

    elif sesName == 'ses-004':
        
        # Need to assign the following variables
        # - 'ses-4_test-accuracy'
        # - 'ses-4_test-reading'
        # - 'ses-4_test-writing'
        # - 'ses-4_train-accuracy'
        # - 'ses-4_train-reading'
        # - 'ses-4_train-checking'
        # - 'ses-4_train-writing'
        tableOut.loc[0, "ses-4_test-accuracy"] = sum(te['score']) / len(te)
        tableOut.loc[0, "ses-4_test-reading"] = te['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-4_test-writing"] = te['writingTime'].mean(skipna = True)

        tableOut.loc[0, "ses-4_train-accuracy"] = sum(tr['score']) / 20
        tableOut.loc[0, "ses-4_train-reading"] = tr['readingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-4_train-checking"] = tr['checkingTime'].mean(skipna = True)
        tableOut.loc[0, "ses-4_train-writing"] = tr['writingTime'].mean(skipna = True)


    return tableOut


# Add timings to lists to control for outliers
def add_outliers(train, test, outliersWR, outliersRD, sub, ses, script):
    
    writing = pd.DataFrame({'sub': [sub]*len(test),
                            'ses': [ses]*len(test),
                            'script': [script]*len(test),
                            'nlWrd': test.nlWrd, 
                            'writing': test.writingTime, 
                            'breaks': test.breaks, 
                            'check': test.check, 
                            'score': test.score})
    outliersWR = pd.concat([outliersWR, writing], ignore_index = True)
    
    if not ses == '001':
    
        reading = pd.DataFrame({'sub': [sub]*len(train),
                                'ses': [ses]*len(train),
                                'nlWrd': train.nlWrd,
                                'readingTime': train.readingTime})
        outliersRD = pd.concat([outliersRD, reading], ignore_index = True)
    
    
    return outliersWR, outliersRD


# Exclude outliers form each subject
def exclude_outliers(train, test):
    
    # Training reading time, max 60 seconds. Then considered outlier
    train = train[(train['readingTime'] <= 60) | train['readingTime'].isna()]
    
    # Test writing time
    # - exclude cases where no key was pressed if the time is shorter than 1s or longer than 30s
    selection = test[(test['check'] == 0) & ((test['writingTime'] < 1) | (test['writingTime'] > 30)) | 
                     (test['breaks'] > 30) | (test['writingTime'] > 60)]
    
    test = test.drop(selection.index)
    
    return train, test


















