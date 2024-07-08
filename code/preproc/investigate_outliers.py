#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:06:28 2024

Standalone script to investigate potential outliers in 
- writing time during test
- reading time during training on words (days 2-3-4)

@author: Filippo Cerpelloni
"""

import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

# Load files 
outWR = pd.read_csv('/Volumes/fcerpe_phd/VBT_data/outputs/derivatives/stats/' + 
                         'VBT_investigation-outliers-writing.csv')
outRD = pd.read_csv('/Volumes/fcerpe_phd/VBT_data/outputs/derivatives/stats/' + 
                         'VBT_investigation-outliers-reading.csv')


# Writing time during test, issue in day 1
outWR = outWR.sort_values(by = outWR.columns[7], ascending = False)

selection = outWR[(outWR['check'] == 0) & ((outWR['writing'] < 1) | (outWR['writing'] > 30)) | 
                  (outWR['breaks'] > 30) | (outWR['writing'] > 60)]
outWR = outWR.drop(selection.index)
