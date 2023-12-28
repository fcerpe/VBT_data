function [opt, subResults] = clean_mergeAndSave(opt, trimmedCsv, trimmedLog, subResults, subInfo)
%   SAVE FILES 
%   - save each file as a .csv 
%   - add current subs data to the subResults structure

%% Merge files: accuracy and then timing

trainingTable = cat(2, trimmedCsv.training, trimmedLog.training);
testTable = cat(2, trimmedCsv.test, trimmedLog.test);

if strcmp(subInfo.sesID, '002')
    refreshTable = cat(2, trimmedCsv.refresh, trimmedLog.refresh);
end


%% Save files as csv
% Get sub info compatible with filename
subName = ['sub-' subInfo.subID];
sesName = ['ses-' subInfo.sesID];
scriptName = ['script-' subInfo.scriptID];

% Fetch the output directory: if not present, make it
outputDir = fullfile(opt.dir.extracted, subName, sesName);

if ~exist(outputDir)
    mkdir(outputDir)
end

% Training table
writetable(trainingTable, fullfile(outputDir, [subName,'_',sesName,'_task-',opt.taskName,'_',scriptName,'_beh-training.csv']));

% Test table
writetable(testTable, fullfile(outputDir, [subName,'_',sesName,'_task-',opt.taskName,'_',scriptName,'_beh-test.csv']));

% Refresh table, if present
if strcmp(subInfo.sesID, '002')
    writetable(refreshTable, fullfile(outputDir, [subName,'_',sesName,'_task-',opt.taskName,'_',scriptName,'_beh-refresh.csv']));
end


%% Add to the big variable

subVar = ['sub' subInfo.subID];
sesVar = ['ses' subInfo.sesID];
scriptVar = subInfo.scriptID;

eval(['subResults.',subVar,'.',sesVar,'.training = trainingTable;']);
eval(['subResults.',subVar,'.',sesVar,'.test = testTable;']);
if strcmp(subInfo.sesID, '002')
    eval(['subResults.',subVar,'.',sesVar,'.refresh = refreshTable;']);
end

end
   




