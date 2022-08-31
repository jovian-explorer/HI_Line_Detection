tic

clear
close all

% Parameters to be used

c = 299792.458;  % Speed of light (in km/s)
v_lsr = 218;     % Orbital speed of Sun wrt galactic center (in km/s)

R_sun = 8.5;     % Distance of the Sun from the galactic center (in kpc)

v_disp = 25;     % dispersion (FWHM for 180 longitude)

%% Error bars
%Read files

aa = readtable('.././Max_rel_vel/max_rec_vel.csv');
aa = aa(3:10,:);

theta = aa{:,1};
v_rec_max = aa{:,2};
v_upper = aa{:,3};
v_lower = aa{:,4};

%calculate values for velocity and radius
v_source = (v_lsr*sind(theta) ) + v_rec_max - v_disp;
R = R_sun.*sind(theta);

%v_lsr_err = 6;
v_lsr_err = 2.8;
v_upper_err = -v_upper + v_rec_max;
v_lower_err =  v_lower - v_rec_max;
theta_err = 0.1;
R_sun_err = 0.5;

v_disp_err = 1;

%calculate error bars
v_pos = ((v_lsr_err * sind(theta)).^2 + (theta_err * v_lsr * cosd(theta)).^2 + (v_upper_err).^2 + (v_disp_err).^2).^0.5;
v_neg = ((v_lsr_err * sind(theta)).^2 + (theta_err * v_lsr * cosd(theta)).^2 + (v_lower_err).^2 + (v_disp_err).^2).^0.5;
R_pos = ((R_sun_err*sind(theta)).^2 + (theta_err*R_sun*cosd(theta)).^2).^0.5;
R_neg = ((R_sun_err*sind(theta)).^2 + (theta_err*R_sun*cosd(theta)).^2).^0.5;

% plot data
scatter(R,v_source,70,'r','filled')
hold on
errorbar(R,v_source,v_neg,v_pos,R_neg,R_pos,'b-','linewidth',1)
scatter(R,v_source,50,'r','filled')
xlabel('R (kpc)');
ylabel('Velocity (km s^{-1})');
hold on;
%xlim([0 10]);
ylim([0 300]);
%axis equal
grid on;
box on;
set(gca,'FontName','Times New Roman');
set(gca,'FontSize',15); % Set it to times

% save plots
if not(isfolder('.././Plots'))
    mkdir('.././Plots')
end

print(gcf,'.././Plots/Rot_curve.eps','-depsc','-r300');
print(gcf,'.././Plots/Rot_curve.png','-dpng','-r300');
print(gcf,'.././Plots/Rot_curve.tif','-dtiffn','-r300');
toc