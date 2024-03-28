#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:25:34 2024

@author: cerpelloni
"""

import os
import glob
import pathlib as Path
import pandas as pd
import matplotlib.pyplot as plt


def viz_accuracy_timing(opt):
    
    # Load the necessary files
    # - descriptive stats related to 'rmanova' analyses
    teAccuracy = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-test_variable-accuracy_analysis-descriptive.csv'))
    teWritingTime = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-test_variable-writing-time_analysis-descriptive.csv'))
    
    trAccuracy = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-training_variable-accuracy_analysis-descriptive.csv'))
    trReadingTime = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-training_variable-reading-time_analysis-descriptive.csv'))

    
    # Call the plotting function for each anova
    # - test accuracy
    # - test writing time
    # - training assessment accuracy
    # - training reading time
    teAccuInfo = {'xlab': 'Days of testing', 'ylab': 'Accuracy', 'title': 'Accuracy during testing', 
                  'legend position': 'lower right', 'output name': 'VBT_data-test_variable-accuracy_plot-descriptive.png'}
    viz_plot_rmanova(opt, teAccuracy, teAccuInfo)

    teWriteInfo = {'xlab': 'Days of testing', 'ylab': 'Writing time', 'title': 'Writing time during testing', 
                  'legend position': 'lower right', 'output name': 'VBT_data-test_variable-writing-time_plot-descriptive.png'}
    viz_plot_rmanova(opt, teWritingTime, teWriteInfo)
    
    trAccuInfo = {'xlab': 'Days of training', 'ylab': 'Accuracy', 'title': 'Accuracy during training assessment', 
                  'legend position': 'lower right', 'output name': 'VBT_data-training_variable-accuracy_plot-descriptive.png'}
    viz_plot_rmanova(opt, trAccuracy, trAccuInfo)
    
    trReadInfo = {'xlab': 'Days of traning', 'ylab': 'Reading time', 'title': 'Reading time during training', 
                  'legend position': 'lower right', 'output name': 'VBT_data-training_variable-reading-time_plot-descriptive.png'}
    viz_plot_rmanova(opt, trReadingTime, trReadInfo)



### Subfunctions

# Main plotting function for ANOVA results (no data cloud so far)
def viz_plot_rmanova(opt, res, information):

    # ADD DATA CLOUDS OF INDIVIDUAL DATA
    # I MAY NOT EVEN HAVE THOSE TABLES    

    # Separate data for 'br' and 'cb' scripts
    br = res[res['script'] == 'br']
    cb = res[res['script'] == 'cb']
    
    # Define a small offset to avoid overlap between error bars
    offset = 0.05

    # Plot br and cb perfromances
    # BR: green
    # CB: orange
    # Errorbars: standard deviation
    plt.errorbar(br['day'] - offset, br['mean'], yerr = br['std'], label = 'br', fmt = '-o', color = '#69B5A2')
    plt.errorbar(cb['day'] + offset, cb['mean'], yerr = cb['std'], label = 'cb', fmt = '-o', color = '#FF9E4A')
    
    # Add axes labels and title
    plt.xlabel(information['xlab'])
    plt.ylabel(information['ylab'])
    plt.title(information['title'])

    # Customize x-axis ticks, accoid half-days
    plt.xticks(res['day'].unique())
    
    # Move the legend to the bottom-right corner
    plt.legend(loc = information['legend position'])
    
    # Save plot
    filename = os.path.join(opt['dir']['figures'], information['output name'])
    plt.savefig(filename, dpi = 600)
    
    # Display the plot
    plt.show()