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
    trResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                  'VBT_stimuli-training_desc-behavioural-results.csv'))
    teResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'datasets', 
                                  'VBT_stimuli-test_desc-behavioural-results.csv'))
    
    # Load stimuli statistics
    
    # Compute letter-wise averages across repetitions
    
    # Compute word-wise distance averages for test
    
    # Correlate averages with language statistics
    
    # Save results
    
    
    
    
