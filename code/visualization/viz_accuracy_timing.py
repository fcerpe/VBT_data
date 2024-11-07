#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:25:34 2024

@author: cerpelloni
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def viz_accuracy_timing(opt):
    
    # Load the necessary files
    # results from the original data, before rmANOVA
    behResults = pd.read_csv(os.path.join(opt['dir']['stats'], 'VBT_results-accuracy-timing.csv'))
    teAccuStats = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-test_variable-accuracy_analysis-descriptive.csv'))
    teWriteStats = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-test_variable-writing-time_analysis-descriptive.csv'))
    trAccuStats = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-training_variable-accuracy_analysis-descriptive.csv'))
    trReadStats = pd.read_csv(os.path.join(opt['dir']['results'], 'VBT_data-training_variable-reading-time_analysis-descriptive.csv'))
    
    # Re-organize table 
    behResults = rearrange_table(behResults)
    
    # Call the plotting function for each variable
    # - test accuracy
    teAccuInfo = {'xlab': 'Sessions', 
                  'ylab': 'Accuracy (a.u.)', 
                  'title': '', 
                  'var_name': 'test-accuracy',
                  'output name': 'VBT_data-test_variable-accuracy_plot-rmANOVA.png'}
    teAccuracy = behResults[['subject', 'script', 'session', 'test-accuracy']].copy()
    
    viz_plot_rmanova(opt, teAccuracy, teAccuStats, teAccuInfo)

    # - test writing time
    teWriteInfo = {'xlab': 'Sessions', 
                   'ylab': 'Writing time (s)', 
                   'title': '', 
                   'var_name': 'test-writing',
                   'output name': 'VBT_data-test_variable-writing-time_plot-rmANOVA.png'}
    teWritingTime = behResults[['subject', 'script', 'session', 'test-writing']].copy()
    
    viz_plot_rmanova(opt, teWritingTime, teWriteStats, teWriteInfo)
    
    # - training assessment accuracy
    trAccuInfo = {'xlab': 'Sessions',
                  'ylab': 'Accuracy (a.u.)', 
                  'title': '', 
                  'var_name': 'train-accuracy',
                  'output name': 'VBT_data-training_variable-accuracy_plot-rmANOVA.png'}
    trAccuracy = behResults[behResults['session'] != '1'][['subject', 'script', 'session', 'train-accuracy']].copy()
    
    viz_plot_rmanova(opt, trAccuracy, trAccuStats, trAccuInfo)
    
    # - training reading time
    trReadInfo = {'xlab': 'Sessions',
                  'ylab': 'Reading time (s)', 
                  'title': '', 
                  'var_name': 'train-reading',
                  'output name': 'VBT_data-training_variable-reading-time_plot-rmANOVA.png'}
    trReadingTime = behResults[behResults['session'] != '1'][['subject', 'script', 'session', 'train-reading']].copy()
    
    viz_plot_rmanova(opt, trReadingTime, trReadStats, trReadInfo)
    
    # Plot a big legend
    #viz_plot_circle_legend(opt)



### Subfunctions

# Modify the table to have columns like correlations, to centralize plotting scripts
def rearrange_table(tableIn):
    
    tableIn = pd.DataFrame(tableIn)

    # Reshape using melt and then pivot
    tableOut = tableIn.melt(id_vars = ['subject', 'script'], 
                            var_name = 'session_metric', 
                            value_name = 'value')

    # Extract session and metric information
    tableOut[['session', 'metric']] = tableOut['session_metric'].str.extract(r'ses-(\d+)_(.*)')

    # Filter out unwanted variables
    tableOut = tableOut[~tableOut['metric'].isin(['test-reading', 'train-checking', 'ref-reading', 'ref-checking'])]

    # Pivot to have one row per subject per session, with metrics as columns
    tableOut = tableOut.pivot(index = ['subject', 'script', 'session'], 
                              columns = 'metric', 
                              values = 'value').reset_index()
    
    #tableOut['session'] = tableOut['session'].astype(float)
    
    return tableOut 


# Main plotting function for ANOVA results (no data cloud so far)
def viz_plot_rmanova(opt, res, stats, information):

     
    custom_palette = {
        'br': '#FF9E4A', # CPP Orange
        'cb': '#69B5A2'  # CPP Green
    }
    dodge_val = 0.2
    jitter_val = 0.1

    # Average and SD bars
    point_plot = sns.pointplot(x = 'session', 
                               y = information['var_name'], 
                               hue = 'script', 
                               data = res, 
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
                               y = information['var_name'], 
                               hue = 'script', 
                               data = res, 
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
    plt.xticks(fontname = 'Avenir', fontsize = 12)
    plt.yticks(fontname = 'Avenir', fontsize = 12)
    
    # Add axes labels and title
    plt.xlabel(information['xlab'], fontname = "Avenir", fontsize = 16)
    plt.ylabel(information['ylab'], fontname = "Avenir", fontsize = 16)
    plt.title(information['title'])

    # Customize x-axis ticks, accoid half-days
    plt.xticks(res['session'], fontname = "Avenir", fontsize = 12)
    plt.yticks(fontname = "Avenir", fontsize = 12)
    
    # Save plot
    filename = os.path.join(opt['dir']['figures'], information['output name'])
    plt.savefig(filename, dpi = 600)
    
    # Display the plot
    plt.show()
    

# Plot a big legend with only dots
def viz_plot_circle_legend(opt):
    
    # Create a figure with a specific size
    plt.figure(figsize=(10, 6))  
    
    # Custom legend handles
    legend_handles = [plt.Line2D([], [], marker='o', color='w', markersize = 40, markerfacecolor='#FF9E4A'),
                      plt.Line2D([], [], marker='o', color='w', markersize = 40, markerfacecolor='#69B5A2')]
    legend_labels = ['Braille', 'Line Braille']
    
    
    # Move the legend to the bottom-right corner
    plt.legend(legend_handles, legend_labels, loc = 'best', fontsize = 40, handlelength = .5)
    
    # Hide the axes
    plt.axis('off')
    
    # Save plot
    filename = os.path.join(opt['dir']['figures'], 'VBT_legend-circles.png')
    plt.savefig(filename, dpi = 600, bbox_inches = 'tight')
    
    # Display the plot
    plt.show()
    
    
    
    
    
    
    
    
    
    
    