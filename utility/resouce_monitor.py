#!/usr/bin/python
######
# Description: Monitors system resources (WIP)
######

import argparse
import subprocess
import time
import logging
import socket
import sys
import os
import glob

# Set gloabal variables for processed users and groups
processed_ad_groups = []
processed_ldap_groups = []

# Other vars
origin_host = socket.gethostname()

#
# log config
#

# Stamp log with exact time
# Rename log only at the end of script to avoid clutter
log_filename_tmp = "/tmp/resource-monitor-log-tmp.txt"
log_dest_hdfs = '/uda-scripts/audit/adretriever'
# Reuse the same log file for now (unless we should keep these rolling)
# Log all for file log
log_formatting = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=log_filename_tmp, level=logging.DEBUG, filemode='w', format=log_formatting) 
# Log to file and to stdout
# For the console logger, only show warnings, error, critical
stdoutLogger=logging.StreamHandler()
stdoutLogger.setLevel(logging.WARNING)
stdoutLogger.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logging.getLogger().addHandler(stdoutLogger)
logging.info("\n-------------------------\nBEGIN LOG FILE\n-------------------------\n") 

# LDAP host parameters
adldapuri = "ldaps://adldapserver.geisinger.edu"
ldapuri = "ldaps://smgldaprlx2v.geisinger.edu"

aparser = argparse.ArgumentParser(description="Generate AD Groups and Memberships for Ranger")
aparser.add_argument('-nl', '--nolog', action='store_true', default=False, help="Do not store the log (useful for testing)")
args = aparser.parse_args()

def sendEmail(msg):
		""" Sends an email out based on given information """
		p = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
		p.communicate(msg.as_string())

# End log file
logging.info("\n-------------------------\nEND LOG FILE\n-------------------------\n") 

# Rename log file and push to HDFS
log_filename = "/tmp/resource-monitor-log-" + str(time.strftime("%Y%m%d-%H%M%S")) + ".txt"
try:
	os.rename(log_filename_tmp, log_filename)
except:
	logging.error("Could not rename logfile: " + str(log_filename_tmp) + ". Please check /tmp on host " + origin_host)
	sys.exit()

# Handle script log
if args.nolog is not None:
	logging.info("Transferring log file: " + str(log_filename) + " to HDFS at location " + log_dest_hdfs)
	# Check sudo status first
	proc_status = subprocess.call(['sudo', '-u', 'hdfs', '-n', 'uname'], stdout=open('/dev/null', 'w'))
	if proc_status is 0:
		subprocess.call(['sudo', '-n', '-u', 'hdfs', 'hadoop', 'fs', '-put', log_filename, log_dest_hdfs], stdout=open('/dev/null', 'w'))
		# Attempt to remove old log files now
		# This should be fine unless a log failed to cleanup and another less privledged user is trying to remove it
		for logname in glob.glob('/tmp/resource-monitor-log*.txt'):
			try:
				os.remove(logname)
			except:
				logging.error("Could not remove logfile: " + str(logname) + ". Please check /tmp on host " + origin_host)
	else:
		logging.error("Could not transfer log file. Perhaps sudo timed out")
else:
	logging.info("Log file will not be transferred to HDFS")
