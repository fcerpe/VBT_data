%% VISUAL BRAILLE TRAINING - DATA CLEANING
% 
% Main script to extract information from raw data
%
% From inputs data (extracted from Pavlovia), take the subjects that have
% completed the experiment and "preprocess" / clean the results and log
% tables.
%
% © Filippo Cerpelloni


% Clean workspae and command window
clear;
clc;

% Load bidspm for secondary subfunctions 
addpath '../lib/bidspm'
addpath(genpath(pwd))
bidspm;

% get option
opt = clean_option();


%% Extract data from raw
% For each subject:
% - extract data from the four different days of training
% - import each csv and extract the meaningful responses (for accuracy)
% - import log file and extract timings
% - save relevant files in /outputs/extracted_data/subID 

[opt, subResults] = clean_import(opt);


%% Make summary for JASP / R (separate function)

% Get files from each preprocessed sub

% Make data into new file in new format:
% sub, script, ACCURACIES
% day1: time reading training, time checking training, time reading test, 
%       time checking test
% day2: time reading refresh, time checking refresh, time reading training, 
%       time checking training, time writing training, time reading test, 
%       time checking test
% day3: time reading training, time checking training, time writing training, 
%       time reading test, time checking test
% day4: time reading training, time checking training, time writing training, 
%       time reading test, time checking test



