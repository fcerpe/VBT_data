import pandas as pd

def preproc_extract_csv(filename, session):

    # Import the data
    imported = pd.read_csv(filename)
    
    # Initialize the trimmed structure
    trimmed = {}
    
    # Switch based on session
    if session == '001':

        # Extract necessary columns
        tableToTrim = imported[["ID", "nlLet", "nlWrd", "testResp"]]
        
        # Extract chunks for session '001'
        trimmed['training'] = extract_letters_results(tableToTrim)
        trimmed['test'] = extract_test_results(tableToTrim, session)

    elif session == '002':

        # Extract necessary columns
        tableToTrim = imported[["ID", "nlLet", "nlWrd", "test", "testResp"]]

        # Extract chunks for session '002'
        trimmed['refresh'] = extract_letters_results(tableToTrim)
        trimmed['training'] = extract_training_results(tableToTrim)
        trimmed['test'] = extract_test_results(tableToTrim, session)

    elif session in ['003', '004']:

        # Extract necessary columns
        tableToTrim = imported[["ID", "nlWrd", "test", "testResp"]]

        # Extract chunks for sessions '003' and '004'
        trimmed['training'] = extract_training_results(tableToTrim)
        trimmed['test'] = extract_test_results(tableToTrim, session)
    
    return trimmed




### Subfunctions


def extract_letters_results(tableIn):

    # Training set is defined by the variable nlLet
    # Isolate letters column
    letterColumn = tableIn['nlLet']

    # Find indexes of entries that are actual letters
    letterIdx = -letterColumn.isna()

    # Start and end of letters array defines the refresh set
    tableOut = tableIn.loc[letterIdx, 'nlLet']
    
    # Adjust csv output: from series to dataframe, index starting from 0
    tableOut = pd.DataFrame(tableOut)
    tableOut.reset_index(drop = True, inplace = True)

    return tableOut


def extract_training_results(tableIn):
    
    # Training and test sets are defined by nlWrd variable and the 'test' variable
    # If there is a word and there is a 'test' value, it means we are in a training trial
    # Find indexes of entries that are actual letters and have a 'test' value
    writeIdx = -tableIn['nlWrd'].isna() & -tableIn['test'].isna()

    # Start and end of letters array defines the training set
    tableOut = tableIn.loc[writeIdx, ["nlWrd", "test", "testResp"]]

    # Quickly assign rudimental score to the elements tested
    tableOut['score'] = tableOut['nlWrd'].str.lower() == tableOut['testResp'].str.lower()
    
    # Adjust csv output: from series to dataframe, index starting from 0
    tableOut = pd.DataFrame(tableOut)
    tableOut.reset_index(drop = True, inplace = True)


    return tableOut


def extract_test_results(tableIn, session):

    # Test sets are defined by nlWrd
    wordColumn = tableIn['nlWrd']

    # In session '001', there is no 'test' column
    if session == '001':
        testIdx = -wordColumn.isna()
    else:
        # Find indexes of entries that are actual letters and have NaN 'test' value
        testIdx = -wordColumn.isna() & tableIn['test'].isna()

    # Start and end of letters array defines the test set
    tableOut = tableIn.loc[testIdx, ["nlWrd", "testResp"]]
    
    # Clean the test output
    tableOut['testResp'] = tableOut['testResp'].apply(clean_test_response)
    
    # Quickly assign rudimental score to the elements tested
    tableOut['score'] = tableOut['nlWrd'].str.lower() == tableOut['testResp'].str.lower()
    
    # Adjust csv output: index starting from 0
    tableOut.reset_index(drop = True, inplace = True)
    
    return tableOut


def clean_test_response(answer):

    # Choose allowed characters and numbers
    allowedChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0123456789'
    allowedNums = [ord(c) for c in allowedChar] + [ord("'")]  # Include ASCII for '

    cleanAnswer = ''
    
    # if the answer has been skipped, mark the string as empty
    if isinstance(answer, float):
        answer = ''

    for char in answer:
        if ord(char) in allowedNums:
            cleanAnswer += char

    return cleanAnswer
