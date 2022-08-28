# Project_H1_line_detection
This project explains hardware and software for a backyard H1 line detection.


# Code Usage
pyhton3 data_avg.py [-h HELP] [-ip INPUTFILE] [-io OUTPUTFILE] [-t AVGTIME] [-plt PLOTFILENAME] [-res TIMERES] [-cali CALIBRATIONFILE] [-l LOWERCUTOFF] [-u UPPERCUTOFF]


argument description:

      -h, --help                                                        show this help message and exit
      -ip INPUTFILE, --inputfile INPUTFILE                              input filename with path (must be provided)
      -io OUTPUTFILE, --outputfile OUTPUTFILE                           output filename with path
      -t AVGTIME, --avgtime AVGTIME                                     average time in seconds (default = 10s)
      -plt PLOTFILENAME, --plotfilename PLOTFILENAME                    plot the and save the filename with path
      -res TIMERES, --timeres TIMERES                                   time resolution of data in seconds (default = 1s)
      -cali CALIBRATIONFILE, --calibrationfile CALIBRATIONFILE          To remove system error provide clibration file path
                                                                        (default setting is to plot non calibrated result)
      -l LOWERCUTOFF, --lowercutoff LOWERCUTOFF                         lower cutoff for waterfall plot
      -u UPPERCUTOFF, --uppercutoff UPPERCUTOFF                         lower cutoff for waterfall plot


Example:

python3 data_avg.py -ip [Input file path] -t [average time in seconds] -cali [calibration file path] -l [lower limit of waterfall plot] -u [upper limit of waterfall plot]

python3 subplot.py -ip /home/dev/Project_H1_line_detection/real_data/log_H1_2022_08_27_16_15_48 -t 60 -cali /home/dev/Project_H1_line_detection/calibration/cal_file -l -0.1 -u 0.3 -f1 1420 -f2 1420.5 -dt 0.5

# Sample Data
Sample data file link: [Dropbox](https://www.dropbox.com/sh/fiapt4wd439nawa/AAAxG33dJw-1ByZ5uw9c7XEaa?dl=0)
