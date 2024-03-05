%% VISUAL BRAILLE TRAINING - MAKE SUMMARY TABLES
% 
% Main script to create different summary tables 
% 
% From pre-processed data, take each subject and extract values for the 
% following parameters: 
% - accuracies
% - timings
% - qualitative analyses (type of mistakes)
%
% © Filippo Cerpelloni


% Clean workspae and command window
clear;
clc;

% get option
opt = summary_option();


%% Summarize accuracy and timing

% For each subject, extract and save 
% - accuracies (test and training) 
% - timings (reading, checking, writing) 
% Save a summary csv in
% outputs/derivatives/summary/VBT_summary_results-accuracies-timings.csv

summary_accuraciesAndTimings(opt);







