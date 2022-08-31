%v = load('yourfile.sfit', '-mat');

% Code to fit gaussians

clear
close all

% Input data
indir = './../Calibrated_data/';
infiles = dir([indir '*.csv']);
nfiles = length(infiles);

% Input fit models
model_indir = './../Fits/';
model_infiles = dir([model_indir '*.sfit']);
model_nfiles = length(model_infiles);

v = zeros(10,1);
v_upper = zeros(10,1);
v_lower = zeros(10,1);
fname = zeros(10,1);
model_fname = zeros(10,1);

counter = 0;

% Loop
for i = 1:nfiles
    
    cond_name = infiles(i).name;
    cond_name_str = cond_name(1:end-4);
    cond_name = str2num(cond_name_str);
    
    model_cond_name = model_infiles(i).name;
    model_cond_name_str = model_cond_name(1:end-4);
    model_cond_name = str2num(model_cond_name_str);
    
    if cond_name <= 90
        
        counter = counter + 1;
        %open data
        filename = [indir infiles(i).name];
        
        %        load(filename);
        
        fid = fopen([filename(1:end-3) 'csv']);
        a = textscan(fid, '%f %f', 'delimiter',',','headerlines',1);
        fclose(fid);
        
        vd = a{1};
        
        x = vd;
        
        %open model
        model_filename = [model_indir model_infiles(i).name];
        vd1 = load(model_filename, '-mat');
        y = vd1.savedSession.AllFitdevsAndConfigs{1, 1}.Fitdev.Fit(vd);
        y_sig = vd1.savedSession.AllFitdevsAndConfigs{1, 1}.Fitdev.Goodness.rmse;
        
        [xs,ind] = sort(x,'desc');
        ys = y(ind);
        
        
        sigma_cut = 0.9*3; % 0.9K is 1 sigma so we choose 3 sigma points
        
        ind_ys = find(ys>=(sigma_cut*y_sig));
        ind_sel = ind(ind_ys(1));
        vel = x(ind_sel);
        y_vel = y(ind_sel);
        v(counter) = vel;
        
        ind_ys1 = find(ys>=((sigma_cut+1)*y_sig)); % 
        ind_sel1 = ind(ind_ys1(1));
        vel1 = x(ind_sel1);
        y_vel1 = y(ind_sel1);
        v_upper(counter) = vel1;
        
        ind_ys2 = find(ys>=((sigma_cut-1)*y_sig));
        ind_sel2 = ind(ind_ys2(1));
        vel2 = x(ind_sel2);
        y_vel2 = y(ind_sel2);
        v_lower(counter) = vel2;
        
        fname(counter) = cond_name;
        
        figure
        plot(x,y,'b-','linewidth',1)
        hold on
        scatter(vel,y_vel,50,'ro','filled')
        scatter(vel1,y_vel1,50,'bo','filled')
        scatter(vel2,y_vel2,50,'ko','filled')
        box on
        set(gca,'fontsize',15)
        set(gca,'FontName','Times New Roman')
        xlabel('Recession Velocity (Km/s)')
        ylabel('Brightness Temperature (K)')
        title([cond_name_str '^{\circ}'])
        
    end
    
end

% make folde Max_rel_vel
if not(isfolder('.././Max_rel_vel'))
    mkdir('.././Max_rel_vel')
end

%Save points of max rel vel
T = table(fname,v,v_upper,v_lower);
writetable(T,'./../Max_rel_vel/max_rec_vel.csv','delimiter',',')



