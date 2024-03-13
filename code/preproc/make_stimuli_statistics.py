#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:03:14 2024

Function to combine the list of stimuli presented during the different days of 
the visual braille training experiment with  data about the statistics of the 
dutch language. 

The function will first try to read the lists of training and test stimuli. 
If that is not possible, it will create them from the lists of stimuli presented 
during each day. 
Then, it will load the Dutch Lexicon Project (DLP2) dataset and extract relevant 
columns before adding information about the stimuli used to training and test lists. 
Lastly, it will save the tables in outputs/derivatives/datasets 

@author: Filippo Cerpelloni
"""

import os
import pandas as pd

def make_stimuli_statistics(opt):
    
    # Get the stimuli list
    # If the files are not already present in the stats/datasets folder, make them
    tr, te = get_stimuli_lists(opt)
    
    # Load datasets of statistics
    dlp = get_dutch_statistics(opt)
    
    # Apply the statistics to the training and test sets
    trStats = pd.merge(tr, dlp, on = 'woord', how = 'left')
    teStats = pd.merge(te, dlp, on = 'woord', how = 'left')

    # Save the datasets
    trStats.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-stats.csv'), index = False)
    teStats.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-stats.csv'), index = False)



### Subfunctions

# Read tables of stimuli, DLP2, etc and merge them to extract statistics
# Return the table and save it for future use
def get_stimuli_lists(opt):
    
    trFullpath = os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-list.csv')
    
    # If the training file does not exists, we can assume the test ones do not either.
    # Create them
    if not os.path.exists(trFullpath):
        
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
        
        # Add a tags to the test stimuli
        # - session: on which day were they presented? [1,2,3,4]
        te1Subset = te1[['nlWrd']].copy()
        te2Subset = te2[['nlWrd']].copy()   
        te3Subset = te3[['nlWrd']].copy()
        te4Subset = te4[['nlWrd']].copy()
    
        te1Subset['session'] = 1
        te2Subset['session'] = 2
        te3Subset['session'] = 3
        te4Subset['session'] = 4
        
        
        # - stimulus type, organized in sequence (seen, pseudo, novel)
        for t in [te1Subset, te2Subset, te3Subset, te4Subset]:
            t['stimulus'] = t.index.map(get_stimulus_type)
        
        # Concatenate the days and sort them
        te = pd.concat([te1Subset, te2Subset, te3Subset, te4Subset])
        te = te.rename(columns = {'nlWrd': 'woord'})
        te.sort_values(by = ['woord'], inplace = True, ignore_index = True)
        
        # Create separate DataFrames for each type of stimulus
        teSeen = te[te['stimulus'] == 'seen']
        tePseudo = te[te['stimulus'] == 'pseudo']
        teNovel = te[te['stimulus'] == 'novel']
        
        # Save test lists: both full and single types
        te.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-list.csv'), index = False)
        
        teSeen.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-seen-words.csv'), index = False)
        tePseudo.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-pseudowords.csv'), index = False)
        teNovel.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-novel-words.csv'), index = False)


    # If the training file (and the others) do exist, load them
    else: 
        tr = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-list.csv'))
        te = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-list.csv'))
        

    return tr, te    


# Read dutch exicon project (DLP2) table and extract relevant columns
def get_dutch_statistics(opt):
    
    # Load the file
    dlpPath = os.path.join(opt['dir']['stats'], 'datasets', 'DLP2_dataset.xlsx')
    dlp = pd.read_excel(dlpPath, 
                        sheet_name='DLP2_eerste_analyses')
    
    # Adjust the dataset
    # - keep only relevant columns
    dlp = dlp[['Woord', 'Length', 'Nsyl', 'SUBTLEX2', 'N_phonemes', 'OLD20', 'PLD30']]
    
    # - rename columns 
    dlp = dlp.rename(columns = {'Woord': 'woord', 
                                'Length': 'length', 
                                'Nsyl': 'syllabels',
                                'SUBTLEX2': 'frequency',
                                'N_phonemes': 'phonemes',
                                'OLD20': 'old20',
                                'PLD30': 'pld30'})
    
    return dlp
    
# Assign the type of test stimulus (seen words, pseudo-words, novel words)
def get_stimulus_type(idx):
    
    # type of stimulus depends on its position in the test_dayX.csv file
    # - 1-20: seen words
    # - 21-40: pseudo-words
    # - 41-60: novel words
    if idx < 20:
        return 'seen'
    
    elif idx < 40:
        return 'pseudo'
    
    else:
        return 'novel'







