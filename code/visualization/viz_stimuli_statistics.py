#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:27:21 2024

@author: Filippo Cerpelloni
"""

import os
import glob
import pathlib as Path
import pandas as pd
import matplotlib.pyplot as plt


def viz_stimuli_statistics(opt):
    
    # Load the necessary files
    # leCorrAvgs = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-letters_variable-linguistic-stats_analysis-correlations_desc-average.csv'))
    # leCorrInds = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-letters_variable-linguistic-stats_analysis-correlations_desc-individual.csv'))
    
    # trTCorrAvgs = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-tested-items-average.csv'))
    # trNTCorrAvgs = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-nontested-items-average.csv'))
    # trTCorrInds = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-tested-items-individual.csv'))
    # trNTCorrInds = pd.read_csv(os.path.join(opt['dir']['results'], 
    #                         'VBT_data-training_variable-linguistic-stats_analysis-correlations_desc-nontested-items-individual.csv'))
    
    # - correlations for test phase
    teCorrAvgs = pd.read_csv(os.path.join(opt['dir']['results'], 
                            'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-average.csv'))
    teCorrInds = pd.read_csv(os.path.join(opt['dir']['results'], 
                            'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-individual.csv'))
    
    
    # Call the plotting function for each of the following correlations:
    # - letters: reading time [r] letter frequency
    #   Nothing is significant, skip for now
    # - assessed training: score, writing time for each session and script [r] length, frequency, old20
    # - training: reading time for each session and script [r] length, frequency, old20
    # - test: score, distance, writing time for each session and script [r] length, frequency, old20
    # leInfo = {'xlab': 'Days of testing', 'ylab': 'Correlation', 'legend position': 'lower right', 
    #           'output name': 'VBT_data-test_variable-accuracy_plot-descriptive.png'}
    # viz_plot_letters_correlations(opt, leCorrInds, leCorrAvgs, leInfo)
    
    teInfo = {'xlab': 'Days of testing', 'ylab': 'Correlation', 'legend position': 'lower right'}
    viz_plot_test_correlations(opt, teCorrAvgs, teInfo)
    
    viz_plot_square_legend(opt)
    
    


### Subfunctions

# Plot correlations across trials
def viz_plot_test_correlations(opt, avgs, params):
        
    # ADD DATA CLOUDS OF INDIVIDUAL DATA

    # Behavioural variables 
    behavioural = set(var.split('_')[0] for var in avgs.column1)

    # Loop through each variable in column 2
    for iC2, col2 in enumerate(avgs.column2.unique()):
        
        # Loop thourugh each variable of column1, without distinction between scripts
        for beh in behavioural:
            
            # Extract the corresponding subset of correlations to plot             
            subset = avgs[(avgs['column1'].str.startswith(beh)) & (avgs['column2'] == col2)]
            
            # Add information over the values plotted
            params['behavioural variable'] = beh
            params['statistic'] = col2
            
            stimuliTypes = ['all', 'real', 'novel', 'seen', 'pseudo']
            
            # For each of them 
            for stim in stimuliTypes:
                
                # Divide the set into the different types of stimuli
                selection = subset[subset['stimuli'] == stim]
                
                # if it exists, plot average correlations 
                if not selection.empty:
                    
                    # Add information over the values plotted
                    params['stimuli'] = stim
                    
                    # Plot the values across sessions
                    viz_plot_correlations(opt, selection, params)
                    
            

def viz_plot_correlations(opt, subset, params):
    
    # Separate data for 'br' and 'cb' scripts
    br = subset[subset['column1'].str.endswith('br')]
    cb = subset[subset['column1'].str.endswith('cb')]
    
    # Define how broad the bar is
    width = 0.2
    
    # Positions for the x-values
    x_pos = subset.session.unique()
    
    # Plot br and cb correlations
    # BR: green
    # CB: orange
    bar1 = plt.bar([pos - width/2 for pos in x_pos], 
                   br['correlation'], color='#69B5A2', width = width, label = 'Braille')
    bar2 = plt.bar([pos + width/2 for pos in x_pos], 
                   cb['correlation'], color='#FF9E4A', width = width, label = 'Connected Braille')

    # Adjust
    # - x axis
    plt.xlabel(params['xlab'])
    plt.xticks([pos for pos in x_pos], subset['session'].unique())

    # - y-axis
    plt.ylabel(params['ylab'])
    
    # - title
    title = 'Correlation between ' + params['behavioural variable'] + ' and ' + params['statistic']
    plt.title(title)

    # Does not work
    # # Add significance stars
    # # Braille
    # for i, (height, p) in enumerate(zip(br['correlation'], br['p_value'])):
        
    #     if p > 0.05:
    #         plt.text(i - width/2, height - 0.5, 'ns', ha = 'center')
    #     elif 0.01 < p <= 0.05:
    #         plt.text(i - width/2, height - 0.5, '*', ha = 'center')
    #     elif 0.001 < p <= 0.01:
    #         plt.text(i - width/2, height - 0.5, '**', ha = 'center')
    #     else:
    #         plt.text(i - width/2, height - 0.5, '***', ha = 'center')
    
    # # Connected Braille 
    # for i, (height, p) in enumerate(zip(cb['correlation'], cb['p_value'])):
        
    #     if p > 0.05:
    #         plt.text(i + width/2, height - 0.5, 'ns', ha = 'center')
    #     elif 0.01 < p <= 0.05:
    #         plt.text(i + width/2, height - 0.5, '*', ha = 'center')
    #     elif 0.001 < p <= 0.01:
    #         plt.text(i + width/2, height - 0.5, '**', ha = 'center')
    #     else:
    #         plt.text(i + width/2, height - 0.5, '***', ha = 'center')
    
    # Save plot
    savename = ('VBT_data-test_variable-' + params['behavioural variable'] + 
                '_stimuli-' + params['stimuli'] + 
                '_plot-correlation-' + params['statistic'] + '.png')
    savepath = os.path.join(opt['dir']['figures'], savename)
    plt.savefig(savepath, dpi = 600)
    
    # Display the plot
    plt.show()
    
    
# Make legend with squares
# Plot a big legend with only dots
def viz_plot_square_legend(opt):
    
    # Create a figure with a specific size
    plt.figure(figsize=(10, 6))  
    
    # Custom legend handles
    legend_handles = [plt.Line2D([], [], marker = 's', color = 'w', markersize = 40, markerfacecolor = '#69B5A2'),
                      plt.Line2D([], [], marker = 's', color = 'w', markersize = 40, markerfacecolor = '#FF9E4A')]
    legend_labels = ['Braille', 'Connected Braille']
    
    
    # Move the legend to the bottom-right corner
    plt.legend(legend_handles, legend_labels, loc = 'best', fontsize = 40, handlelength = .5)
    
    # Hide the axes
    plt.axis('off')
    
    # Save plot
    filename = os.path.join(opt['dir']['figures'], 'VBT_legend-squares.png')
    plt.savefig(filename, dpi = 600, bbox_inches = 'tight')
    
    # Display the plot
    plt.show()
    

