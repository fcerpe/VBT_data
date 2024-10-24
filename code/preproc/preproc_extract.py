import os
from pathlib import Path
from preproc_extract_csv import preproc_extract_csv  # assuming this function is implemented in a separate file
from preproc_extract_log import preproc_extract_log  # assuming this function is implemented in a separate file
from preproc_merge_and_save import preproc_merge_and_save

def preproc_extract(opt):

    # Extract data from raw
    # For each subject:
    # - extract data from the four different days of training
    # - import each csv and extract the meaningful responses (for accuracy)
    # - import log file and extract timings
    # - save relevant files in /outputs/extracted_data/subID

    # Suppress warnings
    import warnings
    warnings.filterwarnings("ignore")

    # Load folders
    # only those specifying a day of training
    rawFolders = [folder for folder in os.listdir(opt['dir']['input']) if 'day' in folder]

    # Folder by folder, get all the files for a participant and extract the data
    for rw in rawFolders:

        # Notify the user
        print(f"\n\nWorking on script-{rw[0:2]} ses-00{rw[-1]}\n")

        # Get two separate lists, one for response/csv files and one for timing/log files
        csvList = list(Path(os.path.join(opt['dir']['input'], rw)).glob('sub-*.csv'))
        logList = list(Path(os.path.join(opt['dir']['input'], rw)).glob('sub-*.log'))

        # Work on each file
        for cf, lf in zip(csvList, logList):
            currentCsv = str(cf)
            currentLog = str(lf)

            # If filenames do not correspond, stop and notify the user
            if currentCsv[:-4] != currentLog[:-4]:
                raise ValueError("Filenames do not correspond, you are trying to open two different subjects")

            # Extract subject information
            sub = extract_subject_info(currentCsv)

            # Check that data come from a real participant
            if sub['subID'] not in opt['subList']:
                raise ValueError("Participant that is being processed is not on the list. Check inputs folder")

            # Notify the user
            print(f"Extracting sub-{sub['subID']}...")

            # Import csv and clean it based on the day and which files are needed
            trimmedCsv = preproc_extract_csv(currentCsv, sub['sesID'])

            # Import log file and clean it to get the events
            trimmedLog, completionTime = preproc_extract_log(currentLog, sub['sesID'])

            # Save files
            preproc_merge_and_save(opt, trimmedCsv, trimmedLog, completionTime, sub)

    # Notify the user
    print(f"\n\n EXTRACTED ALL THE SUBJECTS \nData can be found in: {opt['dir']['extracted']}")


### Subfunctions

# Extract information from filename
def extract_subject_info(filename):

    subInfo = {}

    # Split filename
    # First we need to make all the elements standard
    separators = filename.maketrans("/", "_")
    modFilename = filename.translate(separators)
    nameParcels = modFilename.split('_')
    
    subInfo['subID'] = nameParcels[-6].split('-')[1]
    subInfo['sesID'] = nameParcels[-5].split('-')[1]
    subInfo['scriptID'] = nameParcels[-3].split('-')[1].lower()

    return subInfo
