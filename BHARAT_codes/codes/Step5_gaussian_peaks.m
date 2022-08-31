% Code to find peaks
tic
clear
close all

if not(isfolder('.././Fitted_peaks'))
    mkdir('.././Fitted_peaks')
end
% Input model
indir = './../Fits/';
infiles = dir([indir '*.sfit']);
nfiles = length(infiles);

counter = 0;

% Loop
for i = 1:nfiles
    % Read files
    cond_name = infiles(i).name;
    cond_name_str = cond_name(1:end-5);
    cond_name = str2double(cond_name_str);
    
    counter = counter + 1;
    
    filename = [indir infiles(i).name];
    
    
    vd1 = load(filename, '-mat');
    %read values from sfit variable vd1
    parameters = vd1.savedSession.AllFitdevsAndConfigs{1, 1}.Fitdev.Output.numparam;
    l = (parameters)/3;
    a = zeros(l,1);
    b = zeros(l,1);
    c = zeros(l,1);
    coeff = coeffvalues(vd1.savedSession.AllFitdevsAndConfigs{1, 1}.Fitdev.Fit  );
    k = 1;
    for j = 1:3:parameters
        
        a(k) = coeff(j);
        b(k) = coeff(j+1);
        c(k) = coeff(j+2);
        k = k + 1;
    end
    fname(counter) = cond_name;
    
    % save peaks
    
    T = table(a,b,c);
    my_directory = 'path to folder Fitted_peaks/'; % give full path to folder 
    save = [my_directory cond_name_str '.txt'];
    writetable(T,save,'delimiter',',')
    
    
end

toc


