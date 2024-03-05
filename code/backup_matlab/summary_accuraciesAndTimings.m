function summary_accuraciesAndTimings(opt)
%  MAKE SUMMARY
%
% Accuracies and timings in both training and testing
% First level of analyses

% Import data

% Get "preproc" folder
subsFolder = dir(fullfile(opt.dir.extracted, 'sub-*'));

% Initialize summary table
summary = table;

% Extract data participant by participant
for iSub = 1:numel(subsFolder)

    % Get subject
    subName = subsFolder(iSub).name;
    
    % Notify the user
    fprintf(['\n\nWorking on ', subName '\n']);

    % Get the different session folders
    sessFolder = dir(fullfile(opt.dir.extracted, subName, 'ses-*'));

    % Extract sub ID to compose the subject's entry
    nameSplit = strsplit(subName, 'sub-');
    subID = nameSplit{2};

    % Compose new entry for table
    entry = initEntry(opt, subID);

    % Work on each file
    for iSes = 1:numel(sessFolder)

        % Get session
        sesName = sessFolder(iSes).name;

        % Notify the user
        fprintf(['- adding data from ', sesName '\n']);

        % Find elements in the folder
        sessFiles = dir(fullfile(opt.dir.extracted, subName, sesName, '*.csv'));


        % Based on session, distinguish which routines were presented
        switch iSes
            case {1, 3, 4}
                % Load the tables from the folder
                [train, test, ~] = loadResults(sessFiles);

                % Process the results (e.g. compute means) and add them to the
                % right columns of the entry
                entry = addResultsToEntry(entry, iSes, train, test, []);

            case 2
                % Load the tables from the folder
                [train, test, ref] = loadResults(sessFiles);

                entry = addResultsToEntry(entry, iSes, train, test, ref);
        end

    end

    % Add the entry to the summary
    summary = cat(1, summary, entry);
end


% Save table 
if ~exist(opt.dir.summary)
    mkdir(opt.dir.summary)
end

writetable(summary, fullfile(opt.dir.summary, 'VBT_summary_results-accuracy-timings.csv'));

end



%% Subfunctions

function [tr, te, re] = loadResults(dir)

% init outputs to avoid errors
te = [];
tr = [];
re = [];

opts.DataLines = [2 Inf];

% find positions of files
trPos = find(endsWith({dir.name}, 'training.csv'));
tePos = find(endsWith({dir.name}, 'test.csv'));

% Load files
tr = readtable(fullfile(dir(trPos).folder, dir(trPos).name));
te = readtable(fullfile(dir(tePos).folder, dir(tePos).name));

% Load extra file if we are in session 2 
if endsWith(dir(1).folder, '002')
    rePos = find(endsWith({dir.name}, 'refresh.csv'));
    re = readtable(fullfile(dir(rePos).folder, dir(rePos).name));
end

% FIX for issue with sub-00050_ses-001
filenameSplit = strsplit(dir(tePos).folder, '/');
if strcmp(filenameSplit{end-1},'sub-00050') && strcmp(filenameSplit{end-1},'ses-001')
    c = readtable(fullfile(dir(tePos).folder, dir(tePos).name), "NumHeaderLines", 1);

end

end

function tableOut = initEntry(opt, subID)

tableOut = table('Size', [1 30], ...
                'VariableNames', {'subject', 'script', ...
                                  'ses-1_test-accuracy', 'ses-1_test-reading',  'ses-1_test-writing', ...
                                  'ses-1_train-reading', 'ses-1_train-checking', ...
                                  'ses-2_test-accuracy', 'ses-2_test-reading',  'ses-2_test-writing', ...
                                  'ses-2_train-accuracy','ses-2_train-reading', 'ses-2_train-checking', 'ses-2_train-writing', ...
                                  'ses-2_ref-reading',   'ses-2_ref-checking', ...
                                  'ses-3_test-accuracy', 'ses-3_test-reading',  'ses-3_test-writing', ...
                                  'ses-3_train-accuracy','ses-3_train-reading', 'ses-3_train-checking', 'ses-3_train-writing', ...
                                  'ses-4_test-accuracy', 'ses-4_test-reading',  'ses-4_test-writing', ...
                                  'ses-4_train-accuracy','ses-4_train-reading', 'ses-4_train-checking', 'ses-4_train-writing'}, ...
                'VariableTypes', {'string', 'string', ...
                                  'double', 'double', 'double', 'double', 'double', 'double', 'double', ...
                                  'double', 'double', 'double', 'double', 'double', 'double', 'double', ...
                                  'double', 'double', 'double', 'double', 'double', 'double', 'double', ...
                                  'double', 'double', 'double', 'double', 'double', 'double', 'double'});

% Add subject
tableOut.subject(1) = subID;

% Find and add script
scriptIdx = find(strcmp(opt.subList, subID));
tableOut.script(1) = opt.scriptList{scriptIdx};

end

function tableOut = addResultsToEntry(tableIn, iSes, tr, te, re)

% Output entry starts from input entry
tableOut = tableIn; 

switch iSes
    case 1
        % Need to assign the following variables 
        % - 'ses-1_test-accuracy'
        % - 'ses-1_test-reading'
        % - 'ses-1_test-writing'
        % - 'ses-1_train-reading'   
        % - 'ses-1_train-checking'
        
        tableOut{1,"ses-1_test-accuracy"} = sum(te.score)/60;
        tableOut{1,"ses-1_test-reading"} = mean(te.readingTime,'omitnan');
        tableOut{1,"ses-1_test-writing"} = mean(te.writingTime,'omitnan');

        tableOut{1,"ses-1_train-reading"} = mean(tr.readingTime,'omitnan');
        tableOut{1,"ses-1_train-checking"} = mean(tr.checkingTime,'omitnan');


    case 2
        % Need to assign the following variables 
        % - 'ses-2_test-accuracy'
        % - 'ses-2_test-reading'
        % - 'ses-2_test-writing'
        % - 'ses-2_train-accuracy'
        % - 'ses-2_train-reading'
        % - 'ses-2_train-checking'
        % - 'ses-2_train-writing'
        % - 'ses-2_ref-reading'
        % - 'ses-2_ref-checking'

        tableOut{1,"ses-2_test-accuracy"} = sum(te.score)/60;
        tableOut{1,"ses-2_test-reading"} = mean(te.readingTime,'omitnan');
        tableOut{1,"ses-2_test-writing"} = mean(te.writingTime,'omitnan');        

        tableOut{1,"ses-2_train-accuracy"} = sum(tr.score)/20;
        tableOut{1,"ses-2_train-reading"} = mean(tr.readingTime,'omitnan');
        tableOut{1,"ses-2_train-checking"} = mean(tr.checkingTime,'omitnan');
        tableOut{1,"ses-2_train-writing"} = mean(tr.writingTime,'omitnan');

        tableOut{1,"ses-2_ref-reading"} = mean(re.readingTime,'omitnan');
        tableOut{1,"ses-2_ref-checking"} = mean(re.checkingTime,'omitnan');


    case 3
        % Need to assign the following variables 
        % - 'ses-3_test-accuracy'
        % - 'ses-3_test-reading'
        % - 'ses-3_test-writing'
        % - 'ses-3_train-accuracy'
        % - 'ses-3_train-reading'
        % - 'ses-3_train-checking'
        % - 'ses-3_train-writing'

        tableOut{1,"ses-3_test-accuracy"} = sum(te.score)/60;
        tableOut{1,"ses-3_test-reading"} = mean(te.readingTime,'omitnan');
        tableOut{1,"ses-3_test-writing"} = mean(te.writingTime,'omitnan');        

        tableOut{1,"ses-3_train-accuracy"} = sum(tr.score)/20;
        tableOut{1,"ses-3_train-reading"} = mean(tr.readingTime,'omitnan');
        tableOut{1,"ses-3_train-checking"} = mean(tr.checkingTime,'omitnan');
        tableOut{1,"ses-3_train-writing"} = mean(tr.writingTime,'omitnan');

    case 4
        % Need to assign the following variables 
        % - 'ses-4_test-accuracy'
        % - 'ses-4_test-reading'
        % - 'ses-4_test-writing'
        % - 'ses-4_train-accuracy'
        % - 'ses-4_train-reading'
        % - 'ses-4_train-checking'
        % - 'ses-4_train-writing'

        tableOut{1,"ses-4_test-accuracy"} = sum(te.score)/60;
        tableOut{1,"ses-4_test-reading"} = mean(te.readingTime,'omitnan');
        tableOut{1,"ses-4_test-writing"} = mean(te.writingTime,'omitnan');        

        tableOut{1,"ses-4_train-accuracy"} = sum(tr.score)/20;
        tableOut{1,"ses-4_train-reading"} = mean(tr.readingTime,'omitnan');
        tableOut{1,"ses-4_train-checking"} = mean(tr.checkingTime,'omitnan');
        tableOut{1,"ses-4_train-writing"} = mean(tr.writingTime,'omitnan');
end

end


