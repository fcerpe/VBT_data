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
        * letter frequency
        
    - are there differences in testing due to the nature of the stimulus seen?
        * seen words
        * novel words
        * pseudo-words


To operationalize, this function computes the following statistics: 
    - correlations

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob as glob
from scipy.stats import pearsonr


def stats_stimuli_properties(opt):
    
    # OTHER FOLDER: 
    # - load tables with statstics 
    # - extract statistics for stimuli used
    # - save skimmed tables
    # - re-organize results summary to have something based on words and not on sessions
    
    # Load stimuli results 
    leResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                         'VBT_stimuli-letters_desc-behavioural-results.csv'))
    trResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                         'VBT_stimuli-training_desc-behavioural-results.csv'))
    teResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                         'VBT_stimuli-test_desc-behavioural-results.csv'))
    
    # Load stimuli statistics
    leStats = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                       'VBT_stimuli-letters_desc-list-with-stats.csv'))
    trStats = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                       'VBT_stimuli-training_desc-list-with-stats.csv'))
    teStats = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                       'VBT_stimuli-test_desc-list-with-stats.csv'))
    
    
    # Calculate lenght for all stimuli, including pseudo-words
    trStats['length'] = trStats['woord'].apply(lambda x: len(x))
    teStats['length'] = teStats['woord'].apply(lambda x: len(x))
    
    # Convert scores from T/F to 1/0
    trResults['score'] = trResults['score'].astype(int)
    teResults['score'] = teResults['score'].astype(int)

    
    ## Letters
    # Averages across repetitions and across subjects
    leInds, leAvgs = merge_results_stats(leResults, leStats, 'letters')

    # Correlate results averages with language statistics
    # - use stats length, frequency, orthographic neighbours 
    # - use results score, writing time, distance 
    leCorrAvgs = correlate_letters(leAvgs)
    
    # Make the same correlations on individual subjects, to create cloud of variance
    # A lot of warnings will pop-up, they indicate that 'score' is a constant (participant performed 0 in that session)
    # and that therefore there won't be a correlation 
    leCorrInds = pd.DataFrame()
        
    for sub in leInds['subject'].unique():
        
        leCorrInds = pd.concat([leCorrInds, 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 1)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 2)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 3)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 4)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 5)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 6)]), 
                                correlate_letters(leInds[(leInds['subject'] == sub) & (leInds['repetition'] == 7)])], axis = 0)
        

    ## Training
    # Extract average and individual tables for tested and non-tested items
    trTInds, trTAvgs, trNTInds, trNTAvgs = merge_results_stats(trResults, trStats, 'training')

    # Correlate results averages with language statistics
    # - use stats length, frequency, orthographic neighbours 
    # - use results score, writing time, distance 
    trTCorrAvgs = pd.concat([correlate_trainings(trTAvgs[trTAvgs['session_x'] == 2]),
                             correlate_trainings(trTAvgs[trTAvgs['session_x'] == 3]),
                             correlate_trainings(trTAvgs[trTAvgs['session_x'] == 4])], axis = 0)
    trNTCorrAvgs = pd.concat([correlate_trainings(trNTAvgs[trNTAvgs['session_x'] == 2]),
                              correlate_trainings(trNTAvgs[trNTAvgs['session_x'] == 3]),
                              correlate_trainings(trNTAvgs[trNTAvgs['session_x'] == 4])], axis = 0)
        
    # Make the same correlations on individual subjects, to create cloud of variance
    # A lot of warnings will pop-up, they indicate that 'score' is a constant (participant performed 0 in that session)
    # and that therefore there won't be a correlation 
    trTCorrInds = pd.DataFrame()
    trNTCorrInds = pd.DataFrame()
        
    for sub in trTInds['subject'].unique():
   
        trTCorrInds = pd.concat([trTCorrInds, 
                                correlate_trainings(trTInds[(trTInds['subject'] == sub) & (trTInds['session_x'] == 2)]), 
                                correlate_trainings(trTInds[(trTInds['subject'] == sub) & (trTInds['session_x'] == 3)]), 
                                correlate_trainings(trTInds[(trTInds['subject'] == sub) & (trTInds['session_x'] == 4)])], axis = 0)
        
        trNTCorrInds = pd.concat([trNTCorrInds, 
                                correlate_trainings(trNTInds[(trNTInds['subject'] == sub) & (trNTInds['session_x'] == 2)]), 
                                correlate_trainings(trNTInds[(trNTInds['subject'] == sub) & (trNTInds['session_x'] == 3)]), 
                                correlate_trainings(trNTInds[(trNTInds['subject'] == sub) & (trNTInds['session_x'] == 4)])], axis = 0)
        

    ## Test
    # Extract average and individual tables
    teInds, teAvgs = merge_results_stats(teResults, teStats, 'test')
    
    # Correlate results averages with language statistics
    # - use stats length, frequency, orthographic neighbours 
    # - use results score, writing time, distance 
    teCorrAvgs = pd.concat([correlate_tests(teAvgs[teAvgs['session'] == 1]), 
                            correlate_tests(teAvgs[teAvgs['session'] == 2]),
                            correlate_tests(teAvgs[teAvgs['session'] == 3]),
                            correlate_tests(teAvgs[teAvgs['session'] == 4])], axis = 0)
        
    # Make the same correlations on individual subjects, to create cloud of variance
    # A lot of warnings will pop-up, they indicate that 'score' is a constant (participant performed 0 in that session)
    # and that therefore there won't be a correlation 
    teCorrInds = pd.DataFrame()
    
    for sub in teInds['subject'].unique():
   
        teCorrInds = pd.concat([teCorrInds, 
                                correlate_tests(teInds[(teInds['subject'] == sub) & (teInds['session_x'] == 1)]), 
                                correlate_tests(teInds[(teInds['subject'] == sub) & (teInds['session_x'] == 2)]), 
                                correlate_tests(teInds[(teInds['subject'] == sub) & (teInds['session_x'] == 3)]), 
                                correlate_tests(teInds[(teInds['subject'] == sub) & (teInds['session_x'] == 4)])], axis = 0)
        
        
    # Save all the correlations
    leCorrAvgs.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-letters_variable-linguistic-stats_analysis-correlations_desc-average.csv'), index = False)
    leCorrInds.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-letters_variable-linguistic-stats_analysis-correlations_desc-individual.csv'), index = False)
    
    trTCorrAvgs.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-tested-items-average.csv'), 
                       index = False)
    trNTCorrAvgs.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-nontested-items-average.csv'), 
                        index = False)
    trTCorrInds.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-tested-items-individual.csv'), 
                       index = False)
    trNTCorrInds.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-nontested-items-individual.csv'), 
                        index = False)
    
    teCorrAvgs.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-average.csv'), index = False)
    teCorrInds.to_csv(os.path.join(opt['dir']['results'], 
                                   'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-individual.csv'), index = False)
    

   
### Subfunctions

# From test behvioural results, extract averages and subject tables
def merge_results_stats(tab, stats, flag):
    
    # TEST DATA
    if flag == 'test':
        
        # Extract individual scores, writing times, distances for variance purposes
        inds = tab[['subject', 'script', 'session', 'woord', 'score', 'writingTime', 'distance']].sort_values(['subject','session','woord'])
        inds.reset_index(drop = True)
        
        # Average scores, writing time, distance from the correct answer
        avgs = tab.groupby(['script', 'session', 'woord']).agg({'score': 'mean','writingTime': 'mean','distance': 'mean'}).reset_index()
    
        # In the averages, separate groups in different columns (BR v. CB)
        avgs = avgs.pivot(index = 'woord', columns = 'script', values=['score', 'writingTime', 'distance'])
        avgs.columns = ['_'.join(col) for col in avgs.columns]
        avgs.reset_index(inplace = True)
        
        # Merge tables into one
        avgs = pd.concat([stats, avgs.iloc[:, 1:]], axis = 1)
        inds = pd.merge(inds, stats, on = 'woord', how = 'left')
        
        return inds, avgs
    
    
    # TRAINING DATA
    elif flag == 'training':
        
        # Separate tested items
        t = tab[tab['tested'] == 1]
        t = t[['subject', 'script', 'session', 'woord', 'response', 'score', 'writingTime', 'checkingTime']]
        nt = tab[tab['tested'] == 0]
        nt = nt[['subject', 'script', 'session', 'woord', 'readingTime', 'checkingTime']]
        
        
        # Extract individual scores, writing times, distances for variance purposes
        tInds = t[['subject', 'script', 'session', 'woord', 'score', 'writingTime']].sort_values(['subject','session','woord'])
        tInds.reset_index(drop = True)
        ntInds = nt[['subject', 'script', 'session', 'woord', 'readingTime']].sort_values(['subject','session','woord'])
        ntInds.reset_index(drop = True)
        
        # Exclude outliers in time, maybe participant took a break
        
        # Merge with stats
        tInds = pd.merge(tInds, stats, on = 'woord', how = 'left') 
        ntInds = pd.merge(ntInds, stats, on = 'woord', how = 'left')
        
        
        # Compute averages
        tAvgs = t.groupby(['script', 'session', 'woord']).agg({'score': 'mean', 'writingTime': 'mean'}).reset_index()
        ntAvgs = nt.groupby(['script','session','woord']).agg({'readingTime': 'mean','checkingTime': 'mean'}).reset_index()
        
        # In the averages, separate groups in different columns (BR v. CB)
        tAvgs = tAvgs.pivot_table(index = ['session', 'woord'], columns = 'script', values = ['score', 'writingTime'], aggfunc = 'first')
        tAvgs.columns = ['_'.join(map(str, col)).strip() for col in tAvgs.columns.values]
        tAvgs.reset_index(inplace=True)
        
        ntAvgs = ntAvgs.pivot(index = ['session','woord'], columns = 'script', values = ['readingTime'])
        ntAvgs.columns = ['_'.join(col) for col in ntAvgs.columns]
        ntAvgs.reset_index(inplace = True)
       
        # Merge tables into one
        tAvgs = pd.merge(tAvgs, stats, on = 'woord', how = 'left')
        ntAvgs = pd.merge(ntAvgs, stats, on = 'woord', how = 'left')
        
        return tInds, tAvgs, ntInds, ntAvgs
    
    
    # LETTERS DATA
    elif flag == 'letters':
        
        # Extract individual times (reading and checking), averaging the repetitions for each subject
        inds = tab.groupby(['subject', 'script', 'repetition', 'letter']).agg({'readingTime': 'mean', 'checkingTime': 'mean'}).reset_index()
        
        # Merge with stats
        inds = pd.merge(inds, stats, on = 'letter', how = 'left') 

        # Compute averages
        avgs = tab.groupby(['script', 'letter']).agg({'readingTime': 'mean', 'checkingTime': 'mean'}).reset_index()
    
        # Separate groups into different columns, to avoid having too many variables
        avgs = avgs.pivot(index = 'letter', columns = 'script', values = ['readingTime', 'checkingTime'])
        avgs.columns = ['_'.join(col) for col in avgs.columns]
        avgs.reset_index(inplace = True)
        
        # Merge tables into one
        avgs = pd.merge(avgs, stats, on = 'letter', how = 'left')
            
        return inds, avgs
    
    # NO INFO PROVIDED
    else: 
        return []
                

# Correlate each column to all the other ones and produce clean output with stats
def correlate_letters(tab):
    
    tab.reset_index(inplace = True)

    # Different structures fro individual and averages
    if 'subject' in tab.columns: 
        
        # Individual correlations 
        # * session is repetition 
        # * correlation table has more information, more columns
        # * results don't indicate the script
        session = tab['repetition'][0]
        correlationColumns = ['subject', 'script', 'column1', 'column2', 'stimuli', 'repetition', 
                              'correlation', 'p_value', 'degrees_of_freedom']
        resultColumns = ['readingTime', 'checkingTime']

    else:
        # Average correlations 
        # * session is cast as 0, not relevant here
        # * correlation table has less information
        # * results indicate the script
        session = 0
        correlationColumns = ['column1', 'column2', 'correlation', 'p_value', 'degrees_of_freedom']
        resultColumns = ['readingTime_br', 'checkingTime_br', 'readingTime_cb', 'checkingTime_cb']

    # Stats is constant and it's only one
    statsColumns = ['frequency']

    # Initialize list to store correlation results
    correlations = []

    ## Compute correlations  
     
    # Look at al the comparisons
    for i, col1 in enumerate(resultColumns):
        for j, col2 in enumerate(statsColumns):
                
            correlations = add_correlations(tab, col1, col2, correlations, 'all', session) 
                
                            
    # if we're dealing with averages, we don't need repetituon information
    if session == 0:
        correlations = [[sublist[0], sublist[1], *sublist[4:]] for sublist in correlations]
    
    # Cast correlations as dataframe
    correlations = pd.DataFrame(correlations, columns = correlationColumns)
    
    return correlations



# Correlate each column to all the other ones and produce clean output with stats
def correlate_trainings(tab):
    
    tab.reset_index(inplace = True)
    
    # Define valid columns based on individual correlation of average ones 
    if 'subject' in tab.columns: 
        
        # Individual correlations 
        # * session is different variable 
        # * correlation table has more information, more columns
        session = tab['session_x'][0]
        correlationColumns = ['subject', 'script', 'column1', 'column2', 'stimuli', 'session', 
                              'correlation', 'p_value', 'degrees_of_freedom']
        
        # Define which variable will be correlated based on tested or not tested
        if 'score' in tab.columns:
            
            # Tested items - multiple scores and times
            resultColumns = ['score', 'writingTime']
            
        else:
            # Not tested - only one score, time
            resultColumns = ['readingTime']
            
        
    else:
        # Average scores - duplicate scores, distances, times, and restriced info in correlation table
        session = tab['session_x'][0]
        correlationColumns = ['column1', 'column2', 'stimuli', 'session', 'correlation', 'p_value', 'degrees_of_freedom']

        # Define which variable will be correlated based on tested or not tested
        if 'score_br' in tab.columns:
            
            # Tested items - multiple scores
            resultColumns = ['score_br', 'score_cb', 'writingTime_br', 'writingTime_cb']
            
        else:
            # Not tested - only one score, distance, time
            resultColumns = ['readingTime_br', 'readingTime_cb']

            
    # stats are always the same
    statsColumns = ['length', 'frequency', 'old20']

    # Initialize list to store correlation results
    correlations = []

    ## Compute correlations  
     
    # Look at al the comparisons
    for i, col1 in enumerate(resultColumns):
        
        for j, col2 in enumerate(statsColumns):
                
            correlations = add_correlations(tab, col1, col2, correlations, 'all', session) 
                
                            
    # Cast correlations as dataframe
    correlations = pd.DataFrame(correlations, columns = correlationColumns)
    
    return correlations


# Correlate each column to all the other ones and produce clean output with stats
def correlate_tests(tab):
    
    tab.reset_index(inplace = True)
    
    # Define valid columns based on individual correlation of average ones 
    if 'subject' in tab.columns: 
        
        # Individual correlations 
        # * session is different variable 
        # * only one score, distance, time
        # * correlation table has more information, more columns
        resultColumns = ['score', 'writingTime', 'distance']
        statsColumns = ['length', 'frequency', 'old20']
        fullColumns = ['score', 'writingTime', 'distance', 'length']
        session = tab['session_x'][0]
        correlationColumns = ['subject', 'script', 'column1', 'column2', 'stimuli', 'session', 
                              'correlation', 'p_value', 'degrees_of_freedom']
        
    else:
        # Average scores - duplicate scores, distances, times, and restriced info in correlation table
        resultColumns = ['score_br', 'score_cb', 'distance_br', 'distance_cb', 'writingTime_br', 'writingTime_cb']
        statsColumns = ['length', 'frequency', 'old20']
        fullColumns = ['score_br', 'score_cb', 'distance_br', 'distance_cb', 'writingTime_br', 'writingTime_cb', 'length']
        session = tab['session'][0]
        correlationColumns = ['column1', 'column2', 'stimuli', 'session', 'correlation', 'p_value', 'degrees_of_freedom']


    # Initialize list to store correlation results
    correlations = []

    ## Compute correlations  
     
    # Look at al the comparisons
    for i, col1 in enumerate(resultColumns):
        
        for j, col2 in enumerate(statsColumns):
                
            # If we know it contains values for all the stimulus types, correlate the whole set
            if (col1 in fullColumns) and (col2 in fullColumns):
                # do overall correlation
                correlations = add_correlations(tab, col1, col2, correlations, 'all', session) 
                
                # isolate pseudowords
                correlations = add_correlations(tab, col1, col2, correlations, 'pseudo', session) 
              
            # Otherwise, only correlate real words instead of all stimuli
            else:
                # non-pseudo words
                correlations = add_correlations(tab, col1, col2, correlations, 'real', session) 
                
            # novel words
            correlations = add_correlations(tab, col1, col2, correlations, 'novel', session) 
          
            # In session one there are no seen words
            if not session == 1:
                
                # seen words
                correlations = add_correlations(tab, col1, col2, correlations, 'seen', session)               

    # Cast correlations as dataframe
    correlations = pd.DataFrame(correlations, columns = correlationColumns)
    
    return correlations



# Compute correlations for one set of stimuli
def add_correlations(tab, col1, col2, corrs, stimulus, session):
    
    # Based on stimulus type:
    # - all the stimuli, select everything
    # - real words, select not pseudo
    # - pseudo, novel, seen; select specific 
    if stimulus == 'all':
        selection = tab
        
    elif stimulus == 'real':
        selection = tab[tab['stimulus'] != 'pseudo']   
        
    else:
        selection = tab[tab['stimulus'] == stimulus]               


    # compute correlation
    corr_coef, p_value = pearsonr(selection[col1], selection[col2])
    
    # add it to the list
    # If there is a subject columns, we are working on individual correlations. 
    # Otherwise it's average and we don't need extra columnd
    if 'subject' in tab.columns:
        corrs.append([tab['subject'][0], tab['script'][0], col1, col2, stimulus, session, corr_coef, p_value, len(selection) - 2])
        
    else:
        corrs.append([col1, col2, stimulus, session, corr_coef, p_value, len(selection) - 2])
    
    
    return corrs
