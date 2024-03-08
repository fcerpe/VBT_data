#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:03:14 2024

We assessed that accuracy and timings (reading, writing) across sessions do not 
differ between groups (Braille v. Connected-Braille).
Here we want to assess the role played by the statistics of the stimuli learned.

Questions:
    - how do they learn? 
    
    - which statistics play a role in learning (a.k.a which are correlated)?
        * word frequency
        * word length
        * word orthographic neighbours
        * word phonologic neighbours
        * letter frequency
        * letter neighbours (shape-based)
        
    - are there differences in testing due to the nature of the stimulus seen?
        * seen words
        * novel words
        * pseudo-words


To operationalize, this function computes the followin statistics: 
    - TBD

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob

def make_stimuli_statistics(opt):
    
    # If it has not been done already, extract the stimuli and their properties
    
    
    opt, stimuliStats = get_stimuli_stats(opt)
    
    
    
    

### Subfunctions

# Read tables of stimuli, DLP2, etc and merge them to extract statistics
# Return the table and save it for future use
def get_stimuli_stats(opt):

    # Create list of stimuli post-hoc
    # Extract training set from ses-002 and test sets from each session
    tr2 = pd.read_csv(os.path.join(opt['dir']['extracted'], 'sub-00004', 'ses-002', 
                                  'sub-00004_ses-002_task-alphabetLearning_script-cb_beh-training.csv'))
    tr3 = pd.read_csv(os.path.join(opt['dir']['extracted'], 'sub-00004', 'ses-003', 
                                  'sub-00004_ses-003_task-alphabetLearning_script-cb_beh-training.csv'))
    tr4 = pd.read_csv(os.path.join(opt['dir']['extracted'], 'sub-00004', 'ses-004', 
                                  'sub-00004_ses-004_task-alphabetLearning_script-cb_beh-training.csv'))
    
    ## Make list of training stimuli
    tr2.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    tr3.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    tr4.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    tr = pd.DataFrame({'woord': tr2.nlWrd, 'test_2': tr2.test, 'test_3': tr3.test, 'test_4': tr4.test})
    
    # Add a tags to training stimuli
    # - tested: where they tested? If so, on which session? [0,2,3,4]
    tr['session'] = tr.apply(lambda row: 2 if row['test_2'] == 1 
                                         else (3 if row['test_3'] == 1 
                                               else (4 if row['test_4'] == 1
                                                     else 0)), axis = 1)
    tr = tr[['woord','session']]
    
    # Save training list
    tr.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-list.csv'), index = False)
    
    
    ## Make list of all test stimuli
    # Extract stimuli from tests of each day
    te1 = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'test_d1.csv'))
    te2 = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'test_d2.csv'))
    te3 = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'test_d3.csv'))
    te4 = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'test_d4.csv'))
    
    te1.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    te2.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    te3.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    te4.sort_values(by = ['nlWrd'], inplace = True, ignore_index = True)
    
    te1Subset = te1[['nlWrd']].copy()
    te2Subset = te2[['nlWrd']].copy()   
    te3Subset = te3[['nlWrd']].copy()
    te4Subset = te4[['nlWrd']].copy()
    
    # Add a tags to the test stimuli
    # - session: on which day were they presented? [1,2,3,4]
    te1Subset['session'] = 1
    te2Subset['session'] = 2
    te3Subset['session'] = 3
    te4Subset['session'] = 4
    te = pd.concat([te1Subset, te2Subset, te3Subset, te4Subset], ignore_index = True)
    te = te.rename(columns = {'nlWrd': 'woord'})
    
    # - type: are they [seen] words, [novel] words or [pseudo]words?
    te['type'] = te['woord'].isin(tr['woord']).map({True: 'seen', False: None})
    

    
    
    
    
    
    
    
    tableOut = 0
    
    return opt, tableOut    









