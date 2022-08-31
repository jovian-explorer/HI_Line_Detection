This document explains the steps involved in data analysis and using the code.
 
Saving the observations
 
The code is broken down into steps for easy understanding and use. The raw data is collected using the RTLSDR scanner app and is stored as csv files with the name of each file as the galactic longitude. For this experiment, the observations are taken in the galactic plane for galactic longitudes 0, 10, 20,… and these are the corresponding names of the csv files.
The observations are broken down into sets according to the best possible observation conditions for each direction. Each set of observations is saved in a folder named 1, 2, 3… . 
Each folder contains the source observation files, a zenith observation file and a ground observation file. 


E.g., folder 1 contains 0.csv, 10.csv, 20.csv, 30.csv, 40.csv, ground.csv, zenith.csv.
Folder 2 contains 50.csv, 60.csv, 70.csv, 80.csv, ground.csv, zenith.csv.
And so on.
 
The zenith and ground files are required to calibrate the sources' temperature. Each set is taken at a different time; hence each set must be calibrated individually by pointing the antenna to the zenith and the ground. This takes care of the temperature axis calibration. 
 
For velocity axis calibrations, the radial velocity correction must be done. Here, velocities are corrected to Local Standard of Rest (LSR) by removing the effects of Earth rotation, Earth revolution around the Sun and the peculiar motion of the Sun w.r.t. the LSR. There are two ways mentioned here to get the correction velocity for a given direction. One can use either the Green Bank Telescope (GBT) radial velocity calculator (https://www.gb.nrao.edu/~fghigo/gbt/setups/radvelcalc.html) or the included python script. 
GBT radial velocity calculator:
The calculator is valid for the Green Bank Telescope, which means the velocity correction is done for the location of GBT. This will give rise to small error depending on your location on Earth.
Python script:
The python script requires PyAstronomy (https://pyastronomy.readthedocs.io/en/latest/index.html) package installed.
The inputs to the code are the latitude, longitude and altitude of the telescope, the date and time of observation and the direction of the source. The resulting output can then be added/subtracted to get the velocity w.r.t LSR.
The Matlab code expects an excel named vlsr_data.xlsx file containing the galactic longitude column and the corresponding velocity correction column. 
 
Codes:
Step1_calibrate_data.m
This code reads the files from the observation folders containing the observation, ground and zenith files as mentioned above. The observation data is in units of power (dBm) vs frequency. The code converts the axes to temperature (calibrated) and velocity (corrected to LSR). The calibrated data is stored in the Calibrated_data folder (created automatically).
 
2) Step2_fitting_gaussians.m
After calibration, the data can now be fit with gaussians. The Matlab Curve Fitter tool is used for this purpose. The code reads each file from the Calibrated_data folder and opens the Curve Fitter app for curve fitting. The x and y variables must be loaded manually. The number of gaussians and can be chosen in the app. One should experiment with the app to get the best fit. The fit file must be saved manually in the Fits folder (created automatically) in .sfit format.
 
3) Step3_max_rel_velocity.m
This code reads the .sfit files from the Fits folder and gets the maximum red-shifted point from the model. This point is estimated by the noise in the signal and is chosen by finding the three sigma cutoff point in the most red-shifted part of the line. The error bars are +- 1 sigma points around this point. These points are written to a file in the Max_rel_vel folder (created automatically).
 
4) Step4_rotation_curve.m
This code takes the most red-shifted points from the last step and plots the rotation curve.
 
5) Step5_gaussian_peaks.m
This code takes the .sfit models from the Fits folder and extracts the peaks and the corresponding velocities of the fitted gaussians. These are stored in the Fitted_peaks folder (created automatically).
 
6) Step6_spiral_plot.m
This code takes the velocities of the peaks of the gaussians and plots the arms of the Galaxy.

 
All plots are saved in the Plots folder.
