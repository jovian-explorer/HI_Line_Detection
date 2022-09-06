import os
import datetime

itr = 1
for i in range(0,itr):
	now = datetime.datetime.now()
	filestr = "rtl_power -f 1419M:1421M:1k -w blackman-haris -i 1s -e 12h "+ "log_H1_" + now.strftime("%Y_%m_%d")
	os.system(filestr)
