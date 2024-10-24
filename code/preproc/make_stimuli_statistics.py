#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:03:14 2024

Function to combine the list of stimuli presented during the different days of 
the visual braille training experiment with  data about the statistics of the 
dutch language. 

The function will create a series of tables to be used in stats:
    - lists of training and test stimuli (if not already present, otherwise 
      will just read them) 
    - relevant information from Dutch Lexicon Project (DLP2) dataset 
    - statistics made based on the individual words presented (accuracy, timing)
Then, it will merge the stimuli lists with behavioural data and statistics  
Lastly, it will save (individual and merged) tables in outputs/derivatives/datasets 

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob as glob
import Levenshtein as lev

def make_stimuli_statistics(opt):
    
    # Get the stimuli list
    # If the files are not already present in the stats/datasets folder, make them
    tr, te = get_stimuli_lists(opt)
    
    # Load datasets of statistics
    dlp = get_dutch_statistics(opt)
    
    # Compute stimuli accuracy and timings
    letters, training, test = get_results_stimuli(opt)
    
    # Extract qualitative information about the test responses:
    # - how distant were the responses from the correct answers
    # - which letters have been omitted most and which have been mistaken 
    # - which words have been recognized the most / the least
    test = extract_test_responses(test)
    
    # Exclude outliers
    training, test = exclude_outliers(training, test)
        
    # Apply the statistics to the training and test sets
    trStats = pd.merge(tr, dlp, on = 'woord', how = 'left')
    teStats = pd.merge(te, dlp, on = 'woord', how = 'left')

    # Save the datasets
    trStats.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-list-with-stats.csv'), index = False)
    teStats.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-list-with-stats.csv'), index = False)
    
    letters.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-letters_desc-behavioural-results.csv'), index = False)
    training.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-training_desc-behavioural-results.csv'), index = False)
    test.to_csv(os.path.join(opt['dir']['stats'], 'datasets', 'VBT_stimuli-test_desc-behavioural-results.csv'), index = False)


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
        # Participant is not important, they all saw the same stimuli
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
        
        # If it's session one, there are no 'seen' words. All are novel
        teSeen.loc[(teSeen['session'] == 1) & (teSeen['stimulus'] == 'seen'), 'stimulus'] = 'novel'
        
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
    

# Extract information about stimuli for training of letters, training of words,
# testing of words
def get_results_stimuli(opt):
    
    # For each subject
    # import all the files
    # extract letters: add repetition, order alphabetically, extract columns, append
    # extract training: add sub, group, day, extract columns, append
    # extract test: add day, type, sub, group, extract columns, append
    
    # Get "preproc" folder
    # Glob is used to find specific patterns within a path (e.g. 'sub-*')
    subjects = glob.glob(os.path.join(opt['dir']['extracted'], 'sub-*'))

    # Initialize summary table
    letters = pd.DataFrame()
    training = pd.DataFrame()
    test = pd.DataFrame()

    # Extract data participant by participant
    for sub in subjects:
        
        # Get subject path
        subPath = sub

        # Extract sub name and ID to compose the subject's entry
        subID = subPath.split('-')[2]

        # Take path of letters (day 1)
        le = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-001', '*-training.csv'))[0])
        
        # Take path of training (days 2-3-4)
        tr2 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-002', '*-training.csv'))[0])
        tr3 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-003', '*-training.csv'))[0])
        tr4 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-004', '*-training.csv'))[0])     
        
        # Take path of test (days 1-2-3-4)
        te1 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-001', '*-test.csv'))[0])
        te2 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-002', '*-test.csv'))[0])
        te3 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-003', '*-test.csv'))[0])
        te4 = pd.read_csv(glob.glob(os.path.join(subPath, 'ses-004', '*-test.csv'))[0])

        # Get the relevant information out of the letters
        le = extract_letters_information(opt, subID, le)
        
        # Get the relevant information out of the letters
        tr = extract_training_information(opt, subID, tr2, tr3, tr4)
        
        # Get the relevant information out of the letters
        te = extract_test_information(opt, subID, te1, te2, te3, te4)
        
        # Exclude outliers
        tr, te = exclude_outliers(tr, te)
        
        # Add the entries to the statistics
        letters = pd.concat([letters, le], ignore_index = True)
        training = pd.concat([training, tr], ignore_index = True)
        test = pd.concat([test, te], ignore_index = True)
        

    return letters, training, test


# From behavioural results of letters training, extract and order information of 
# one participant
def extract_letters_information(opt, subID, le):
        
    # Add important columns
    # - repetition
    # - subject
    # - script (after fetching relative name)
    le['repetition'] = le.index.map(get_stimulus_repetition)
    le['subject'] = 'sub-' + subID
    
    scriptID = opt['subList'].index(subID)
    le['script'] = opt['scriptList'][scriptID]
    
    # Re-arrange table and drop redundant letter column
    letters = le[['subject','script','repetition','letter','readingTime','checkingTime']]
    
    return letters
    

# From behavioural results of word trainings, extract and order information of 
# one participant
def extract_training_information(opt, subID, tr2, tr3, tr4):
    
    # Add 'day' information to each file
    tr2['session'] = '2'
    tr3['session'] = '3'
    tr4['session'] = '4'
    
    # Merge and add information about script and subject
    tr = pd.concat([tr2, tr3, tr4])
    tr['subject'] = 'sub-' + subID
    
    scriptID = opt['subList'].index(subID)
    tr['script'] = opt['scriptList'][scriptID]
    
    # Re-arrange table and drop redundant letter column
    tr = tr.rename(columns = {'nlWrd': 'woord', 'testResp': 'response'})
    training = tr[['subject','script','session','woord','tested','response','score','readingTime','checkingTime','writingTime']]
    
    return training


# From behavioural results of word test, extract and order information of 
# one participant
def extract_test_information(opt, subID, te1, te2, te3, te4):
    
    # Add 'day' information to each file
    te1['session'] = '1'
    te2['session'] = '2'
    te3['session'] = '3'
    te4['session'] = '4'
    
    # Merge and add information about script and subject
    te = pd.concat([te1, te2, te3, te4])
    te['subject'] = 'sub-' + subID
    
    scriptID = opt['subList'].index(subID)
    te['script'] = opt['scriptList'][scriptID]
    
    # Re-arrange table and drop redundant letter column
    te = te.rename(columns = {'nlWrd': 'woord', 'testResp': 'response', 'attempts': 'keypresses'})
    test = te[['subject','script','session','woord','response','score','readingTime','writingTime', 'keypresses']]
    
    return test


# Extract information from test responses:
# - distance (levensthein) between target and response
# - which letters were identified, omitted, mistaken for another
def extract_test_responses(te):
    
    # Initialize new columns to be added to table
    distances = []
    mistakes = []
    newResponses = []
    
    # go entry by entry and correct them
    for target, response, score in zip(te['woord'], te['response'], te['score']):
        
        # edit response to add missing dots, useful to then comupute mistakes and 
        # distance between response and correct answer
        response = adjust_response(response)    

        # Calculate Levensthein distance between two strings
        # (number of changes to go from one to the other)
        distance = lev.distance(response, target)
        
        # In case the strings don't match, have a look at why
        if distance > 0:
            
            # Check omitted letters or mistook ones
            mistake = assess_mistakes(response, target)
            
        else:
            mistake = []
                        
        # Save new columns to be added to table
        distances.append(distance/len(target))
        mistakes.append(mistake)
        newResponses.append(response)
        
    # Add new columns and update answers
    te['distance'] = distances
    te['mistakes'] = mistakes
    te['response'] = newResponses

    return te


# Assess which mistakes were made in the response
def assess_mistakes(re, ta):
    
    mi = ''
    
    # If the first character of the response is not equal to the target and 
    # it's not a '.', assume that the participant did not follow the instructions 
    # to mark the skipped letters and do it yourself   
    if not (re[0] == ta[0] or re[0] == '.') or len(re) > len(ta) :
        
        # Ask for manual check
        return 'Requires manual assessment'
        
        # # compare current response with the case of adding +1 or +2 dots at the beginning
        # rePlus1 = '.' + re
        # rePlus2 = '..' + re
        
        # lev0 = lev.distance(re, ta)
        # lev1 = lev.distance(rePlus1, ta)
        # lev2 = lev.distance(rePlus2, ta)
        
        # # which is closest to answer? Assign the corresponding string and prefer 
        # # minimal changes if dots don't improve distance
        # closest = min([lev0, lev1, lev2])
        # if closest == lev0: 
        #     re = re
        # elif closest == lev1:
        #     re = rePlus1
        # elif closest == lev2:
        #     re = rePlus2
                
    # take the difference in length between strings and add dots to match lengths
    if len(re) < len(ta):
        
        # compute number of dots to add
        nbDots = len(ta) - len(re)
        
        # add at the end of the string
        re = re + '.'*nbDots
        
    # Asess errors
    for iLet in range(0, len(re)):
        
        # If the letter in response is different from target, store it with the 
        # corresponding target
        if not re[iLet] == ta[iLet]:
            mi = mi + ta[iLet] + '-' + re[iLet] + '_'
            
    mi = mi[:-1]
    
    return mi
    
    mi = []
    
    # look up each letter against the same one in that position
    
    return mi


# Fix the missing dots to have equally long strings
def adjust_response(re):
    
    # First checks on the response
    # - make sure it's not empty 
    if pd.isna(re): 
        re = '.'
        
    # - make sure it contains only lower-case letters
    re = re.lower()
        
    return re


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


# Assign a number to the repetition of letters in the letters training
def get_stimulus_repetition(idx):
    
    if idx < 26:
        return '1'
    
    elif idx < 52:
        return '2'
    
    elif idx < 78:
        return '3'
    
    elif idx < 104:
        return '4'
    
    elif idx < 130:
        return '5'
    
    elif idx < 156:
        return '6'
    
    else:
        return '7'
    

# Exclude outliers form each subject
def exclude_outliers(train, test):
    
    # Training reading time, max 60 seconds. Then considered outlier
    train = train[(train['readingTime'] <= 60) | train['readingTime'].isna()]
    
    # Test writing time
    # - exclude cases where no key was pressed if the time is shorter than 1s or longer than 30s
    selection = test[((test['writingTime'] > 30)) | 
                      (test['writingTime'] > 60)]
    
    test = test.drop(selection.index)
    
    return train, test