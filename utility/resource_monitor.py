#!/usr/bin/python
######
# Description: Monitors system resources (WIP)
######

'''
As a starting point I'd want to know if five minute load average exceeds 
2xCPU (on our nodes greater than 80) and/or if iowait exceeds 30.

Once we know when/if that's happening we can tweak from there based on 
what we see on the actual systems during heavy job use.
'''

import argparse
import subprocess
import time
import logging
import socket
import sys
import os
import glob
import time
import datetime

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
stdoutLogger.setLevel(logging.ERROR)
stdoutLogger.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logging.getLogger().addHandler(stdoutLogger)
logging.info("\n-------------------------\nBEGIN LOG FILE\n-------------------------\n") 

aparser = argparse.ArgumentParser(description="Generate AD Groups and Memberships for Ranger")
aparser.add_argument('-hr', '--hours', help="runtime in hours")
aparser.add_argument('-m', '--minutes', help="runtime in minutes")
aparser.add_argument('-s', '--seconds', help="runtime in seconds")
aparser.add_argument('-nl', '--nolog', action='store_true', default=False, help="Do not store the log (useful for testing)")
args = aparser.parse_args()

# 
# Parse args
#

# check for conflicting ergs
if args.minutes is not None and args.seconds is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")
elif args.minutes is not None and args.hours is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")
elif args.hours is not None and args.seconds is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")

if args.hours is not None:
	total_hours = int(args.hours)
	finish_time = datetime.datetime.now() + datetime.timedelta(seconds=total_hours)

if args.minutes is not None:
	total_minutes = int(args.minutes)
	finish_time = datetime.datetime.now() + datetime.timedelta(minutes=total_minutes)

if args.seconds is not None:
	total_seconds = int(args.seconds)
	finish_time = datetime.datetime.now() + datetime.timedelta(seconds=total_seconds)

def sendEmail(msg):
	""" Sends an email out based on given information """

	p = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	p.communicate(msg.as_string())

def test_cpu_load(finish_time):
	"""Tests CPU load from a fixed time frame"""

	# Goal: want to know if five minute load average exceeds 2xCPU (on our nodes greater than 80)
	# and/or if iowait exceeds 30. Generate CPU load with parallel instances of:
	# 'dd if=/dev/zero of=/dev/null'

	# Set warning at 50%, Critical at 90%
	cpu_limit_1min = float(20.10)
	cpu_limit_5min = float(10.10)
	cpu_limit_15min = float(5.10)
	cpu_limit_threshold = cpu_limit_1min
	cpu_limit_warning = cpu_limit_threshold * .5
	cpu_limit_critical = cpu_limit_threshold *.9
	print "Running OS load averge until:", finish_time
	print "CPU threshold limit:", cpu_limit_threshold

	while datetime.datetime.now() < finish_time:

		# reduce stdout logging to INFO when testing is done
		raw_average = os.getloadavg()
		load_average = {1: raw_average[0], 5: raw_average[1], 15: raw_average[2]}
		logging.info("CPU Load sample: " + str(load_average))
		#print "\n" + str(load_average)

		if raw_average[0] >= cpu_limit_critical:
			sys.stdout.write('\r'+ 'WARNING: CPU limit at critical capacity              ')
			sys.stdout.flush()
			logging.warning("CPU load at critical capacity: " + str(load_average))
		elif raw_average[0] >= cpu_limit_warning:
			# Make sure to make the buffer rewrite at least as long as the last to overwrite it all
			sys.stdout.write('\r'+ 'WARNING: CPU limit at half capacity                  ')
			sys.stdout.flush()
			logging.warning("CPU load at half capacity: " + str(load_average))
		elif raw_average[0] < cpu_limit_threshold:
			sys.stdout.write('\r'+ 'CPU limit within threshhold. Continuing to monitor...')
			sys.stdout.flush()

		# Check outside of conditionals if the limit has been met
		if raw_average[0] > cpu_limit_threshold:
			sys.exit("\nCPU limit reached! limiter: " + str(cpu_limit_threshold))

		# Idle for a bit so we are not flooding the log
		time.sleep(10)

test_cpu_load(finish_time)
# End log file
logging.info("\n-------------------------\nEND LOG FILE\n-------------------------\n") 

'''
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
'''
