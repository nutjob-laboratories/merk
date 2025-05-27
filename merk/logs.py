#
# ███╗   ███╗██████╗ ██████╗ ██╗  ██╗
# ████╗ ████║╚═══╗██╗██╔══██╗██║ ██╔╝
# ██╔████╔██║███████║██████╔╝█████╔╝
# ██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗
# ██║ ╚═╝ ██║ █████╔╝██║  ██║██║  ██╗
# ╚═╝     ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
# Copyright (C) 2025  Daniel Hetrick
# https://github.com/nutjob-laboratories/merk
# https://github.com/nutjob-laboratories
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import os
import json
from pathlib import Path
from datetime import datetime

from .resources import *

CONFIG_DIRECTORY = None
LOG_DIRECTORY = None

def initialize(directory,directory_name):
	global CONFIG_DIRECTORY
	global LOG_DIRECTORY

	# If the passed directory is set to None,
	# set the storage directory to the user's
	# home directory
	if directory==None:
		directory = str(Path.home())

	# The config directory should already be created
	CONFIG_DIRECTORY = os.path.join(directory,directory_name)

	LOG_DIRECTORY = os.path.join(CONFIG_DIRECTORY,"logs")
	if not os.path.isdir(LOG_DIRECTORY): os.mkdir(LOG_DIRECTORY)

# Functions

# Converts an array of Message() objects to an array of arrays
def log_to_array(log):
	out = []
	for l in log:
		entry = [ l.timestamp,l.type,l.sender,l.contents ]
		out.append(entry)
	return out

# Converts an array of arrays to an array of Message Objects
def array_to_log(log):
	out = []
	for l in log:
		m = Message(l[1],l[2],l[3],l[0])
		out.append(m)
	return out

def trimLog(ilog,maxsize):
	count = 0
	shortlog = []
	for line in reversed(ilog):
		count = count + 1
		shortlog.append(line)
		if count >= maxsize:
			break
	return list(reversed(shortlog))

def encodeLogName(network,name=None):
	network = network.replace(":","-")
	network = network.lower()
	if name==None:
		return f"{network}.json"
	else:
		return f"{network}-{name}.json"

# Takes an array of Message() objects, converts it to
# an AoA, and appens the AoA to a file containing
# AoAs on disk
def saveLog(network,name,logs,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	logs = log_to_array(logs)

	slog = loadLog(network,name,logdir)
	for e in logs:
		slog.append(e)

	with open(logfile, "w",encoding="utf-8",errors="ignore") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

# Takes an array of Message() objects, converts it to
# an AoA, and appens the AoA to a file containing
# AoAs on disk
def saveLogFile(network,name,logs,logdir=LOG_DIRECTORY,logfile=None):

	logs = log_to_array(logs)

	slog = loadLog(network,name,logdir)
	for e in logs:
		slog.append(e)

	with open(logfile, "w",encoding="utf-8",errors="ignore") as writelog:
		json.dump(slog, writelog, indent=4, sort_keys=True)

# Loads an AoA from disk and returns it
def loadLog(network,name,logdir=LOG_DIRECTORY):
	f = encodeLogName(network,name)
	logfile = os.path.join(logdir,f)

	if os.path.isfile(logfile):
		with open(logfile, "r",encoding="utf-8",errors="ignore") as logentries:
			data = json.load(logentries)
			return data
	else:
		return []

# Loads an AoA from disk, converts it to an arroy
# of Message() objects, and returns it
def readLog(network,name,logdir=LOG_DIRECTORY):
	logs = loadLog(network,name,logdir)
	logs = array_to_log(logs)
	return logs

def dumpRawLog(logs):
	delimiter = "\t"
	logs = log_to_array(logs)

	out = []
	for l in logs:
		l[2] = l[2].strip()
		l[3] = l[3].strip()
		if l[2]=='': l[2] = '***'

		pretty_timestamp = datetime.fromtimestamp(l[0]).strftime('%a, %d %b %Y %H:%M:%S')
		entry = pretty_timestamp+delimiter+l[2]+delimiter+l[3]
		out.append(entry)
	return "\n".join(out)

# Loads an AoA from disk, converts it to a string
def dumpLog(filename,delimiter,linedelim="\n",epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r",encoding="utf-8",errors="ignore") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			l[2] = l[2].strip()
			l[3] = l[3].strip()
			if l[2]=='': l[2] = '***'

			if not epoch:
				pretty_timestamp = datetime.fromtimestamp(l[0]).strftime('%a, %d %b %Y %H:%M:%S')
				entry = pretty_timestamp+delimiter+l[2]+delimiter+l[3]
			else:
				entry = str(l[0])+delimiter+l[2]+delimiter+l[3]
			out.append(entry)
		return linedelim.join(out)
	else:
		return ''

# Loads an AoA from disk, converts it to a JSON string
def dumpLogJson(filename,epoch=True):
	if os.path.isfile(filename):
		with open(filename, "r",encoding="utf-8",errors="ignore") as logentries:
			logs = json.load(logentries)
	if logs:
		out = []
		for l in logs:
			l[2] = l[2].strip()
			l[3] = l[3].strip()
			if l[2]=='': l[2] = '*'
			if not epoch:
				l[0] = datetime.fromtimestamp(l[0]).strftime('%a, %d %b %Y %H:%M:%S')
			entry = [ l[0],l[2],l[3] ]
			out.append(entry)
		return json.dumps(out, indent=4, sort_keys=True)
	else:
		return ''