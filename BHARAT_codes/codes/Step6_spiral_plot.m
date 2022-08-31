
tic

clear
close all

% Parameters to be used

v_sun = 218;     % Orbital speed of Sun wrt galactic center (in km/s)
v_rot = v_sun;   % Orbital speed of Sources wrt galactic center (in km/s) [assumed to be constant]
R_sun = 8.5;     % Distance of the Sun from the galactic center (in kpc)
v_sun_err = 6;   % "The Milky Way's circular velocity curve between 4 and 14 kpc from APOGEE data" Jo Bovy et al
R_sun_err = 0.5; % Error in R_sun
theta_err = 0.1; % Error in pointing
vp_err = 0.8;    % Error in determining peak velocity
p = 0;           % correction term which is 0
% Data Files information
dinfo = dir('.././Fitted_peaks/*0.txt');
nfiles = length(dinfo);     % Number of files

count = 0;
%%

for i = 1:nfiles
    % Reading files
    filename = dinfo(i).name;
    
    if isempty(intersect(str2double(filename(1:end-4)),[0 350 180 170]))==1
        
        %fprintf([filename '\n'])
        
        fid = fopen(['.././Fitted_peaks/' filename]);
        a = textscan(fid, '%f%f%f', 'delimiter',',','headerlines',1);
        fclose(fid);
        
        %velocities of peaks
        vp = a(:,2);
        vp = cell2mat(vp);
        
        %galactic longitude
        theta = filename(1:end-4);
        
        theta = str2double(theta);
        
        
        
        for k = 1:length(vp)
            %Distance of source
            R_source = (R_sun*v_sun*sind(theta)) ./ (vp(k) + p + (v_sun*sind(theta)));
                
                %angle of source
                l = asin((R_sun*sind(theta))./R_source);
                theta;
                alpha_rad = pi - ((pi*theta/180) + l);

                count = count + length(alpha_rad);
                
                x = R_source .* sin(alpha_rad);
                y = R_source .* cos(alpha_rad);
                
                %error
                f = v_sun*sind(theta);
                R_err = ((((R_sun_err*f)/(vp(k) + f))^2 ...
                    + (-R_sun*f*vp_err/(vp(k) + f)^2)^2 ...
                    + ((v_sun_err*sind(theta))*((1/(1+f)) - (f/(1+f)^2)))^2 ...
                    + ((theta_err*v_sun*cosd(theta))*((1/(1+f)) - (f/(1+f)^2))))^2)^0.5;
                m = R_sun*sind(theta)./R_source ;
                l_err = (((1/(1-m^2))^2)* ...
                    (R_sun_err*sind(theta)/R_source)^2 ...
                    + (R_sun*cosd(theta)*theta_err/R_source)^2 ...
                    + (-R_sun*sind(theta)*R_err/R_source^2)^2)^0.5;
                alpha_rad_err = ((pi*theta_err/180)^2 + l_err^2)^0.5;
                
                x_err = ((R_err*sin(alpha_rad))^2 + (R_source*cos(alpha_rad)*alpha_rad_err)^2)^0.5;
                y_err = ((R_err*cos(alpha_rad))^2 + (-R_source*sin(alpha_rad)*alpha_rad_err)^2)^0.5;
                
                x0 = 0; %for center
                y0 = 0; %fro center
                
                xe = R_sun .* sind(0); % for sun
                ye = R_sun .* cosd(0); % for sun
                

                
                %fprintf('%d',theta);
                if (x_err <2 && y_err < 2)
                    eh = errorbar(x,y,y_err,y_err,x_err,x_err,'color',[139 69 22]/255,'marker','o',...
                        'linewidth',1,'MarkerEdgeColor','black');
                    hold on
                    scatter(x,y,20,'ro','filled')
                    %           scatter(x1,y1,10,'r','filled')
                    scatter(xe,ye,200,'b*','linewidth',2) %sun
                    scatter(x0,y0,300,'k+','linewidth',2) %center
                    
                end
                
            
        end
        
        
    end
    
end

%%

axis equal
%grid on
box on
xlabel('X (kpc)')
ylabel('Y (kpc)')
set(gca,'FontName','Times New Roman');
set(gca,'FontSize',15); % Set it to times
%set(gca,'color','k')
ylim([-15 22])
toc

%print(gcf,'Spiral_1.eps','-depsc','-r300');