#!/usr/bin/env python
# coding: utf-8

# PyAstronomy package requireq: https://pyastronomy.readthedocs.io/en/latest/index.html

from __future__ import print_function, division
from PyAstronomy import pyasl
import math
import datetime

# Coordinates of telescope
longitude = -75.857727
latitude = 22.719568
altitude = 554

# Coordinates of source (RA2000, DEC2000) RA_hr RA_min RA_sec DEC_deg DEC_min DEC_sec. Note DEC must be signed + or -.
hd1 = "18 36 07.85 -08 19 30.20"
obs_ra_2000, obs_dec_2000 = pyasl.coordsSexaToDeg(hd1)

# Time of observation converted to Julian Date
dt = datetime.datetime(2019, 2, 12, 15, 49, 43)
jd = pyasl.jdcnv(dt)

# Calculate barycentric correction (debug=True show
# various intermediate results)
corr, hjd = pyasl.helcorr(longitude, latitude, altitude, obs_ra_2000, obs_dec_2000, jd, debug=True)

#print("Barycentric correction [km/s]: ", corr)
#print("Heliocentric Julian day: ", hjd)

# Calculate LSR correction
v_sun = 20.5 # peculiar velocity (km/s) of sun w.r.t. LSR (The Solar Apex. Nature 162, 920 (1948). https://doi.org/10.1038/162920a0)
# solar apex
sun_ra = math.radians(270.2)
sun_dec = math.radians(28.7)

obs_dec = math.radians(obs_dec_2000)
obs_ra = math.radians(obs_ra_2000)

# equation from https://icts-yebes.oan.es/reports/doc/IT-CDT-2014-10.pdf
a = math.cos(sun_dec) * math.cos(obs_dec)
b = (math.cos(sun_ra) * math.cos(obs_ra)) + (math.sin(sun_ra) * math.sin(obs_ra))
c = math.sin(sun_dec) * math.sin(obs_dec)
v_rs = v_sun * ((a * b) + c)

v_lsr = corr + v_rs
print("LSR correction [km/s]: ", -v_lsr)
print("Positive value means receding (redshift) source, negative value means approaching (blueshift) source")
