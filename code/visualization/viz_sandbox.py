#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:30:07 2024

@author: cerpelloni
"""

import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 35, 45, 30],
        'City': ['New York', 'Paris', 'London', 'Tokyo']}
df = pd.DataFrame(data)

# Plot DataFrame as a table
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

# Save as PNG
plt.savefig('dataframe_table.png', bbox_inches='tight')
plt.close()
