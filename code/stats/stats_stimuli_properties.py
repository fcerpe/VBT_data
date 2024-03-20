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
        * letter neighbours (shape-based) TBD
        
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
    trStats = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                       'VBT_stimuli-training_desc-list-with-stats.csv'))
    teStats = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                       'VBT_stimuli-test_desc-list-with-stats.csv'))
    
    ## Letters
    # Averages across repetitions and across subjects
    leRepAverages = leResults.groupby(['subject', 'script', 'letter']).agg({
        'readingTime': 'mean',  
        'checkingTime': 'mean'}).reset_index()
    leAverages = leRepAverages.groupby(['script', 'letter']).agg({
        'readingTime': 'mean', 
        'checkingTime': 'mean'}).reset_index()

    # Separate groups into different columns, to avoid having too many variables
    leAverages = leAverages.pivot(index='letter', columns='script', values=['readingTime', 'checkingTime'])
    leAverages.columns = ['_'.join(col) for col in leAverages.columns]
    leAverages.reset_index(inplace = True)


    ## Training
    # Separate tested and non-tested items, to compute different averages 
    trTested = trResults[trResults['tested'] == 1]
    trTested = trTested[['subject', 'script', 'session', 'woord', 'response', 
                         'score', 'writingTime', 'checkingTime']]
    
    trTestedAverages = trTested.groupby(['script', 'session', 'woord']).agg({
        'score': 'mean',
        'writingTime': 'mean',
        'checkingTime': 'mean'
        }).reset_index()
    
    trNotTested = trResults[trResults['tested'] == 0]
    trNotTested = trNotTested[['subject', 'script', 'session', 'woord', 'readingTime', 'checkingTime']]
    
    trNotTestedAverages = trNotTested.groupby(['script', 'session', 'woord']).agg({
        'readingTime': 'mean',
        'checkingTime': 'mean'
        }).reset_index()
    
    # Separate sessions and groups
    
    
    ## Test
    # Average scores, writing time, distance from the correct answer
    teAverages = teResults.groupby(['script', 'session', 'woord']).agg({
        'score': 'mean',
        'writingTime': 'mean',
        'distance': 'mean'
        }).reset_index()
    
    # Separate groups in different columns (BR v. CB)
    teAverages = teAverages.pivot(index = 'woord', columns = 'script', values=['score', 'writingTime', 'distance'])
    teAverages.columns = ['_'.join(col) for col in teAverages.columns]
    teAverages.reset_index(inplace = True)
    
    # Add information about stimulus type, to avoid correlations with pseudo-words (there's no stats for that)
    teAverages['type'] = teStats[['stimulus']]

    # Merge tables into one
    test = pd.concat([teStats, teAverages.iloc[:, 1:-1]], axis = 1)
    
    # Add woord length to pseudo-words
    test['length'] = test['woord'].apply(lambda x: len(x))  
    
    # Correlate results and stats averages with language statistics
    # - exclude pseudo-words because we don't have stats for that (we could have length)
    # - use stats length, nb syllables, frequency, nb phonemes, ortho and phon neighbours 
    # - use results score, writing time, distance 
    corrTestSes1 = correlate_test_results(test[test['session'] == 1])
    corrTestSes2 = test[(test['session'] == 2) & (test['stimulus'] != 'pseudo')].drop(columns=['woord', 'stimulus','session']).corr()
    corrTestSes3 = test[(test['session'] == 3) & (test['stimulus'] != 'pseudo')].drop(columns=['woord', 'stimulus','session']).corr()
    corrTestSes4 = test[(test['session'] == 4) & (test['stimulus'] != 'pseudo')].drop(columns=['woord', 'stimulus','session']).corr()
    
    
    # Save all the results
    corrTestSes1.to_csv(os.path.join(opt['dir']['results'], 
                                     'VBT_data-test_variable-linguistic-stats_analysis-correlation_desc-ses-1.csv'), index = False)
    corrTestSes2.to_csv(os.path.join(opt['dir']['results'], 
                                     'VBT_data-test_variable-linguistic-stats_analysis-correlation_desc-ses-2.csv'), index = False)
    corrTestSes3.to_csv(os.path.join(opt['dir']['results'], 
                                     'VBT_data-test_variable-linguistic-stats_analysis-correlation_desc-ses-3.csv'), index = False)
    corrTestSes4.to_csv(os.path.join(opt['dir']['results'], 
                                     'VBT_data-test_variable-linguistic-stats_analysis-correlation_desc-ses-4.csv'), index = False)

    
   
### Subfunctions

# Correlate each column to all the other ones and produce clean output with stats
def correlate_test_results(tab):
    
    # Define columns for correlation
    validColumns = list(tab.columns[3:])
    fullColumns = ['length', 'score_br', 'score_cb', 'distance_br', 'distance_cb', 'writingTime_br', 'writingTime_cb']

    # Initialize list to store correlation results
    correlations = []

    ## Compute correlations

    # Keep track of which correlations have already been computed, to avoid doubles
    computed = set()   
     
    # Look at al the comparisons
    for i, col1 in enumerate(tab.columns):
        
        for j, col2 in enumerate(tab.columns):
          
            # Computeif (col1 in fullColumns) and (col2 in fullColumns): correlations only if it's a column with numerical values
            # i.e., skip 'woord', 'session', 'stimulus' and correlations between the same columns
            if (col1 in validColumns) and (col2 in validColumns) and (col1 != col2):
          
                # If the correlations haven't been computed yet
                if (col1, col2) not in computed and (col2, col1) not in computed:
                  
                    # Add session loop here
                  
                    # If we know it contains values for all the stimulus types,
                    # correlate the whole set
                    if (col1 in fullColumns) and (col2 in fullColumns):
                        # do overall correlation
                        corr_coef, p_value = pearsonr(tab[col1], tab[col2])
                        correlations.append([col1, col2, 'overall', corr_coef, p_value, len(tab) - 2])
                        
                        # isolate pseudowords
                        pseudo = tab[tab['stimulus'] == 'pseudo']               
        
                        # do pseudo correlation
                        corr_coef, p_value = pearsonr(pseudo[col1], pseudo[col2])
                        correlations.append([col1, col2, 'pseudo words', corr_coef, p_value, len(pseudo) - 2])
                      
                    # Otherwise, only correlate real words instead of all stimuli
                    else:
                        # isolate non-pseudo words
                        real = tab[tab['stimulus'] != 'pseudo']               
                        
                        # do non-pseudo correlation
                        corr_coef, p_value = pearsonr(real[col1], real[col2])
                        correlations.append([col1, col2, 'real words', corr_coef, p_value, len(real) - 2])
                        
                    # isolate novel words
                    novel = tab[tab['stimulus'] == 'novel']               
        
                    # do novel correlation
                    corr_coef, p_value = pearsonr(novel[col1], novel[col2])
                    correlations.append([col1, col2, 'novel words', corr_coef, p_value, len(novel) - 2])
                  
                    # isolate seen words
                    seen = tab[tab['stimulus'] == 'seen']               
        
                    # do seen correlation
                    corr_coef, p_value = pearsonr(seen[col1], seen[col2])
                    correlations.append([col1, col2, 'seen words', corr_coef, p_value, len(seen) - 2])
                  
                  
                    # Add this correlation to the list of already computed ones
                    computed.add((col1, col2))

    # Cast correlations as dataframe
    correlations = pd.DataFrame(correlations, columns = ['column1', 'column2', 'stimuli', 'session', 
                                                         'correlation', 'p_value', 'degrees_of_freedom'])

    
    
    
    
    
    # Initialize correlation matrix 
    correlations = []
    
    # Create all the subgroups to be correlated 
    
    # different session (4) * different stimuli (3+overall)
    ses1 = tab[tab['session'] == 1]
    ses2 = tab[tab['session'] == 2]
    ses3 = tab[tab['session'] == 3]
    ses4 = tab[tab['session'] == 4]
        
    # Correlate all the results score with woord length AND with themselves
    for i, col1 in enumerate(tabNoPseudo.columns):
        for j, col2 in enumerate(tabNoPseudo.columns):
            if i < j:
                corr_coef, p_value = pearsonr(tabNoPseudo[col1], tabNoPseudo[col2])
                correlations.append([col1, col2, corr_coef, p_value, len(tab)-2])
    
    
    
    
    # Separate pseudo-words from the rest
    tabNoPseudo = tab[tab['stimulus'] != 'pseudo']
    
    # Remove unnecessary columns to ease correlations 
    tab = tab.drop(columns=['woord', 'stimulus','session', 'syllables', 'phonemes', 'frequency', 'old20', 'pld30'])
    tabNoPseudo = tabNoPseudo.drop(columns=['woord', 'stimulus','session'])

    
    
                
    # Correlate all the WORDS scores with other linguistic properties
    for i, col1 in enumerate(tabNoPseudo.columns):
        for j, col2 in enumerate(tabNoPseudo.columns):
            if i < j:
                corr_coef, p_value = pearsonr(tabNoPseudo[col1], tabNoPseudo[col2])
                correlations.append([col1, col2, corr_coef, p_value, len(tab)-2])

    # Create a new DataFrame with the desired columns
    corrTable = pd.DataFrame(correlations, columns=['column1', 'column2', 'correlation', 'pValue', 'DoF'])

    
    return corrTable


    
import pandas as pd
from scipy.stats import pearsonr

# Sample DataFrame
data = {
    'column1': [1, 2, 3, 4, 5],
    'column2': [6, 7, 8, 9, 10],
    'column3': [11, 12, 13, 14, 15],
    'column4': [16, 17, 18, 19, 20],
}

df = pd.DataFrame(data)

# Compute correlation coefficients and p-values for each pair of columns
correlation_values = []
for i, col1 in enumerate(df.columns):
    for j, col2 in enumerate(df.columns):
        if i < j:
            corr_coef, p_value = pearsonr(df[col1], df[col2])
            correlation_values.append([col1, col2, corr_coef, p_value, len(df)-2])

# Create a new DataFrame with the desired columns
correlation_df = pd.DataFrame(correlation_values, columns=['column1', 'column2', 'correlation', 'p_value', 'degrees_of_freedom'])

print(correlation_df)

