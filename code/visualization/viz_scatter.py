#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 10:26:25 2024

@author: cerpelloni
"""

import os
import glob
import pathlib as Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def viz_scatter(opt):
    
    # Read tables
    results = pd.read_csv('../../outputs/derivatives/stats/datasets/VBT_stimuli-test_desc-behavioural-results.csv')
    stats = pd.read_csv('../../outputs/derivatives/stats/datasets/VBT_stimuli-test_desc-list-with-stats.csv')
    
    # Skim datasets 
    results = results[['subject','script','session','woord','writingTime']]
    stats = stats[['woord','session','stimulus','old20']]
    merged = pd.merge(results, stats, on = 'woord', how = 'inner')
    
    merged = merged[merged['stimulus'] != 'pseudo']
    merged = merged[['subject','script','session_x','woord','writingTime','old20']]

    
    
    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    
    # Define the marker shapes for each session
    markers = {1: 'o', 2: 's', 3: 'D', 4: '^'}
    
    custom_palette = ['#69B5A2', '#FF9E4A']
    
    # Plotting each session separately to use different markers
    for session, marker in markers.items():
        subset = merged[merged['session_x'] == session]
        sns.scatterplot(data = subset, 
                        x = 'writingTime', 
                        y = 'old20', 
                        hue = 'script', 
                        style = 'session_x', 
                        markers = {session: marker}, s = 10, palette = custom_palette, legend = 'full', facecolor = 'none')
    
    # Customizing the plot
    plt.title('Scatter Plot of Writing Time vs. Old20')
    plt.xlabel('Writing Time')
    plt.ylabel('Old20')
    plt.legend(title='Script and Session')
    
    # Save plot
    savename = ('VBT_data-test_variables-writing-old20_session-all_plot-scatter.png')
    savepath = os.path.join(opt['dir']['figures'], savename)
    plt.savefig(savepath, dpi = 600)
    
    # Display the plot
    plt.show()
    
    
    
    # Single sessions
    # Loop through each session and create a separate plot
    for session in sorted(merged['session_x'].unique()):
        subset = merged[merged['session_x'] == session]
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data = subset, 
                        x = 'writingTime', 
                        y = 'old20', 
                        hue = 'script', 
                        style = 'session_x',
                        markers = markers, s = 100, palette = custom_palette, 
                        legend = 'auto', 
                        edgecolor = 'w', 
                        linewidth = 1.5, 
                        facecolors = 'none')
        
        # Regression lines for each script
        for script in subset['script'].unique():
            script_subset = subset[subset['script'] == script]
            sns.regplot(data=script_subset, x='writingTime', y='old20', scatter=False, label=script, ci=None)

        
        plt.title(f'Session {session}')
        plt.xlabel('Writing Time')
        plt.ylabel('Old20')
        plt.legend(title='Script')
        plt.show()
    
    