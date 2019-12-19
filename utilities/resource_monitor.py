#!/usr/bin/python
######
# Description: Monitors system resources (WIP)
#	Loggign is designed to be minimal with stdout, rewritting the
#	Buffer to output normal/warning/critical states
#	file-level logging outputs deatil at regular intervals
######

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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Other vars
origin_host = socket.gethostname()

#
# log config
#

# Stamp log with exact time
# Rename log only at the end of script to avoid clutter
log_filename_tmp = "/tmp/os-resource-monitor-log-tmp.txt"
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
aparser.add_argument('-cpult1', '--cpu-load-threshold1', help="specify CPU load threshold (1 minute)")
aparser.add_argument('-cpult5', '--cpu-load-threshold5', help="specify CPU load threshold (5 minutse)")
aparser.add_argument('-cpult15', '--cpu-load-threshold15', help="specify CPU load threshold (15 minutes)")
aparser.add_argument('-cti', '--cpu-interval', help="specify main cpu internal to monitor (1, 5, or 15 min)")
aparser.add_argument('-r', '--refresh-rate', help="specify how often to check the samples (seconds, default 15)")
aparser.add_argument('-d', '--days', help="runtime in days")
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
elif args.days is not None and args.seconds is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")
elif args.days is not None and args.minutes is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")
elif args.days is not None and args.hours is not None:
	sys.exit("ERROR: Arguments cannot be specified together.")

# 1 minute cpu_load_threshold
if args.cpu_load_threshold1 is None:
	# set default
	cpu_load_threshold1 = float(80.00)
else:
	cpu_load_threshold1 = float(args.cpu_load_threshold1)

# 5 minute cpu_load_threshold
if args.cpu_load_threshold5 is None:
	# set default
	cpu_load_threshold5 = float(80.00)
else:
	cpu_load_threshold5 = float(args.cpu_load_threshold5)

# 15 minute cpu_load_threshold
if args.cpu_load_threshold15 is None:
	# set default
	cpu_load_threshold15 = float(80.00)
else:
	cpu_load_threshold15 = float(args.cpu_load_threshold15)

# Set main interval to monitor
if args.cpu_interval is None:
	# set default to 1 minute intervals
	cpu_interval_string = '1 min'
	cpu_interval = cpu_load_threshold1 
else:
	cpu_interval_tmp = int(args.cpu_interval)
	# Set interval based on arg
	if cpu_interval_tmp is 1:
		cpu_interval_string = '1 min'
		cpu_interval = cpu_load_threshold1 
		raw_avg_index = 0
	elif cpu_interval_tmp is 5:
		cpu_interval_string = '5 min'
		cpu_interval = cpu_load_threshold5 
		raw_avg_index = 1
	elif cpu_interval_tmp is 15:
		cpu_interval_string = '15 min'
		cpu_interval = cpu_load_threshold15 
		raw_avg_index = 2
	else:
		sys.exit("Invalid CPU interval specified")
	
# Set runtime
if args.days is not None:
	total_days = int(args.days)
	finish_time = datetime.datetime.now() + datetime.timedelta(days=total_days)
elif args.hours is not None:
	total_hours = int(args.hours)
	finish_time = datetime.datetime.now() + datetime.timedelta(hours=total_hours)
elif args.minutes is not None:
	total_minutes = int(args.minutes)
	finish_time = datetime.datetime.now() + datetime.timedelta(minutes=total_minutes)
elif args.seconds is not None:
	total_seconds = int(args.seconds)
	finish_time = datetime.datetime.now() + datetime.timedelta(seconds=total_seconds)
else:
	# set a default runtie of 60 minutes
	finish_time = datetime.datetime.now() + datetime.timedelta(minutes=60)

# set refresh rate for sampling
if args.refresh_rate is not None:
	refresh_rate = int(args.refresh_rate)
else:
	# set default to 15
	refresh_rate = 15

# 
# Functions
#

def send_cpu_alert_email(cpu_load_threshold, cpu_load_avg, cpu_interval):
	""" Sends an email out based on given information """

	# Set a few variables to make the email nice looking
	date_stamp = str(time.strftime("%c"))
	divider = str('-' * 80 + "\n")
	origin_host = socket.gethostname()

	# Define the message headers
	msg = MIMEMultipart()
	msg["From"] = "" 
	msg["To"] = "" 
	#msg["Cc"] = "udahadoopops@geisinger.edu" 
	msg["Subject"] = "Cluster CPU load threshold reached on: " + origin_host
	msg.attach(MIMEText(
	"Notice: \nCPU load avg of " + str(cpu_load_threshold) + " reached" +
	" at an interval of " + cpu_interval_string +
	". The load avg at time of notification was " + str(cpu_load_avg) +
	"\n\nPlease do not reply to this email.\n\n" + divider + 
	"(Sent via Linux Sendmail on " + origin_host + " at " + date_stamp + " via os-resource-mon.py)"
	))

	p = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	p.communicate(msg.as_string())

def test_cpu_load(finish_time, cpu_load_threshold1, cpu_load_threshold5, cpu_load_threshold15, cpu_interval, raw_avg_index):
	"""Tests CPU load from a fixed time frame"""

	# Goal: want to know if five minute load avg exceeds 2xCPU (on our nodes greater than 80)
	# and/or if iowait exceeds 30. Generate CPU load with parallel instances of:
	# 'dd if=/dev/zero of=/dev/null'

	# Set warning at 50%, Critical at 90%
	cpu_load_avg_1min = cpu_load_threshold1
	cpu_load_avg_5min = cpu_load_threshold5
	cpu_load_avg_15min = cpu_load_threshold15
	cpu_load_threshold =  cpu_interval
	cpu_load_avg_warning = cpu_load_threshold * .5
	cpu_load_avg_critical = cpu_load_threshold * .9
	print "Running OS load averge until:", finish_time
	print "Host:", origin_host
	print "CPU interval:", cpu_interval_string
	print "Refresh rate:", refresh_rate, "seconds"
	print "CPU load threshold:", cpu_load_threshold

	while datetime.datetime.now() < finish_time:
		raw_avg = os.getloadavg()
		cpu_load_avg = {1: raw_avg[0], 5: raw_avg[1], 15: raw_avg[2]}
		logging.info("CPU Load sample: " + str(cpu_load_avg))

		if raw_avg[raw_avg_index] >= cpu_load_avg_critical:
			sys.stdout.write('\r'+ 'CRITICAL: CPU load avg at critical capacity              ')
			sys.stdout.flush()
			logging.critical("\nCPU load at critical capacity: " + str(cpu_load_avg))
		elif raw_avg[raw_avg_index] >= cpu_load_avg_warning:
			# Make sure to make the buffer rewrite at least as long as the last to overwrite it all
			sys.stdout.write('\r'+ 'WARNING: CPU load avg at half capacity                  ')
			sys.stdout.flush()
			logging.warning("\nCPU load at half capacity: " + str(cpu_load_avg))
		elif raw_avg[raw_avg_index] < cpu_load_threshold:
			sys.stdout.write('\r'+ 'CPU load avg within threshhold. Continuing to monitor...')
			sys.stdout.flush()

		# Check outside of conditionals if the load_avg has been met
		if raw_avg[raw_avg_index] > cpu_load_threshold:
			logging.info("Sending alert email")
			send_cpu_alert_email(cpu_load_threshold, cpu_load_avg, cpu_interval)
			logging.error("\nCPU load avg reached! Load avg: " + str(cpu_load_avg))
			logging.info("\nSleeping for 15 minutes to allow cooldown")
			# sleep for a bit to see if cpu load avg calms down so we are not bombarded with emails
			# Use 15 minutes for now for account for a job finishing up
			time.sleep(900)

		# Idle for a bit so we are not flooding the log
		time.sleep(refresh_rate)
#
# main
#

test_cpu_load(finish_time, cpu_load_threshold1, cpu_load_threshold5, cpu_load_threshold15, cpu_interval, raw_avg_index)

print ''

#
# End log file
#

logging.info("\n-------------------------\nEND LOG FILE\n-------------------------\n") 
