function opt = import_option()
% returns a structure that contains the options chosen by the user to run
% Data cleaning (called through clean_main)

if nargin < 1
    opt = [];
end

% I like chatty outputs
opt.verbosity = 2;

% task to analyze
opt.taskName = 'alphabetLearning';


% PATHS
% The directory where the data are located
opt.dir.root = fullfile(fileparts(mfilename('fullpath')), '..', '..');

opt.dir.raw = fullfile(opt.dir.root, 'inputs');
opt.dir.derivatives = fullfile(opt.dir.root, 'outputs', 'derivatives');
opt.dir.extracted = fullfile(opt.dir.root, 'outputs', 'derivatives', 'extracted-data');
opt.dir.input = opt.dir.raw;
opt.dir.stats = fullfile(opt.dir.root, 'outputs', 'derivatives', 'analyses');

% directory for the saved jobs
opt.jobsDir = fullfile(opt.dir.derivatives, 'jobs', opt.taskName);

% Type of pipeline
opt.pipeline.type = 'cleaning';

% ASSIGN SUBJECTS AND SCRIPTS
% Load from participants.tsv 
par = tdfread(fullfile(opt.dir.raw,'participants.tsv'));
opt.subList = {}; 
opt.scriptList = {};

for iPar = 1:size(par.subject,1)

    % Subjects
    opt.subList{iPar} = par.subject(iPar,2:6);

    % Scripts
    opt.scriptList{iPar} = par.script(iPar,:);
end

end