function trimmed = clean_trim_log(imported, session)
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

        % Trim around specific events and their relationship
        % In this session, what is important is: 
        % - which letter appears
        % - mouse presses
        % - letter appears / disappears
        % - word appears / disappears
        % - disappearence of instruction text (to split training and test)
        events = ["dutch_letter: text",         "Mouse: ", ...
                  "dutch_letter: autoDraw",     "test_word: autoDraw", ...
                  "Keydown:", "train_text: autoDraw = null", ...
                  "testInstr_text: autoDraw = null"];

        % Trim events
        experimentEvents = imported(startsWith(imported.Description, events), [1,3]);

        % Split between training and test events
        trainingStartIndex = find(strcmp(experimentEvents.Description, "train_text: autoDraw = null"));
        testStartIndex = find(strcmp(experimentEvents.Description, "testInstr_text: autoDraw = null"))+1;

        trainingEvents = experimentEvents(trainingStartIndex:testStartIndex, :);
        testEvents = experimentEvents(testStartIndex:end, :);

        % Training set: further skim the list to keep only three events:
        % - dutch letter is chosen, new symbol appears
        % - ducth letter is presented, solution appears
        % - dutch letter disappears, next trial
        trainingEvents = trainingEvents(startsWith(trainingEvents.Description, "dutch"), :);

        % Initialize table to contain letters training
        trainingLog = table('Size', [size(trainingEvents,1)/3 3], ...
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
        for iL = 1:3:size(trainingEvents,1)

            letterEvent = char(trainingEvents.Description{iL});
            trainingLog.letter{iT} = letterEvent(end);

            trainingLog.readingTime(iT) = trainingEvents.Timing(iL+1) - trainingEvents.Timing(iL);

            trainingLog.checkingTime(iT) = trainingEvents.Timing(iL+2) - trainingEvents.Timing(iL+1);

            iT = iT+1;
        end


        % Test set: initialize table to contain letters training
        testLog = table('Size', [60 4], ...
                        'VariableTypes', {'double', 'double', 'double', 'cell'}, ...
                        'VariableNames', {'word', 'readingTime', 'writingTime', 'attempts'});

        % Skip through the test events and get information for the
        % log. Events follow the pattern:
        % - "autoDraw = true" event, test word appears
        % - "autoDraw = null" event, test word disappears
        % - "mouse" event, trial ends

        % Extract order of events, to facilitate loop
        drawTrueEvents = find(startsWith(testEvents.Description, "t") & endsWith(testEvents.Description, "e"));
        drawNullEvents = find(startsWith(testEvents.Description, "t") & endsWith(testEvents.Description, "l"));
        mouseEvents = find(startsWith(testEvents.Description, "M"));
        keywordEvents = find(startsWith(testEvents.Description, "K"));

        % "Draw = true" events represent number of the trials
        for iEv = 1:size(drawTrueEvents,1)

            % Create a window in which to check for events. If it's the
            % last iteration, window stops at the end of the logs
            if iEv <= size(drawTrueEvents,1)-1
                range = drawTrueEvents(iEv):drawTrueEvents(iEv+1);
            else
                range = drawTrueEvents(iEv):size(testEvetns,1);
            end

            % Where does the word presentation start?
            trial = drawTrueEvents(iEv);

            % Where does the presentation end?
            % Intersect events and range 
            word = min(intersect(drawNullEvents, range));

            % Where does the answer stop? Find the last "Mouse" event
            mouse = max(intersect(mouseEvents, range));

            % Which keys were pressed during the answer? 
            keys = intersect(keywordEvents, range);
            whichKeys = testEvents{keys,"Description"};

            % Additional analysis: deal with "Keydown" events
            keys = recordKeydownEvents(whichKeys);
            
            
            % Add everything to the testLog 
            % Which word is not present in the log file, will come later
            testLog.word(iEv) = iEv;
            testLog.readingTime(iEv) = testEvents{word,"Timing"} - testEvents{trial,"Timing"};
            testLog.writingTime(iEv) = testEvents{mouse,"Timing"} - testEvents{word,"Timing"};
            testLog.attempts{iEv} = [keys];
        end

        % Assign variables to final struct
        trimmed.training = trainingLog;
        trimmed.test = testLog;



    case '002'

        %% Extract the necessary columns

        % Trim around specific events and their relationship
        % In this session, what is important is: 
        % - which letter appears
        % - mouse presses
        % - letter appears / disappears
        % - word appears / disappears
        % - disappearence of instruction text (to split training and test)
        events = ["dutch_letter: text",         "Mouse: ", ...
                  "dutch_letter: autoDraw",     "test_word: autoDraw", ...
                  "Keydown:", "train_text: autoDraw = null", ...
                  "testInstr_text: autoDraw = null"];

        % Trim events
        experimentEvents = imported(startsWith(imported.Description, events), [1,3]);

        % Split between training and test events
        trainingStartIndex = find(strcmp(experimentEvents.Description, "train_text: autoDraw = null"));
        testStartIndex = find(strcmp(experimentEvents.Description, "testInstr_text: autoDraw = null"))+1;

        trainingEvents = experimentEvents(trainingStartIndex:testStartIndex, :);
        testEvents = experimentEvents(testStartIndex:end, :);

        % Training set: further skim the list to keep only three events:
        % - dutch letter is chosen, new symbol appears
        % - ducth letter is presented, solution appears
        % - dutch letter disappears, next trial
        trainingEvents = trainingEvents(startsWith(trainingEvents.Description, "dutch"), :);

        % Initialize table to contain letters training
        trainingLog = table('Size', [size(trainingEvents,1)/3 3], ...
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
        for iL = 1:3:size(trainingEvents,1)

            letterEvent = char(trainingEvents.Description{iL});
            trainingLog.letter{iT} = letterEvent(end);

            trainingLog.readingTime(iT) = trainingEvents.Timing(iL+1) - trainingEvents.Timing(iL);

            trainingLog.checkingTime(iT) = trainingEvents.Timing(iL+2) - trainingEvents.Timing(iL+1);

            iT = iT+1;
        end


        % Test set: initialize table to contain letters training
        testLog = table('Size', [60 4], ...
                        'VariableTypes', {'double', 'double', 'double', 'cell'}, ...
                        'VariableNames', {'word', 'readingTime', 'writingTime', 'attempts'});

        % Skip through the test events and get information for the
        % log. Events follow the pattern:
        % - "autoDraw = true" event, test word appears
        % - "autoDraw = null" event, test word disappears
        % - "mouse" event, trial ends

        % Extract order of events, to facilitate loop
        drawTrueEvents = find(startsWith(testEvents.Description, "t") & endsWith(testEvents.Description, "e"));
        drawNullEvents = find(startsWith(testEvents.Description, "t") & endsWith(testEvents.Description, "l"));
        mouseEvents = find(startsWith(testEvents.Description, "M"));
        keywordEvents = find(startsWith(testEvents.Description, "K"));

        % "Draw = true" events represent number of the trials
        for iEv = 1:size(drawTrueEvents,1)

            % Create a window in which to check for events. If it's the
            % last iteration, window stops at the end of the logs
            if iEv <= size(drawTrueEvents,1)-1
                range = drawTrueEvents(iEv):drawTrueEvents(iEv+1);
            else
                range = drawTrueEvents(iEv):size(testEvetns,1);
            end

            % Where does the word presentation start?
            trial = drawTrueEvents(iEv);

            % Where does the presentation end?
            % Intersect events and range 
            word = min(intersect(drawNullEvents, range));

            % Where does the answer stop? Find the last "Mouse" event
            mouse = max(intersect(mouseEvents, range));

            % Which keys were pressed during the answer? 
            keys = intersect(keywordEvents, range);
            whichKeys = testEvents{keys,"Description"};

            % Additional analysis: deal with "Keydown" events
            keys = recordKeydownEvents(whichKeys);
            
            
            % Add everything to the testLog 
            % Which word is not present in the log file, will come later
            testLog.word(iEv) = iEv;
            testLog.readingTime(iEv) = testEvents{word,"Timing"} - testEvents{trial,"Timing"};
            testLog.writingTime(iEv) = testEvents{mouse,"Timing"} - testEvents{word,"Timing"};
            testLog.attempts{iEv} = [keys];
        end

        % Assign variables to final struct
        trimmed.training = trainingLog;
        trimmed.test = testLog;



    case {'003','004'}

        
end

end



%% Subfunctions

function list = recordKeydownEvents(events)

list = {};

for ev = 1:size(events,1)

    % Extract the key without the event
    descSplit = strsplit(char(events(ev)), 'Keydown: ');
    key = descSplit{2};

    % Add the key pressed to the list
    list = cat(2, list, key);

end


end