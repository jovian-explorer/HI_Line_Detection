# Program for calibrating data. The files should be saved as csv files and
# should be named by the corresponding galactic longitude of the
# observation. This is assuming you are pointing only in galactic equator
# requires vlsr correction for observations
# Outputs calibrated x and y axis to Calibrated_data folder

#---------------------------------------------importing libraries required---------------------------------------------
from __future__ import print_function, division
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import argparse
import copy
import datetime
from PyAstronomy import pyasl
import math
from matplotlib.gridspec import GridSpec
global low, up

#----------------------------------------------Addition for input file------------------------------------------------

inpf = "/home/dev/Project_H1_line_detection/real_data/log_H1_2022_08_26_15_32_12"#file for on source observations.
cal_file = "/home/dev/Project_H1_line_detection/real_data/log_H1_2022_08_26_15_32_12"#file for off source observations.
    

# Values of quantities
f0 = 1420.405752;    % 21cm in MHz
c = 299792.458;      % speed of light in km/s
Tref = 300;          % Reference temperature in Kelvin
Tsky = 5;            % Sky temperature in Kelvin

std_rms = []; % estimated rms
mod_rms = []; % modeled rms
%Read files
folder = [2 3 4 5 6]; % folder named as numbers for various sets of observations
for k = 1:length(folder)
    indir = sprintf('./../%i/',folder(k)); % path to observation folder
    fnames = dir([indir '*.csv']);
    
    % Reading zenith file data
    fid = fopen([indir 'zenith.csv']);
    a = textscan(fid,'%f%f%f','delimiter',',','headerlines',1);
    fclose(fid);
    
    tz = a{1};
    fz = a{2};
    pz = a{3};
    
    % Power in linear unit
    pzl = 10.^(pz./10);
    
    
    % Reading ground file data
    fid = fopen([indir 'ground.csv']);
    b = textscan(fid,'%f%f%f','delimiter',',','headerlines',1);
    fclose(fid);
    
    tg = b{1};
    fg = b{2};
    pg = b{3};
    
    % Power in linear unit
    pgl = 10.^(pg./10);
    
    
    % Radiometer temperature (in Kelvin)
    pratio = (pgl./pzl);
    num = (Tsky .* pratio) - Tref;
    den = 1 - pratio;
    Tr = num./den;
    
    % Multiplicative factor a denoted as x1,x2. x1=x2
    x1 = (Tr+Tsky)./pzl;
    x2 = (Tr+Tref)./pgl;
    x = x1;
    
    % fit line to Tr baseline
    npoints = 300;
    
    fbase = fg([1:npoints end-npoints+1:end]);
    Tbase = Tr([1:npoints end-npoints+1:end]);
    
    p = polyfit(fbase,Tbase,1);
    
    Tsys = (p(1) .* fg) + p(2) ; % equation of line
    
    Tres_line = (p(1) .* fbase) + p(2) ;
    
    Tres = Tbase - Tres_line;
    
    
    fprintf('Mean = %f and Std = %f.\n', mean(Tres_line),std(Tres))
    Trms = ((2)^0.5)*mean(Tres_line)/((4000*4)^0.5); %
    mod_rms = [mod_rms Trms];
    fprintf('Modeled T_RMS = %f.\n', Trms)
    figure
    plot(fg,Tr,'b-','linewidth',2);
    hold on
    scatter(fbase,Tbase,50,'ro','filled');
    plot(fg,Tsys,'k-','linewidth',2);
    box on
    grid on
    ylabel('T_{rec} (K)')
    xlabel('Frequency (MHz)')
    set(gca,'fontsize',20)
    
    %% calibrate plots
    baseline = fg([1:10 end-10]);
    
    for i = 1:length(fnames)
        
        filename = fnames(i).name;
        
        if strcmp(filename,'ground.csv')==0 && strcmp(filename,'zenith.csv')==0
            
            fprintf('%d\n',i)
            
            % Reading data files
            fid = fopen([indir filename]);
            d = textscan(fid,'%f%f%f','delimiter',',','headerlines',1);
            fclose(fid);
            
            td = d{1};
            fd = d{2};
            pd = d{3};
            
            % Power in watts
            pdl = 10.^(pd./10);
            
            % Doppler velocity correction
            aaa = xlsread('.././vlsr_data.xlsx','A2:P28');
            theta = aaa(:,1); %galactic longitude, change column number accordingly
            %v = (aaa(:,9)); %vel correction, change column number accordingly
            v = 0;
            for j = 1:length(theta)
                if str2double(filename(1:end-4))==theta(j)
                    v = -aaa(j,9);
                end
            end
            vd = v + (c .* (1 - (fd./f0)));

            %--------------
            Tdl = (Tref + Tsys.*(1 - (pgl./pdl)))./(pgl./pdl);
            
            Tsysl = Tdl + mean(Tres_line);
            
            Tsig1 = Tdl;
            Tsig = Tsig1;
            %save plots csv
            %         T = table(vd,Tsig);
            %         writetable(T,filename);
            %brightness temperature
            vbase = vd([1:npoints end-npoints+1:end]);
            Tbase = Tsig([1:npoints end-npoints+1:end]);
            
            p = polyfit(vbase,Tbase,1);
            
            Tsig = (p(1) .* vd) + p(2) ;
            
            %Tb = (p(1) .* vbase) + p(2) ;
            Tb_final_BT = Tsig1 - Tsig;   % Final Brightness Temperature
            
            Tb_line = (p(1) .* vbase) + p(2) ;
            Tb = Tbase - Tb_line;
            
            std_rms = [std_rms std(Tb)];
            fprintf('Mean = %f and Std = %f.\n', mean(Tb_line),std(Tb));
            
            % Save data to
                if not(isfolder('.././Calibrated_data'))
                   mkdir('.././Calibrated_data')
                end
%                 V_LSR = vd;
%                 T_brightness = Tb_final_BT;
%                     T = table(V_LSR,T_brightness);
%                     writetable(T,['.././Calibrated_data/' filename]);
            
            figure

            hold on
            plot(vd,Tsysl,'r-','linewidth',1);
            box on
            plot(vd,Tb_final_BT,'b-','linewidth',1);
            box on
            plot(vd,Tsig1,'Color',[34/255 139/255 34/255],'linewidth',1);
            box on
            scatter(vbase,Tbase,10,'ko','filled');
            box on;
            plot(vd,Tsig,'k-','linewidth',1);
            box on;
            plot(vd,Tb_final_BT,'b-','linewidth',1);
            grid on
            ylabel('Temperature (K)')
            xlabel('Velocity (km s^{-1}) w.r.t. LSR')
            legend({'T_{sys}','T_{brightness}','T_{sys} - T_{r}','Fitting points','T_{add}'})
            title(['Galactic Longitude  ' filename(1:end-4) '^{\circ}'])
            set(gca,'FontName','Times New Roman');
            set(gca,'FontSize',15); % Set it to times
            
            
            
        end
    %saving plots
        
    end
        if not(isfolder('.././Plots'))
            mkdir('.././Plots')
        end
    %print(gcf,'.././Plots/Calibration.eps','-depsc','-r300');
    %print(gcf,'.././Plots/Calibration.tif','-dtiffn','-r300');
    %print(gcf,'.././Plots/Calibration.png','-dpng','-r300');
end
toc
fprintf('Estimated RMS= %f ___ Modeled RMS = %f ___ Difference = %f___Error = %f.\n ', mean(std_rms),mean(mod_rms),(mean(std_rms)-mean(mod_rms)),100.*(mean(std_rms)-mean(mod_rms))./mean(std_rms));
%fprintf('Tsys = %f',(74.6+74.6+67+58.6+65.7+65.7)/6);
