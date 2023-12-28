function trimmed = import_extract_csv(filename, session)

% Import the data
imported = readtable(filename);

switch session

    case '001'
        % Extract the necessary columns
        tableToTrim = imported(:,["ID", "nlLet", "nlWrd", "testResp"]);
        
        % extract chunks of each part of the experiment and assign them to
        % the final structure
        trimmed.training = extractLettersResults(tableToTrim);
        trimmed.test = extractTestResults(tableToTrim, session);


    case '002'
        % Extract the necessary columns
        tableToTrim = imported(:,["ID", "nlLet", "nlWrd", "test", "testResp"]);

        % extract chunks of each part of the experiment and assign them to
        % the final structure
        trimmed.refresh = extractLettersResults(tableToTrim);
        trimmed.training = extractTrainingResults(tableToTrim);
        trimmed.test = extractTestResults(tableToTrim, session);


    case {'003','004'}
        % Extract the necessary columns
        tableToTrim = imported(:,["ID", "nlWrd", "test", "testResp"]);

        % extract chunks of each part of the experiment and assign them to
        % the final structure
        trimmed.training = extractTrainingResults(tableToTrim);
        trimmed.test = extractTestResults(tableToTrim, session);
end

end



%% Subfunctions

function tableOut = extractLettersResults(tableIn)
% Training set is defined by the variable nlLet
% Isolate letters column
letterColumn = [tableIn.nlLet];

% Find indexes of entries that are actual letters
letterIndexes = find(isletter(char(letterColumn)));

% Start and end of letters array defines the refresh set
tableOut = tableIn(letterIndexes(1):letterIndexes(end),"nlLet");

end

function tableOut = extractTrainingResults(tableIn)
% Training and test sets are defined by nlWrd variable and the 'test' variable
% If there is a word and there is a 'test' value, it means we are
%    in a training trial and the participant is asked (or not) to
%    write down the answer, to check for attention.
% If a word is presented but 'test' is NaN, we are in the real test
wordColumn = char([tableIn.nlWrd]);
writeAnswer = tableIn.test;

% Find indexes of entries that are actual letters
writeIndexes = find(isletter(wordColumn(:,1)) &  ~isnan(writeAnswer));

% Start and end of letters array defines the training set
tableOut = tableIn(writeIndexes(1):writeIndexes(end),["nlWrd", "test", "testResp"]);

% Quickly assign rudimental score to the elements tested
% 1 if strings match (using lowercase responses), 0 if they don't
tableOut.score = strcmp(tableOut.nlWrd, lower(tableOut.testResp));

end

function tableOut = extractTestResults(tableIn, session)
% Test sets are defined by nlWrd
wordColumn = char([tableIn.nlWrd]);

% Find indexes of entries that are actual letters.
% In ses-001, there is no 'test' column, so avoid looking for it
if strcmp(session, '001')
    testIndexes = find(isletter(wordColumn(:,1)));
else
    % If there is a word and there is a 'test' value, it means we are
    %    in a training trial and the participant is asked (or not) to
    %    write down the answer, to check for attention.
    % If a word is presented but 'test' is NaN, we are in the real test
    writeAnswer = tableIn.test;
    testIndexes = find(isletter(wordColumn(:,1)) &  isnan(writeAnswer));
end

% Start and end of letters array defines the test set
tableOut = tableIn(testIndexes(1):testIndexes(end),["nlWrd","testResp"]);

% Quickly assign rudimental score to the elements tested
% 1 if strings match (using lowercase responses), 0 if they don't
tableOut.score = strcmp(tableOut.nlWrd, lower(tableOut.testResp));

end