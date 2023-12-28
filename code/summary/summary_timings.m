function summary_timings(opt)
%  MAKE SUMMARY OF TIMING DATA

% Import data

% Get "preproc" folder
preproc = dir(fullfile(opt.dir.extracted, 'sub-*'));

% Initialize summary table
summary = table('Size', [80 5], ...
                'VariableNames', {'subject', 'script', ...
                                  'ses-1_test_accuracy', 'ses-1_test-readingTime', 'ses-1_test_writingTime', ...
                                  'ses-2_test-accuracy', ...
                                  'ses-3_test-accuracy', ...
                                  'ses-4_test-accuracy'}, ...
                'VariableTypes', {});


% Extract data participant by participant
for iF = 1:numel(preproc)
    
    % Notify the user
    fprintf(['\n\n\nWorking on script-', preprocFolder(iF).name([1,2]), ' ses-00', preprocFolder(iF).name(end) '\n\n']);

    % Get two separate lists, one for response/csv files and one for
    % timing/log files
    csvList = dir(fullfile(preproc(iF).folder, preproc(iF).name, 'sub-*.csv'));
    logList = dir(fullfile(preproc(iF).folder, preproc(iF).name, 'sub-*.log'));

    % Work on each file
    for iFile = 1:numel(csvList)


    end
end


% Extract information


% Save table 


end