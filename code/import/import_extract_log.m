function trimmed = clean_import_log(filename, session)
% Structure of log file:
% - timing
% - type of event
% - description / action performed

opts = specifyImportParameters();

% Import the data
imported = readtable(filename, opts);

% Manipulate the table to get organized data
trimmed = struct;
trimmed.raw = imported;

% Trim based on the session: different training sessions and routine across
% the experiment
switch session

    case '001'
        % Extract necessary chunks of files
        [trainingEvents, testEvents] = trimEvents(imported, session); 
        
        % Compute timings and assign them to the final variable
        trimmed.training = extractLettersTimings(trainingEvents);
        trimmed.test = extractTestTimings(testEvents);
       
    case '002'
        % Extract necessary chunks of files
        [trainingEvents, testEvents, refreshEvents] = trimEvents(imported, session);

        % Compute timings and assign them to the final variable
        trimmed.refresh = extractLettersTimings(refreshEvents);
        trimmed.training = extractTrainingTimings(trainingEvents);
        trimmed.test = extractTestTimings(testEvents);

    case {'003','004'}
        % Extract necessary chunks of files
        [trainingEvents, testEvents] = trimEvents(imported, session);

        % Compute timings and assign them to the final variable
        trimmed.training = extractTrainingTimings(trainingEvents);
        trimmed.test = extractTestTimings(testEvents);

end

end



%% Subfunctions

function opts = specifyImportParameters()

dataLines = [2 Inf];

opts = delimitedTextImportOptions("NumVariables", 3);
opts.DataLines = dataLines;
opts.Delimiter = "\t";
opts.VariableNames = ["Timing", "EVENT", "Description"];
opts.VariableTypes = ["double", "string", "string"];
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";
opts = setvaropts(opts, "Description", "WhitespaceRule", "preserve");
opts = setvaropts(opts, ["EVENT", "Description"], "EmptyFieldRule", "auto");
opts = setvaropts(opts, "Timing", "ThousandsSeparator", ",");

end

function list = recordKeyboardEvents(events)

list = {};

for ev = 1:size(events,1)
    % Extract the key without the event
    descSplit = strsplit(char(events(ev)), 'Keydown: ');
    key = descSplit{2};

    % Add the key pressed to the list, if not a "solution" character
    if ~strcmp(key, 'ArrowDown')
        list = cat(2, list, key);
    end
end

end

function [tra, tes, ref] = trimEvents(tableIn, session)

% Events of interest are general, regardless the session.
% Important points:
% which letters appear and when 
% when the mouse is pressed
% when words (dis)appear
% When it's required a written answer
% which keys are pressed
% when instructions (dis)appear
events = ["dutch_letter: text", ...
    "dutch_letter: autoDraw", ...
    "dutch_word: text", ...
    "dutch_word: autoDraw = true", ...
    "test_word: autoDraw", ...
    "braille_word: autoDraw", ...
    "word_rsp: editable = true", ...
    "Keydown:", ...
    "Mouse: ", ...
    "refresh_text: autoDraw = null", ...
    "train_text: autoDraw = null", ...
    "trainInstr_text: autoDraw = null", ...
    "testInstr_text: autoDraw = null"];

% Trim events
trimmedEvents = tableIn(startsWith(tableIn.Description, events), [1,3]);

% Split between training and test events

% In session 001, variable name is different
% (Coding mistake, sorry)
if strcmp(session, '001')
    trainingStartIndex = find(strcmp(trimmedEvents.Description, "train_text: autoDraw = null"));
else
    trainingStartIndex = find(strcmp(trimmedEvents.Description, "trainInstr_text: autoDraw = null"));
end

% In session 002, there is also a refresh routine to consider
if strcmp(session, '002')

    % Find indexes
    refreshStartIndex = find(strcmp(trimmedEvents.Description, "refresh_text: autoDraw = null"));
    % Trim
    ref = trimmedEvents(refreshStartIndex:trainingStartIndex-1, :);
end

% Test is the same to evey session
testStartIndex = find(strcmp(trimmedEvents.Description, "testInstr_text: autoDraw = null"));

% Trim events
tra = trimmedEvents(trainingStartIndex:testStartIndex, :);
tes = trimmedEvents(testStartIndex:end, :);

end

function tableOut = extractLettersTimings(tableIn)
% Letters set: further skim the list to keep only three events:
% - dutch letter is chosen, new symbol appears
% - ducth letter is presented, solution appears
% - dutch letter disappears, next trial
tableIn = tableIn(startsWith(tableIn.Description, "dutch"), :);

% Initialize table to contain letters training
tableOut = table('Size', [size(tableIn,1)/3 3], ...
    'VariableTypes', {'char', 'double', 'double'}, ...
    'VariableNames', {'letter', 'readingTime', 'checkingTime'});

% Initialize training index to assign timings
iT = 1;

% Skip through the training events and get information for the
% training log. Goes by steps of 3 because there is no irrelaevant
% information. For each triplet:
% - take which letter was presented by 1st element
% - time2 - time1 is reading time
% - time3 - time2 is checking time
for iL = 1:3:size(tableIn,1)

    letterEvent = char(tableIn.Description{iL});
    tableOut.letter{iT} = letterEvent(end);
    tableOut.readingTime(iT) = tableIn.Timing(iL+1) - tableIn.Timing(iL);
    tableOut.checkingTime(iT) = tableIn.Timing(iL+2) - tableIn.Timing(iL+1);

    iT = iT+1;
end

end

function tableOut = extractTestTimings(tableIn)
% Test set: initialize table to contain letters training
tableOut = table('Size', [60 4], ...
    'VariableTypes', {'double', 'double', 'double', 'cell'}, ...
    'VariableNames', {'word', 'readingTime', 'writingTime', 'attempts'});

% Skip through the test events and get information for the
% log. Events follow the pattern:
% - "autoDraw = true" event, test word appears
% - "autoDraw = null" event, test word disappears
% - "mouse" event, trial ends

% Extract order of events, to facilitate loop
appearenceIdx = find(startsWith(tableIn.Description, "t") & endsWith(tableIn.Description, "e"));
disappearenceIdx = find(startsWith(tableIn.Description, "t") & endsWith(tableIn.Description, "l"));
mouseIdx = find(startsWith(tableIn.Description, "M"));
keywordIdx = find(startsWith(tableIn.Description, "K"));

% "Draw = true" events represent number of the trials
for iEv = 1:size(appearenceIdx,1)

    % Create a window in which to check for events. If it's the
    % last iteration, window stops at the end of the logs
    if iEv <= size(appearenceIdx,1)-1
        range = appearenceIdx(iEv):appearenceIdx(iEv+1);
    else
        range = appearenceIdx(iEv):size(tableIn,1);
    end

    % Where does the word presentation start?
    trial = appearenceIdx(iEv);

    % Where does the presentation end?
    % Intersect events and range
    word = min(intersect(disappearenceIdx, range));

    % Where does the answer stop? Find the last "Mouse" event
    mouse = max(intersect(mouseIdx, range));

    % Which keys were pressed during the answer?
    keys = intersect(keywordIdx, range);
    whichKeys = tableIn{keys,"Description"};

    % Additional analysis: deal with "Keydown" events
    keys = recordKeyboardEvents(whichKeys);

    % Add everything to the testLog
    % Which word is not present in the log file, will come later
    tableOut.word(iEv) = iEv;
    tableOut.readingTime(iEv) = tableIn{word,"Timing"} - tableIn{trial,"Timing"};
    tableOut.writingTime(iEv) = tableIn{mouse,"Timing"} - tableIn{word,"Timing"};
    tableOut.attempts{iEv} = [keys];
end

end

function tableOut = extractTrainingTimings(tableIn)
% Training set: initialize the log table
tableOut = table('Size', [200 6], ...
    'VariableTypes', {'char', 'double', 'double', 'double', 'double', 'cell'}, ...
    'VariableNames', {'word', 'readingTime', 'checkingTime', 'tested', 'writingTime', 'attempts'});

% Extract order of relevant events, to facilitate loop
textIdx = find(startsWith(tableIn.Description, "dutch_word: text"));
appearenceIdx = find(strcmp(tableIn.Description, "braille_word: autoDraw = true"));
disappearenceIdx = find(strcmp(tableIn.Description, "braille_word: autoDraw = null"));
solutionIdx = find(strcmp(tableIn.Description, "dutch_word: autoDraw = true"));
mouseIdx = find(startsWith(tableIn.Description, "Mouse"));
keywordIdx = find(startsWith(tableIn.Description, "Keyword"));
answerIdx = find(strcmp(tableIn.Description, "word_rsp: editable = true"));

% text events represent number of the trials
for iTx = 1:size(textIdx,1)

    % Create a window in which to check for events. If it's the
    % last iteration, window stops at the end of the logs
    if iTx <= size(textIdx,1)-1
        range = textIdx(iTx):textIdx(iTx+1);
    else
        range = textIdx(iTx):size(tableIn,1);
    end

    % Where does the word presentation start?
    wordAppears = tableIn{appearenceIdx(iTx),"Timing"};

    % When is the solution displayed?
    solutionAppears = tableIn{solutionIdx(iTx),"Timing"};

    % Where does the presentation end?
    wordDisappears = tableIn{disappearenceIdx(iTx),"Timing"};

    % Which word was presented?
    whichWord = tableIn{textIdx(iTx), "Description"};
    splitEvent = strsplit(whichWord, ' = ');
    whichWord = splitEvent{2};

    % Does it require a written answer?
    if intersect(answerIdx, range)

        % Which keys were pressed during the answer?
        keys = intersect(keywordIdx, range);
        whichKeys = tableIn{keys,"Description"};

        % Additional analysis: deal with "Keydown" events
        keys = recordKeyboardEvents(whichKeys);

        % Add everything to the training log
        tableOut.word{iTx} = whichWord;
        tableOut.readingTime(iTx) = NaN;
        tableOut.checkingTime(iTx) = wordDisappears - solutionAppears;
        tableOut.tested(iTx) = 1;
        tableOut.writingTime(iTx) = solutionAppears - wordAppears;
        tableOut.attempts{iTx} = [keys];

    else
        % Add everything to the training log
        tableOut.word{iTx} = whichWord;
        tableOut.readingTime(iTx) = solutionAppears - wordAppears;
        tableOut.checkingTime(iTx) = wordDisappears - solutionAppears;
        tableOut.tested(iTx) = 0;
        tableOut.writingTime(iTx) = NaN;
        tableOut.attempts{iTx} = [];

    end
end

end

