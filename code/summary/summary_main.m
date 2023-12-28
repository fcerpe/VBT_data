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


%% Summarize information

summary_accuracyAndTiming(opt);







