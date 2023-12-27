function [opt, csvStruct, logStruct] = clean_import(opt)
%% Extract data from raw
% For each subject:
% - extract data from the four different days of training
% - import each csv and extract the meaningful responses (for accuracy)
% - import log file and extract timings
% - save relevant files in /outputs/extracted_data/subID 

% Initialize struct to save subjects' results in a variable
subResults = struct;


% Load folders
% only those specifiying a day of training
rawFolders = dir(fullfile(opt.dir.input, '*_day*'));

% Folder by folder, get all the files for a participant and extract the
% data
for iF = 1%:numel(rawFolders)
    
    % Get two separate lists, one for response/csv files and one for
    % timing/log files
    csvList = dir(fullfile(rawFolders(iF).folder, rawFolders(iF).name, 'sub-*.csv'));
    logList = dir(fullfile(rawFolders(iF).folder, rawFolders(iF).name, 'sub-*.log'));

    % Work on each file
    for iFile = 1%:numel(csvList)

        currentCsv = fullfile(csvList(iFile).folder, csvList(iFile).name);
        currentLog = fullfile(logList(iFile).folder, logList(iFile).name);

        % If filenames do not correspond, stop and notify the user
        if ~strcmp(currentCsv(1:end-4), currentLog(1:end-4))
            error('Filenames do not correspond, you are trying to open two different subjects')
        end

        % Import csv and clean it based on the day and which files are
        % needed
        trimmedCsv = clean_import_csv(currentCsv);

        % Import log file and clean it to get the events
        trimmedLog = clean_import_log(currentLog);

        % Save files
        % create a custom bids-like name to save all the tables extracted,
        % as csv files but also within a variable
%         [opt, subResults] = clean_save_files(opt, trimmedCsv, trimmedLog, subResults);

    end

end



end