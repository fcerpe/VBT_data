#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:03:14 2024

Function will load the results summary generated by stats_summarize_accuracy_timing 
and perform repeated measures ANOVA to test for gorup differences between the 
two scripts learned (Braille v. Connected Braille). 

List of statistics that are performed in this function
- Accuracy: test session * group 
    * descriptive statistics (mean, SD) 
    * rmANOVA 
- Accuracy: training session * group 
    * descriptive statistics (mean, SD) 
    * rmANOVA 
- Time to write the answer in the test: test session * group
    * descriptive statistics (mean, SD) 
    * rmANOVA 
- Time to read during training: training session * group
    * descriptive statistics (mean, SD) 
    * rmANOVA 

@author: cerpelloni
"""

import os
import pandas as pd
import pingouin as pg

def stats_anova_accuracy_timing(opt):
    
    # Load table
    summary = pd.DataFrame()
    summary = pd.read_csv(os.path.join(opt['dir']['stats'], 'VBT_results-accuracy-timing.csv'))
    
    
    # SF: Re-shape table to fit the format required by statsmodels
    testAccuracy = pd.melt(summary, id_vars = ['subject', 'script'], 
                           value_vars = ['ses-1_test-accuracy', 'ses-2_test-accuracy', 'ses-3_test-accuracy', 'ses-4_test-accuracy'],
                           var_name = 'day', 
                           value_name = 'accuracy')

    # Extract day number from 'day' column
    testAccuracy['day'] = testAccuracy['day'].str.extract(r'(\d)').astype(int)

    # Sort the dataframe
    testAccuracy.sort_values(by=['subject', 'script', 'day'], inplace = True)

    
    
    ### Perform ANOVAs on accuracy
    
    ## Test accuracy
    testAccuracyAnova = pg.mixed_anova(dv='accuracy', within = 'day', between = 'script', subject='subject', 
                  data = testAccuracy)
    
    
    # perform ANOVAs in series for all the questions we have
    # print(AnovaRM(data = summary, depvar = 'response', subject = 'patient', within = ['drug']).fit())
    
    # plot ANOVA results
    summary = summary +2
    
    