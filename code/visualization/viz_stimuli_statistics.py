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
    # - correlations for test phase
    teCorrAvgs = pd.read_csv(os.path.join(opt['dir']['results'], 
                            'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-average.csv'))
    teCorrInds = pd.read_csv(os.path.join(opt['dir']['results'], 
                            'VBT_data-test_variable-linguistic-stats_analysis-correlations_desc-individual.csv'))
    
    teCorrInds = teCorrInds[(teCorrInds['stimuli'] == 'all') | (teCorrInds['stimuli'] == 'real')]
    teCorrInds.reset_index(inplace = False)
    teCorrGroup = teCorrInds.groupby(['column1', 'column2'])
    
    for (col1, col2), group in teCorrGroup:
        
        # Extract group to plot
        g = group.reset_index(drop = True)
        
        # Adjust information
        stim = g['stimuli'][1]
        variables = f"corr-{col1}-{col2}_stimuli-{stim}"
        teInfo = {'output name': f'VBT_data-test_variable-{variables}_plot-rmANOVA.png',
                  'xlab': 'Sessions', 
                  'ylab': 'Correlation', 
                  'title': '',
                  'var_name': 'correlation'}

        # Plot 
        viz_plot_anova(opt, g, teInfo)
        


### Subfunctions

# Plot the results of the rmANOVAs on individual correlations 
def viz_plot_anova(opt, subset, params):

    # Custom colors and ofsets
    custom_palette = {
        'br': '#FF9E4A', # CPP Orange
        'cb': '#69B5A2'  # CPP Green
    }
    dodge_val = 0.2
    jitter_val = 0.1

    # Average and SD bars
    point_plot = sns.pointplot(x = 'session', 
                               y = params['var_name'], 
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
                               y = params['var_name'], 
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
    plt.xticks(fontname='Avenir', fontsize=12)
    plt.yticks(np.arange(-0.6, 0.7, 0.2), fontname='Avenir', fontsize=12)
    plt.axhline(0, linewidth = .8, color='black', linestyle='-')
    plt.ylim(-0.6, 0.6)  # Set y-axis limits
    plt.xlabel(params['xlab'], fontname='Avenir', fontsize=16)
    plt.ylabel(params['ylab'], fontname='Avenir', fontsize=16)
    plt.title(params['title'])
    
    # Save plot
    savename = (params['output name'])
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
    

    
    