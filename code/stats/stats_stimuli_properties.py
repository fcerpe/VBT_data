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
import glob as glob


def stats_further_analyses(opt):
    
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
        'checkingTime': 'mean'})
    leAverages = leRepAverages.groupby(['script', 'letter']).agg({
        'readingTime': 'mean', 
        'checkingTime': 'mean'})
    
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
    
    ## Test
    # Average scores, writing time, distance from the correct answer
    teAverages = teResults.groupby(['script', 'session', 'woord']).agg({
        'score': 'mean',
        'writingTime': 'mean',
        'distance': 'mean'
        }).reset_index()
    
    # Separate type of stimulus (no stats for pseudo-words) and groups (BR v. CB)
    
    
    # Correlate averages with language statistics
    # Test: score, writing time, distance (negative) with length, number syllables, frequency
    teCorrStats = teStats[['length', 'syllabels', 'frequency', 'phonemes', 'old20', 'pld30']]  
    teCorrAverages = teAverages[['score', 'writingTime', 'distance']]    
    teCorrelations = teCorrStats.corrwith(teCorrAverages)

    
    
    # Save results
    
    
    
    
