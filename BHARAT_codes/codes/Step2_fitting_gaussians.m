clear all
close all

indir = './../Calibrated_data/';
fnames = dir([indir '*.csv']);
%sort fnames 
% struct2table(s)
% for j = 1:1:length(fnames)
%     
% end

for i = 1:length(fnames)
    
    filename = fnames(i).name
    
    
    % Reading data files
    fid = fopen([indir filename]);
    d = textscan(fid,'%f%f','delimiter',',','headerlines',1);
    fclose(fid);
    
    x = d{1};
    y = d{2}';

    %Create folder to save fits. fits must be saved manually.
    if not(isfolder('.././Fits'))
        mkdir('.././Fits')
    end

    % Opening Curve Fitter app. The x and y arrays must be chosen manually in
    % the app and then fitting can be done. After fitting, file must be saved to Fits
    % folder in .sfit format
    cftool
    pause

end