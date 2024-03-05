import pandas as pd

def preproc_extract_log(filename, session):

    # Import the data
    imported = pd.read_table(filename, names=['Timing', 'EVENT', 'Description'])
    
    # Manipulate the table to get organized data
    trimmed = {}
    trimmed['raw'] = imported
    
    # Trim based on the session
    if session == '001':

        # Extract necessary chunks of files
        trainingEvents, testEvents, _ = trim_events(imported, session)
        
        # Compute timings and assign them to the final variable
        trimmed['training'] = extract_letters_timings(trainingEvents)
        trimmed['test'] = extract_test_timings(testEvents)

    elif session == '002':

        # Extract necessary chunks of files
        trainingEvents, testEvents, refreshEvents = trim_events(imported, session)

        # Compute timings and assign them to the final variable
        trimmed['refresh'] = extract_letters_timings(refreshEvents)
        trimmed['training'] = extract_training_timings(trainingEvents)
        trimmed['test'] = extract_test_timings(testEvents)

    elif session in ['003', '004']:

        # Extract necessary chunks of files
        trainingEvents, testEvents, _ = trim_events(imported, session)

        # Compute timings and assign them to the final variable
        trimmed['training'] = extract_training_timings(trainingEvents)
        trimmed['test'] = extract_test_timings(testEvents)
    
    return trimmed


### Subfunctions

def trim_events(tableIn, session):

    # Events of interest
    events = ["dutch_letter: text", 
              "dutch_letter: autoDraw", 
              "dutch_word: text",
              "dutch_word: autoDraw = true", 
              "test_word: autoDraw", 
              "braille_word: autoDraw",
              "word_rsp: editable = true", 
              "Keydown:", "Mouse:", 
              "refresh_text: autoDraw = null",
              "train_text: autoDraw = null", 
              "trainInstr_text: autoDraw = null",
              "testInstr_text: autoDraw = null"]

    # Avoid import issues with NaNs, cast them as string
    tableIn['Description'] = tableIn['Description'].apply(lambda x: str(x) if isinstance(x, float) else x)

    # Trim events
    trimmedEvents = tableIn[tableIn['Description'].str.startswith(tuple(events))][["Timing", "Description"]]

    # Split between training and test events, use indexes to find starts events of:
    # - TRAining
    # - TESt
    # - REFresh
    if session == '001':
        trainingStartIdx = trimmedEvents[trimmedEvents['Description'] == "train_text: autoDraw = null"].index[0]
    else:
        trainingStartIdx = trimmedEvents[trimmedEvents['Description'] == "trainInstr_text: autoDraw = null"].index[0]

    if session == '002':
        refreshStartIdx = trimmedEvents[trimmedEvents['Description'] == "refresh_text: autoDraw = null"].index[0]
        ref = trimmedEvents.loc[refreshStartIdx:trainingStartIdx-1]
    else:
        ref = None

    testStartIdx = trimmedEvents[trimmedEvents['Description'] == "testInstr_text: autoDraw = null"].index[0]

    tra = trimmedEvents.loc[trainingStartIdx:testStartIdx]
    tes = trimmedEvents.loc[testStartIdx:]

    return tra, tes, ref


def extract_letters_timings(tableIn):

    tableIn = tableIn[tableIn['Description'].str.startswith("dutch")]

    # Create new table to store timings
    tableOut = pd.DataFrame(columns = ['letter', 'readingTime', 'checkingTime'])
    idx = 0

    # Move of steps by 3: events are sequential and identify 
    # - which letter is shown to the participant
    # - when the letter appears 
    # - when the letter disappears
    for i in range(0, len(tableIn), 3):
        
        letterEvent = tableIn.iloc[i]['Description']
        tableOut.loc[idx, 'letter'] = letterEvent[-1]
        tableOut.loc[idx, 'readingTime'] = float(tableIn.iloc[i+1]['Timing']) - float(tableIn.iloc[i]['Timing'])
        tableOut.loc[idx, 'checkingTime'] = float(tableIn.iloc[i+2]['Timing']) - float(tableIn.iloc[i+1]['Timing'])
        idx += 1

    return tableOut


def extract_test_timings(tableIn):

    # Initialize DataFrame to contain test timings
    tableOut = pd.DataFrame(columns = ['word', 'readingTime', 'writingTime', 'attempts'])

    # Extract order of events
    # look for [t]est_word autodraw = tru[e]
    appearenceIdx = tableIn[(tableIn['Description'].str.startswith('t')) & 
                              (tableIn['Description'].str.endswith('e'))].index
    
    # Iterate over appearence events
    for iEv, trialStart in enumerate(appearenceIdx):
        
        # Create a time window from one appearance to the next, to record events relative to one word
        if iEv < len(appearenceIdx) - 1:
            rangeEnd = appearenceIdx[iEv + 1]
        else:
            rangeEnd = tableIn.index[-1]

        # Where does the word presentation end? 
        # look for [t]est_word autodraw = nul[l]
        wordEnd = tableIn.loc[trialStart:rangeEnd][tableIn['Description'].str.startswith('t') & 
                                                   tableIn['Description'].str.endswith('l')].index.min()

        # Where does the answer stop?
        # look for [M]ouse
        mouseEvent = tableIn.loc[trialStart:rangeEnd][tableIn['Description'].str.startswith('M')].index.max()

        # Which keys were pressed during the answer?
        # look for [K]eyboard
        keys = tableIn.loc[trialStart:rangeEnd][tableIn['Description'].str.startswith('K')]['Description'].tolist()

        # Add data to the DataFrame
        tableOut.loc[iEv, 'word'] = iEv
        tableOut.loc[iEv, 'readingTime'] = float(tableIn.loc[wordEnd, 'Timing']) - float(tableIn.loc[trialStart, 'Timing'])
        tableOut.loc[iEv, 'writingTime'] = float(tableIn.loc[mouseEvent, 'Timing']) - float(tableIn.loc[wordEnd, 'Timing'])
        tableOut.loc[iEv, 'attempts'] = keys

    return tableOut



def extract_training_timings(tableIn):

    # Training set: initialize the log table
    tableOut = pd.DataFrame(columns = ['word', 'readingTime', 'checkingTime', 'tested', 'writingTime'], 
                            index=range(200))

    # Extract order of relevant events, to facilitate loop
    textIdx = tableIn.index[tableIn['Description'].str.startswith("dutch_word: text")]
    appearenceIdx = tableIn.index[tableIn['Description'] == "braille_word: autoDraw = true"]
    disappearenceIdx = tableIn.index[tableIn['Description'] == "braille_word: autoDraw = null"]
    solutionIdx = tableIn.index[tableIn['Description'] == "dutch_word: autoDraw = true"]
    answerIdx = tableIn.index[tableIn['Description'] == "word_rsp: editable = true"]

    # text events represent number of the trials
    for iTx in range(len(textIdx)):
        
        # Create a window in which to check for events. If it's the
        # last iteration, window stops at the end of the logs
        if iTx <= len(textIdx) - 2:
            evWindow = tableIn.loc[textIdx[iTx]:textIdx[iTx + 1]]
        else:
            evWindow = tableIn.loc[textIdx[iTx]:tableIn.index[-1]]

        # When does the word presentation start?
        wordAppears = float(tableIn.loc[appearenceIdx[iTx], "Timing"])

        # When is the solution displayed?
        solutionAppears = float(tableIn.loc[solutionIdx[iTx], "Timing"])

        # Where does the presentation end?
        wordDisappears = float(tableIn.loc[disappearenceIdx[iTx], "Timing"])

        # Which word was presented?
        whichWord = tableIn.loc[textIdx[iTx], "Description"].split(' = ')[1]

        # Does it require a written answer?
        # i.e. is there an 'answer' event within the window we are processing
        if present_in_events(answerIdx, evWindow):
            
            # Additional analysis: deal with "Keydown" events
            # keys = recordKeyboardEvents(whichKeys)

            # Add everything to the training log
            tableOut.loc[iTx, "word"] = whichWord
            tableOut.loc[iTx, "readingTime"] = None
            tableOut.loc[iTx, "checkingTime"] = wordDisappears - solutionAppears
            tableOut.loc[iTx, "tested"] = 1
            tableOut.loc[iTx, "writingTime"] = solutionAppears - wordAppears

        else:
            # Add everything to the training log
            tableOut.loc[iTx, "word"] = whichWord
            tableOut.loc[iTx, "readingTime"] = solutionAppears - wordAppears
            tableOut.loc[iTx, "checkingTime"] = wordDisappears - solutionAppears
            tableOut.loc[iTx, "tested"] = 0
            tableOut.loc[iTx, "writingTime"] = None

    return tableOut



def present_in_events(listIn, boundaries):
        
    minIdx = min(boundaries.index)
    maxIdx = max(boundaries.index)
    
    return any(minIdx <= num <= maxIdx for num in listIn)
