from import_option import import_option
from import_extract import import_extract

### VISUAL BRAILLE TRAINING - IMPORT DATA 
# 
# Main script to extract information from raw data
#
# From inputs data (extracted from Pavlovia), take the subjects that have
# completed the experiment and "preprocess" / clean the results and log
# tables.
#
# © Filippo Cerpelloni


# Get options
opt = import_option()


# Extract data from raw
# For each subject, extract data from the four different days of training
# - import each CSV and extract responses
# - import log file and extract timings
# - save relevant files in /outputs/extracted_data/subID
import_extract(opt)
