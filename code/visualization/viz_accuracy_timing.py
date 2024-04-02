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
                  'output name': 'VBT_data-test_variable-accuracy_plot-rmANOVA.png'}
    viz_plot_rmanova(opt, teAccuracy, teAccuInfo)

    teWriteInfo = {'xlab': 'Days of testing', 'ylab': 'Writing time', 'title': 'Writing time during testing', 
                  'output name': 'VBT_data-test_variable-writing-time_plot-rmANOVA.png'}
    viz_plot_rmanova(opt, teWritingTime, teWriteInfo)
    
    trAccuInfo = {'xlab': 'Days of training', 'ylab': 'Accuracy', 'title': 'Accuracy during training assessment', 
                  'output name': 'VBT_data-training_variable-accuracy_plot-rmANOVA.png'}
    viz_plot_rmanova(opt, trAccuracy, trAccuInfo)
    
    trReadInfo = {'xlab': 'Days of traning', 'ylab': 'Reading time', 'title': 'Reading time during training', 
                  'output name': 'VBT_data-training_variable-reading-time_plot-rmANOVA.png'}
    viz_plot_rmanova(opt, trReadingTime, trReadInfo)
    
    # Plot a big legend
    viz_plot_circle_legend(opt)



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
    legend_handles = [plt.Line2D([], [], marker='o', color='w', markersize = 40, markerfacecolor='#69B5A2'),
                      plt.Line2D([], [], marker='o', color='w', markersize = 40, markerfacecolor='#FF9E4A')]
    legend_labels = ['Braille', 'Connected Braille']
    
    
    # Move the legend to the bottom-right corner
    plt.legend(legend_handles, legend_labels, loc = 'best', fontsize = 40, handlelength = .5)
    
    # Hide the axes
    plt.axis('off')
    
    # Save plot
    filename = os.path.join(opt['dir']['figures'], 'VBT_legend-circles.png')
    plt.savefig(filename, dpi = 600, bbox_inches = 'tight')
    
    # Display the plot
    plt.show()
    
    
    
    
    
    
    
    
    
    
    