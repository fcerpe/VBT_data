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
import seaborn as sns
import numpy as np


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
    # leInfo = {'xlab': 'Days of testing', 'ylab': 'Correlation', 'legend position': 'lower right', 
    #           'output name': 'VBT_data-test_variable-accuracy_plot-descriptive.png'}
    # viz_plot_letters_correlations(opt, leCorrInds, leCorrAvgs, leInfo)
    
    # - assessed training: score, writing time for each session and script [r] length, frequency, old20
    # - training: reading time for each session and script [r] length, frequency, old20
    # TBD
    
    # - test: score, distance, writing time for each session and script [r] length, frequency, old20
    teInfo = {'xlab': 'Sessions', 'ylab': 'Correlation', 'legend position': 'lower right'}
    
    # Find files to load
    pattern = 'VBT_data-test_variable-corr-*_analysis-descriptive.csv'
    
    fullPath = os.path.join(opt['dir']['results'], pattern)
    matchingFiles = glob.glob(fullPath)

    for m in matchingFiles:
        
        # Load file
        corr = pd.read_csv(m)
        
        # Plot it
    
    teCorrInds = teCorrInds[(teCorrInds['stimuli'] == 'all') | (teCorrInds['stimuli'] == 'real')]
    teCorrInds.reset_index(inplace = False)
    teCorrGroup = teCorrInds.groupby(['column1', 'column2'])
    
    for (col1, col2), group in teCorrGroup:
        
        # Extract group to plot
        g = group.reset_index(drop = True)
        
        # Adjust information
        stim = g['stimuli'][1]
        title = f"Correlation between {col1} and {col2} for {stim} words"
        variables = f"corr-{col1}-{col2}"
        teInfo = {'variables': variables,
                  'xlab': 'Sessions', 
                  'ylab': 'Correlation', 
                  'title': ''}

        # Plot 
        viz_anova_correlations(opt, g, teInfo)
        


### Subfunctions

# DEPRECATED - Plot correlations across trials
# Correlation of average != average of correlations
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
    y_pos = subset.correlation
    significance = subset.p_value
    
    # Plot br and cb correlations
    # BR: green
    # CB: orange
    bar1 = plt.bar([pos - width/2 for pos in x_pos], 
                   br['correlation'], color='#FF9E4A', width = width, label = 'Braille')
    bar2 = plt.bar([pos + width/2 for pos in x_pos], 
                   cb['correlation'], color='#69B5A2', width = width, label = 'Line Braille')

    # Adjust
    # - x axis
    plt.xlabel(params['xlab'])
    plt.xticks([pos for pos in x_pos], subset['session'].unique())

    # - y-axis
    plt.ylabel(params['ylab'])
    
    # Get the current y-axis limits to add 15% to the y-limit
    # Decide whether to expand upward or downward based on the total sum of bars to plot
    y_min, y_max = plt.ylim()
    margin_max = 0.15 * y_max
    margin_min = 0.15 * y_min
    if sum(y_pos) > 0: 
        plt.ylim(y_min, y_max + margin_max)
        offset = 0.05
        offset_mini = 0.05
    else: 
        plt.ylim(y_min + margin_min, y_max)
        offset = -0.08
        offset_mini = -0.03
    
    # IF CORR IS OPPOSITE SIGN AS TREND, USE 0 INSTEAD OF H
       
    # Assign significanace stars
    for i, (s, h, p) in enumerate(zip(br['session'], br['correlation'], br['p_value'])):
        
        # Determine where to put the asterisks. If correlation is in the opposite trend, put it below/above zero
        if not ((h >= 0 and offset > 0) or (h < 0 and offset < 0)):
            h = 0
            
        if p > 0.05:              plt.text(s - width/2, h + offset_mini, 'ns', ha = 'center', size = 11)
        elif 0.01 < p <= 0.05:    plt.text(s - width/3, h + offset_mini, '*', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
        elif 0.001 < p <= 0.01:   plt.text(s - width/3, h + offset, '**', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
        else:                     plt.text(s - width/3, h + offset, '***', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
    
    for i, (s, h, p) in enumerate(zip(cb['session'], cb['correlation'], cb['p_value'])):
        
        # Determine where to put the asterisks. If correlation is in the opposite trend, put it below/above zero
        if not ((h >= 0 and offset > 0) or (h < 0 and offset < 0)):
            h = 0
            
        if p > 0.05:              plt.text(s + width/2, h + offset_mini, 'ns', ha = 'center', size = 11)
        elif 0.01 < p <= 0.05:    plt.text(s + 2*width/3, h + offset_mini, '*', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
        elif 0.001 < p <= 0.01:   plt.text(s + 2*width/3, h + offset, '**', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
        else:                     plt.text(s + 2*width/3, h + offset, '***', ha = 'center', rotation = 'vertical', weight = 'bold', size = 11)
    

    # - title
    title = 'Correlation between ' + params['behavioural variable'] + ' and ' + params['statistic']
    plt.title(title)
    
    # Save plot
    savename = ('VBT_data-test_variable-' + params['behavioural variable'] + 
                '_stimuli-' + params['stimuli'] + 
                '_plot-correlation-' + params['statistic'] + '.png')
    savepath = os.path.join(opt['dir']['figures'], savename)
    plt.savefig(savepath, dpi = 600)
    
    # Display the plot
    plt.show()
    
    

# Plot the results of the rmANOVAs on individual correlations 
def viz_anova_correlations(opt, subset, params):

    # Custom colors and ofsets
    custom_palette = {
        'br': '#FF9E4A', # CPP Orange
        'cb': '#69B5A2'  # CPP Green
    }
    dodge_val = 0.2
    jitter_val = 0.1

    # Average and SD bars
    point_plot = sns.pointplot(x = 'session', 
                       y = 'correlation', 
                       hue = 'script', 
                       data = subset, 
                       dodge = dodge_val, 
                       markers = 'o', 
                       capsize = 0, 
                       palette = custom_palette,
                       markersize = 12, linewidth = 4,
                       errorbar = 'sd',
                       legend = False,
                       zorder = 2)

    # Individual data points
    strip_plot = sns.stripplot(x = 'session', 
                      y = 'correlation', 
                      hue = 'script', 
                      data = subset, 
                      dodge = dodge_val, 
                      jitter = jitter_val, 
                      alpha = 0.4, 
                      palette = custom_palette,
                      legend = False,
                      zorder = 1)


    # Adjust dodge by separating the hues manually
    for i, artist in enumerate(strip_plot.collections):
        if i % 4 == 0:  # First condition
            artist.set_offsets(artist.get_offsets() - np.array([-0.12, 0]))
        elif i % 4 == 1:  # Second condition
            artist.set_offsets(artist.get_offsets() - np.array([0.12, 0]))
        elif i % 4 == 2:  # Third condition
            artist.set_offsets(artist.get_offsets() - np.array([-0.12, 0]))
        elif i % 4 == 3:  # Fourth condition
            artist.set_offsets(artist.get_offsets() - np.array([0.12, 0]))


    # Customize plot
    plt.xticks(ha='right', fontname = 'Avenir', fontsize = 12)
    plt.yticks(fontname = 'Avenir', fontsize = 12)
    plt.axhline(0, color = 'black', linestyle = '-')
    plt.xlabel(params['xlab'], fontname = 'Avenir', fontsize = 16)
    plt.ylabel(params['ylab'], fontname = 'Avenir', fontsize = 16)
    plt.title(params['title'])
    
    # Save plot
    savename = ('VBT_data-test_variable-' + params['variables'] + 
                '_stimuli-' + subset['stimuli'][0] + 
                '_plot-rmANOVA.png')
    savepath = os.path.join(opt['dir']['figures'], savename)
    plt.savefig(savepath, dpi = 600)

    # Show plot
    plt.show()


    
# Make legend with squares
# Plot a big legend with only squares
def viz_plot_square_legend(opt):
    
    # Create a figure with a specific size
    plt.figure(figsize=(10, 6))  
    
    # Custom legend handles
    legend_handles = [plt.Line2D([], [], marker = 's', color = 'w', markersize = 40, markerfacecolor = '#FF9E4A'),
                      plt.Line2D([], [], marker = 's', color = 'w', markersize = 40, markerfacecolor = '#69B5A2')]
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
    

    
    