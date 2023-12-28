function summary_accuracies(opt)
%  MAKE SUMMARY
%
% Accuracies and timings in both training and testing
% First level of analyses

% Import data

% Get "preproc" folder
subsFolder = dir(fullfile(opt.dir.extracted, 'sub-*'));

% Initialize summary table
summary = table('Size', [80 26], ...
                'VariableNames', {'subject', 'script', ...
                    'ses-1_test_accuracy', 'ses-1_test-reading', 'ses-1_train-reading', 'ses-1_train-checking', ...
                    'ses-2_test-accuracy', 'ses-2_test-reading', 'ses-2_train-accuracy', ...
                        'ses-2_train-reading', 'ses-2_train-checking', 'ses-2_train-writing', ...
                        'ses-2_ref-reading', 'ses-2_ref-checking', ...
                    'ses-3_test-accuracy', 'ses-3_test-reading', 'ses-3_train-accuracy', ...
                        'ses-3_train-reading', 'ses-3_train-checking', 'ses-3_train-writing', ...
                    'ses-4_test-accuracy', 'ses-4_test-reading', 'ses-4_train-accuracy', ...
                        'ses-4_train-reading', 'ses-4_train-checking', 'ses-4_train-writing'}, ...
                'VariableTypes', {'string', 'string', 'double', 'double', 'double', 'double', 'double', 'double', ...
                    'double', 'double', 'double', 'double', 'double', 'double', 'double', 'double', 'double', ...
                    'double', 'double', 'double', 'double', 'double', 'double', 'double', 'double', 'double'});

% Initialize table index, but probably same as iSub
iTable = 1;

% Extract data participant by participant
for iSub = 1:numel(subsFolder)
    
    % Notify the user
    fprintf(['\n\nWorking on ', subsFolder(iSub).name '\n']);

    % Get the different session folders
    sessFolder = dir(fullfile(opt.dir.extracted, subsFolder(iSub).name, 'ses-*'));

    % Work on each file
    for iSes = 1:numel(sessFolder)

        % Notify the user
        fprintf(['- adding data from ', sessFolder(iSes).name '\n']);

        % add sub and script
        % read table training
        % add training info
        % read table test
        % add info


    end
end


% Extract information


% Save table 


end