function import_extract(opt)
%% Extract data from raw
% For each subject:
% - extract data from the four different days of training
% - import each csv and extract the meaningful responses (for accuracy)
% - import log file and extract timings
% - save relevant files in /outputs/extracted_data/subID 

warning('off')


% Load folders
% only those specifiying a day of training
rawFolders = dir(fullfile(opt.dir.input, '*_day*'));

% Folder by folder, get all the files for a participant and extract the
% data
for iF = 1:numel(rawFolders)
    
    % Notify the user
    fprintf(['\n\n\nWorking on script-', rawFolders(iF).name([1,2]), ' ses-00', rawFolders(iF).name(end) '\n\n']);

    % Get two separate lists, one for response/csv files and one for
    % timing/log files
    csvList = dir(fullfile(rawFolders(iF).folder, rawFolders(iF).name, 'sub-*.csv'));
    logList = dir(fullfile(rawFolders(iF).folder, rawFolders(iF).name, 'sub-*.log'));

    % Work on each file
    for iFile = 1:numel(csvList)

        currentCsv = fullfile(csvList(iFile).folder, csvList(iFile).name);
        currentLog = fullfile(logList(iFile).folder, logList(iFile).name);

        % If filenames do not correspond, stop and notify the user
        if ~strcmp(currentCsv(1:end-4), currentLog(1:end-4))
            error('Filenames do not correspond, you are trying to open two different subjects')
        end        

        % Extract subject information
        sub = extractSubjectInfo(currentCsv);

        % Check that data come from a real participant
        if ~ismember(sub.subID, opt.subList)
            error('Participant that is being procesed is not on the list. Check inputs folder')
        end 

        % Notify the user
        fprintf(['Extracting sub-', sub.subID, '...\n']);
        
        % Import csv and clean it based on the day and which files are
        % needed
        trimmedCsv = import_extract_csv(currentCsv, sub.sesID);

        % Import log file and clean it to get the events
        trimmedLog = import_extract_log(currentLog, sub.sesID);

        % Save files
        % create a custom bids-like name to save all the tables extracted,
        % as csv files but also within a variable
        import_extract_mergeAndSave(opt, trimmedCsv, trimmedLog, sub);

    end

end

% Nofity the user
fprintf(['\n\n PIPELINE DONE \nExtracted data can be found in: ' opt.dir.extracted '\n']);


end


%% SUBFUNCTIONS

% Extract information from filename
function subInfo = extractSubjectInfo(filename)

subInfo = struct;

% Split filename
nameParcels = strsplit(filename, {'_','-','/'});

subPos = find(strcmp(nameParcels,'sub') == 1);
sesPos = find(strcmp(nameParcels,'ses') == 1);
scrPos = find(strcmp(nameParcels,'script') == 1);
subInfo.subID = nameParcels{subPos +1};
subInfo.sesID = nameParcels{sesPos +1};
subInfo.scriptID = lower(nameParcels{scrPos +1});


end