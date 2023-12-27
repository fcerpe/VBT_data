function trimmed = clean_import_csv(filename)
% Auto-generated by MATLAB on 27-Dec-2023 13:59:42
% Adapted to multiple csv files by Filippo Cerpelloni

% dataLines is not specified, define defaults
dataLines = [2, Inf];


%% Set up the Import Options and import the data
% Based on day of training
% Different days have different routines and therefore a different number
% of variables

% Extract session from filename
nameParcels = strsplit(filename, {'_','-','/'});

% Find position of 'ses' and pick values just after it
sesPosition = find(strcmp(nameParcels,'ses') == 1);
session = nameParcels{sesPosition +1};

% Load options based on the session
switch session

    % Day 1: training on letters but not on words, so no checks 
    case '001'
        opts = delimitedTextImportOptions("NumVariables", 69, "Encoding", "UTF-8");
        opts.DataLines = dataLines;
        opts.Delimiter = ",";
        opts.VariableNames = ["welcome_mousex", "welcome_mousey", "welcome_mouseleftButton", ...
            "welcome_mousemidButton", "welcome_mouserightButton", "welcome_mousetime", "ID", "date", ...
            "expName", "psychopyVersion", "OS", "frameRate", "mouse_2x", "mouse_2y", "mouse_2leftButton", ...
            "mouse_2midButton", "mouse_2rightButton", "mouse_2time", "mouse_3x", "mouse_3y", ...
            "mouse_3leftButton", "mouse_3midButton", "mouse_3rightButton", "mouse_3time", "train_mousex", ...
            "train_mousey", "train_mouseleftButton", "train_mousemidButton", "train_mouserightButton", ...
            "train_mousetime", "braille_mousex", "braille_mousey", "braille_mouseleftButton", ...
            "braille_mousemidButton", "braille_mouserightButton", "braille_mousetime", "trialsthisRepN",...
            "trialsthisTrialN", "trialsthisN", "trialsthisIndex", "trialsran", "nlLet", "brLet", ...
            "cbLet", "mousex", "mousey", "mouseleftButton", "mousemidButton", "mouserightButton", ...
            "testInstr_mousex", "testInstr_mousey", "testInstr_mouseleftButton", "testInstr_mousemidButton", ...
            "testInstr_mouserightButton", "test_mousex", "test_mousey", "test_mouseleftButton", ...
            "test_mousemidButton", "test_mouserightButton", "test_responsetext", "testResp", ...
            "test_loopthisRepN", "test_loopthisTrialN", "test_loopthisN", "test_loopthisIndex", ...
            "test_loopran", "nlWrd", "brWrd", "cbWrd"];
        opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", "string", ...
            "string", "string", "string", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "string", "string", "string", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "string", "string", "double", "double", "double", ...
            "double", "double", "string", "string", "string"];
        opts.ExtraColumnsRule = "ignore";
        opts.EmptyLineRule = "read";
        opts = setvaropts(opts, ["test_responsetext", "testResp", "nlWrd", "brWrd", "cbWrd"], ...
                                "WhitespaceRule", "preserve");
        opts = setvaropts(opts, ["date", "expName", "psychopyVersion", "OS", "nlLet", "brLet", "cbLet", ...
                                "test_responsetext", "testResp", "nlWrd", "brWrd", "cbWrd"], "EmptyFieldRule", "auto");

    % Day 2: training on letters and words
    case '002'
        opts = delimitedTextImportOptions("NumVariables", 79, "Encoding", "UTF-8");
        opts.DataLines = dataLines;
        opts.Delimiter = ",";
        opts.VariableNames = ["welcome_mousex", "welcome_mousey", "welcome_mouseleftButton", ...
            "welcome_mousemidButton", "welcome_mouserightButton", "welcome_mousetime", "ID", "date", ...
            "expName", "psychopyVersion", "OS", "frameRate", "refresh_mousex", "refresh_mousey", ...
            "refresh_mouseleftButton", "refresh_mousemidButton", "refresh_mouserightButton", ...
            "refresh_mousetime", "braille_mousex", "braille_mousey", "braille_mouseleftButton", ...
            "braille_mousemidButton", "braille_mouserightButton", "braille_mousetime", "trialsthisRepN", ...
            "trialsthisTrialN", "trialsthisN", "trialsthisIndex", "trialsran", "nlLet", "brLet", "cbLet", ...
            "trainInstr_mousex", "trainInstr_mousey", "trainInstr_mouseleftButton", "trainInstr_mousemidButton", ...
            "trainInstr_mouserightButton", "trainInstr_mousetime", "translation_keykeys", "translation_keycorr", ...
            "translation_keyrt", "word_rsptext", "word_mousex", "word_mousey", "word_mouseleftButton", ...
            "word_mousemidButton", "word_mouserightButton", "word_mousetime", "train_loopthisRepN", ...
            "train_loopthisTrialN", "train_loopthisN", "train_loopthisIndex", "train_loopran", "nlWrd", ...
            "brWrd", "cbWrd", "test", "testResp", "mousex", "mousey", "mouseleftButton", "mousemidButton", ...
            "mouserightButton", "testInstr_mousex", "testInstr_mousey", "testInstr_mouseleftButton", ...
            "testInstr_mousemidButton", "testInstr_mouserightButton", "test_mousex", "test_mousey", ...
            "test_mouseleftButton", "test_mousemidButton", "test_mouserightButton", "test_responsetext", ...
            "test_loopthisRepN", "test_loopthisTrialN", "test_loopthisN", "test_loopthisIndex", "test_loopran"];
        opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double", ...
            "string", "string", "string", "string", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "string", "string", "string", ...
            "double", "double", "double", "double", "double", "double", "string", "double", "double", ...
            "string", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "string", "string", "string", "double", "string", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "string", "double", "double", "double", "double", "double"];
        opts.ExtraColumnsRule = "ignore";
        opts.EmptyLineRule = "read";
        opts = setvaropts(opts, ["nlLet", "brLet", "cbLet", "word_rsptext", "nlWrd", "brWrd", "cbWrd", "testResp", "test_responsetext"], ...
                                 "WhitespaceRule", "preserve");
        opts = setvaropts(opts, ["date", "expName", "psychopyVersion", "OS", "nlLet", "brLet", "cbLet", "translation_keykeys", ...
                                 "word_rsptext", "nlWrd", "brWrd", "cbWrd", "testResp", "test_responsetext"], ...
                                 "EmptyFieldRule", "auto");

    % Days 3 and 4: training on words and not on letters
    case {'003','004'}
        opts = delimitedTextImportOptions("NumVariables", 56, "Encoding", "UTF-8");
        opts.DataLines = dataLines;
        opts.Delimiter = ",";
        opts.VariableNames = ["welcome_mousex", "welcome_mousey", "welcome_mouseleftButton", ...
            "welcome_mousemidButton", "welcome_mouserightButton", "ID", "date", "expName", ...
            "psychopyVersion", "OS", "frameRate", "trainInstr_mousex", "trainInstr_mousey", ...
            "trainInstr_mouseleftButton", "trainInstr_mousemidButton", "trainInstr_mouserightButton", ...
            "translation_keykeys", "translation_keycorr", "translation_keyrt", "word_rsptext", ...
            "trWrd_mousex", "trWrd_mousey", "trWrd_mouseleftButton", "trWrd_mousemidButton", ...
            "trWrd_mouserightButton", "train_loopthisRepN", "train_loopthisTrialN", "train_loopthisN", ...
            "train_loopthisIndex", "train_loopran", "nlWrd", "brWrd", "cbWrd", "test", "testResp", ...
            "mousex", "mousey", "mouseleftButton", "mousemidButton", "mouserightButton", ...
            "testInstr_mousex", "testInstr_mousey", "testInstr_mouseleftButton", ...
            "testInstr_mousemidButton", "testInstr_mouserightButton", "test_mousex", ...
            "test_mousey", "test_mouseleftButton", "test_mousemidButton", "test_mouserightButton", ...
            "test_responsetext", "test_loopthisRepN", "test_loopthisTrialN", "test_loopthisN", ...
            "test_loopthisIndex", "test_loopran"];
        opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "categorical", ...
            "string", "string", "string", "double", "double", "double", "double", ...
            "double", "double", "string", "double", "double", "string", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "string", ...
            "string", "string", "double", "string", "double", "double", "double", "double", "double", ...
            "double", "double", "double", "double", "double", "double", "double", "double", "double", ...
            "double", "string", "double", "double", "double", "double", "double"];
        opts.ExtraColumnsRule = "ignore";
        opts.EmptyLineRule = "read";
        opts = setvaropts(opts, ["word_rsptext", "nlWrd", "brWrd", "cbWrd", "testResp", "test_responsetext"], ...
                                 "WhitespaceRule", "preserve");
        opts = setvaropts(opts, ["date", "expName", "psychopyVersion", "OS", "translation_keykeys", ...
                                 "word_rsptext", "nlWrd", "brWrd", "cbWrd", "testResp", "test_responsetext"], ...
                                 "EmptyFieldRule", "auto");

end

% Import the data
imported = readtable(filename, opts);

% Manipulate the table to get organized data
trimmed = clean_trim_csv(imported, session);

end