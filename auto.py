#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import argparse
import os
import datetime
import numpy as np
import pandas as pd
import copy
import math
import shutil
import plotly.express as px
import PyAstronomy
import matplotlib.pyplot as plt
import datetime
from matplotlib.gridspec import GridSpec
from PyAstronomy import pyasl
import glob
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

itr = 1
for i in range(0, itr):
    # recording data
    now = datetime.datetime.now()
    filestr = (
        "rtl_power -f 1419M:1421M:1k -w blackman-harris -i 1s -e 12h "
        + "log_H1_"
        + now.strftime("%Y_%m_%d")
    )
    os.system(filestr)
    print("Recording saved!!")

    # relevant filepaths
    filename = "log_H1_" + f"{now.strftime('%Y_%m_%d')}"
    filename2 = filename + "_plots"
    #os.system("mkdir plots")
    os.system("mkdir plots/" + filename2)
    source = "/home/ad_admin/H1/"
    destination = "/home/ad_admin/H1/plots/" + filename2

    # plotting
    os.system(
        "python3 subplot.py -ip /home/ad_admin/H1/"
        + filename
        + " -t 60 -cali /home/ad_admin/H1/cal_file -l -0.1 -u 0.3 -f1 1420 -f2 1420.5 -dt 0.5"
    )
    print("Plotting Done!!")

    # Search files with .txt extension in source directory
    pattern = "*.png"
    files = glob.glob(source + pattern)

    # move the files with txt extension
    for file in files:
        # extract file name from file path
        file_name = os.path.basename(file)
        shutil.move(file, destination)
        print("Moved:", file)
    print("Moved All images")


    def make_gif(frame_folder):
        # Update the glob pattern to match the correct image filenames
        frames = [
            Image.open(image)
            for image in glob.glob(
                f"{frame_folder}/*_averaged_t_60.0s._time_avg_dt_0.5hrs_*.png"
            )
        ]

        # Check if there are images in the 'frames' list before proceeding
        if not frames:
            print("No images found in the specified folder.")
            return

        frame_one = frames[0]
        frame_one.save(
            f"{frame_folder}/{filename}.gif",
            format="GIF",
            append_images=frames,
            save_all=True,
            duration=100,
            loop=0,
        )


    if __name__ == "__main__":
        make_gif(destination)  # Use the 'destination' variable as an argument

        # Output
        print("All processes for file " + filename + " completed !!")
    # putting system to sleep until the next cycle
    print("Good Night, gotta work tomorrow!")
    os.system("sleep 11.75h")
