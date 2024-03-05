import os
import pandas as pd

def preproc_merge_and_save(opt, trimmedCsv, trimmedLog, subInfo):
    # SAVE FILES
    # - save each file as a .csv
    # - add current sub's data to the subResults structure

    # Merge files: accuracy and then timing
    trainingTable = pd.concat([trimmedCsv['training'], trimmedLog['training']], axis = 1)
    testTable = pd.concat([trimmedCsv['test'], trimmedLog['test']], axis = 1)

    if subInfo['sesID'] == '002':
        refreshTable = pd.concat([trimmedCsv['refresh'], trimmedLog['refresh']], axis = 1)

    # Get sub info compatible with filename
    subName = f"sub-{subInfo['subID']}"
    sesName = f"ses-{subInfo['sesID']}"
    scriptName = f"script-{subInfo['scriptID']}"

    # Fetch the output directory: if not present, make it
    outputDir = os.path.join(opt['dir']['extracted'], subName, sesName)
    os.makedirs(outputDir, exist_ok = True)

    # Save tables as csv
    trainingTable.to_csv(os.path.join(outputDir, f"{subName}_{sesName}_task-{opt['taskName']}_{scriptName}_beh-training.csv"), 
                          index = False)
    testTable.to_csv(os.path.join(outputDir, f"{subName}_{sesName}_task-{opt['taskName']}_{scriptName}_beh-test.csv"), 
                      index = False)

    # Save refresh table, if present
    if subInfo['sesID'] == '002':
        refreshTable.to_csv(os.path.join(outputDir, f"{subName}_{sesName}_task-{opt['taskName']}_{scriptName}_beh-refresh.csv"), 
                             index = False)
    
    return 
