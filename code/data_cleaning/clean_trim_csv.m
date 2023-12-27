function trimmed = clean_trim_csv(imported, session)
% TRIM CSV
%
% Process the CSV file based on the current session to extract response 
% to training and test

% Start buildig the final variable
trimmed = struct;
trimmed.raw = imported;

% Trimming is based on the session
switch session

    case '001'

        %% Extract the necessary columns
        tableToTrim = imported(:,["ID","nlLet","nlWrd","testResp"]);

        % Training set is defined by the variable nlLet
        % Isolate letters column
        letterColumn = [tableToTrim.nlLet];

        % Find indexes of entries that are actual letters, 
        letterIndexes = find(isletter(char(letterColumn)));

        % Start and end of letters array defines the training set
        trainingSet = tableToTrim(letterIndexes(1):letterIndexes(end),"nlLet");


        % Test set is defined by nlWrd variable
        % Isolate words column
        wordColumn = char([tableToTrim.nlWrd]);

        % Find indexes of entries that start with a letter
        wordIndexes = find(isletter(wordColumn(:,1)));

        % Start and end of letters array defines the test set
        testSet = tableToTrim(wordIndexes(1):wordIndexes(end),["nlWrd","testResp"]);

        % Quickly assign rudimental score:
        % 1 if strings match (using lowercase responses)
        % 0 if they don't
        testSet.score = strcmp(testSet.nlWrd, lower(testSet.testResp));


        % Assign variables to final struct
        trimmed.training = trainingSet;
        trimmed.test = testSet;


    case '002'

        %% Extract the necessary columns
        tableToTrim = imported(:,["ID", "nlLet", "nlWrd", "test", "testResp"]);

        % Training set is defined by the variable nlLet
        % Isolate letters column
        letterColumn = [tableToTrim.nlLet];

        % Find indexes of entries that are actual letters
        letterIndexes = find(isletter(char(letterColumn)));

        % Start and end of letters array defines the refresh set
        refreshSet = tableToTrim(letterIndexes(1):letterIndexes(end),"nlLet");


        % Training and test sets are defined by nlWrd variable and the 'test' variable
        % If there is a word and there is a 'test' value, it means we are
        %    in a training trial and the participant is asked (or not) to
        %    write down the answer, to check for attention.
        % If a word is presented but 'test' is NaN, we are in the real test
        wordColumn = char([tableToTrim.nlWrd]);
        writeAnswer = tableToTrim.test;

        % Find indexes of entries that are actual letters
        writeIndexes = find(isletter(wordColumn(:,1)) &  ~isnan(writeAnswer));

        % Start and end of letters array defines the training set
        trainingSet = tableToTrim(writeIndexes(1):writeIndexes(end),["nlWrd", "test", "testResp"]);

        % Quickly assign rudimental score to the elements tested
        % 1 if strings match (using lowercase responses), 0 if they don't
        trainingSet.score = strcmp(trainingSet.nlWrd, lower(trainingSet.testResp));

        % Find indexes of entries that are actual letters
        testIndexes = find(isletter(wordColumn(:,1)) &  isnan(writeAnswer));

        % Start and end of letters array defines the test set
        testSet = tableToTrim(testIndexes(1):testIndexes(end),["nlWrd","testResp"]);

        % Quickly assign rudimental score to the elements tested
        % 1 if strings match (using lowercase responses), 0 if they don't
        testSet.score = strcmp(testSet.nlWrd, lower(testSet.testResp));


        % Assign variables to final struct
        trimmed.refresh = refreshSet;
        trimmed.training = trainingSet;
        trimmed.test = testSet;


    case {'003','004'}

        %% Extract the necessary columns
        tableToTrim = imported(:,["ID", "nlWrd", "test", "testResp"]);

        % Training and test sets are defined by nlWrd variable and the 'test' variable
        % If there is a word and there is a 'test' value, it means we are
        %    in a training trial and the participant is asked (or not) to
        %    write down the answer, to check for attention.
        % If a word is presented but 'test' is NaN, we are in the real test
        wordColumn = char([tableToTrim.nlWrd]);
        writeAnswer = tableToTrim.test;

        % Find indexes of entries that are actual letters
        writeIndexes = find(isletter(wordColumn(:,1)) &  ~isnan(writeAnswer));

        % Start and end of letters array defines the training set
        trainingSet = tableToTrim(writeIndexes(1):writeIndexes(end),["nlWrd", "test", "testResp"]);

        % Quickly assign rudimental score to the elements tested
        % 1 if strings match (using lowercase responses), 0 if they don't
        trainingSet.score = strcmp(trainingSet.nlWrd, lower(trainingSet.testResp));

        % Find indexes of entries that are actual letters
        testIndexes = find(isletter(wordColumn(:,1)) &  isnan(writeAnswer));

        % Start and end of letters array defines the test set
        testSet = tableToTrim(testIndexes(1):testIndexes(end),["nlWrd","testResp"]);

        % Quickly assign rudimental score to the elements tested
        % 1 if strings match (using lowercase responses), 0 if they don't
        testSet.score = strcmp(testSet.nlWrd, lower(testSet.testResp));


        % Assign variables to final struct
        trimmed.training = trainingSet;
        trimmed.test = testSet;

end


end